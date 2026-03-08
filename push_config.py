#!/usr/bin/env python3
# Usage
# python push_configs.py --ip 10.0.0.1 --config update.cfg
# python push_configs.py --file devices.txt --config update.cfg
#
# Windows Dependencies
# py -m pip install netmiko cryptography
# OpenSSH Client installed

import argparse, getpass, os, json
from netmiko import ConnectHandler
from cryptography.fernet import Fernet

# Windows
BASE = os.path.join(os.environ["USERPROFILE"], ".netmgr")
os.makedirs(BASE, exist_ok=True)
CRED_FILE = os.path.join(BASE, "creds.enc")
KEY_FILE = os.path.join(BASE, "key.bin")

# Linux
# CRED_FILE = os.path.expanduser("~/.net_creds.enc")
# KEY_FILE = os.path.expanduser("~/.net_creds.key")

def init_crypto():
    os.makedirs(BASE, exist_ok=True)
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
    return Fernet(open(KEY_FILE, "rb").read())

def create_creds():
    fernet = init_crypto()
    user = input("Username: ")
    pw = getpass.getpass("Password: ")
    data = json.dumps({"u": user, "p": pw}).encode()
    enc = fernet.encrypt(data)
    with open(CRED_FILE, "wb") as f:
        f.write(enc)
    print("[OK] Encrypted credentials created")

def load_key(): return open(KEY_FILE,"rb").read()

def load_creds():
    f = Fernet(load_key())
    data = f.decrypt(open(CRED_FILE,"rb").read())
    j = json.loads(data.decode())
    return j["u"], j["p"]

def get_ips(args):
    ips=[]
    if args.ip: ips.append(args.ip)
    if args.file:
        with open(args.file) as f:
            ips += [l.strip() for l in f if l.strip()]
    return ips

def main():
    try:
        ap = argparse.ArgumentParser()
        ap.add_argument("--ip")
        ap.add_argument("--file")
        ap.add_argument("--configfile", required=True)
        ap.add_argument("--type", required=True, help="Override autodetect (ios, junos, iosxr)")
        ap.add_argument("--reset", help="Resets credentials")
        ap.add_argument("--log", action="store_true", help="Enable logs")
        ap.add_argument("--config", action="store_true", help="Enable Configure Terminal mode")
        args = ap.parse_args()

        # DEBUG
        if (args.log):
            print("[DEBUG] CONFIG FILE:", args.configfile)
            print("[DEBUG] DEV TYPE:", args.type)
        
        # Validate config file
        if not os.path.isfile(args.configfile):
            print(f"[ERROR] Config file not found: {args.configfile}")
            return
            
        # Load or create creds
        if os.path.exists(CRED_FILE):
            if (args.log): print(f"[INFO] Using saved credentials")
        else:
            if (args.log): print(f"[WARN] No saved credentials, obtaining")
            create_creds()

        user,pw = load_creds()
        
        # Load commands
        cmds = [l.strip() for l in open(args.configfile) if l.strip()]

        for ip in get_ips(args):
            print(f"\n=== Connecting to {ip} ===")
            
            dev = {
                "device_type": "autodetect",
                "host": ip,
                "username": user,
                "password": pw,
                "fast_cli": False
            }
            
            dev["device_type"] = args.type
            
            if (args.log): print(f"[INFO] Using device type: {args.type}")
            print(f"Test") 
            
            try:
                conn = ConnectHandler(**dev)
                print(f"Test2")
                print(f"{conn.device_type}")
                if (args.configfile): 
                    print(f"args.configfile present") 
                else: 
                    print(f"args.configfile not present")
                if conn.device_type == "juniper_junos":
                    print(f"Test3")
                    if (args.config):
                        conn.config_mode()
                        out = conn.send_config_set(cmds)
                        commit = conn.send_command("commit")
                        print(f"[{ip}] {out}\n{commit}")
                    else:
                        for cmd in cmds:
                            # EXEC commands
                            if cmd.startswith(("do ", "show ", "sh ")):
                                out = conn.send_command(cmd)
                            # CONFIG commands
                            else:
                                out = conn.send_config_set([cmd])

                elif conn.device_type in ["cisco_xr","cisco_iosxr"]:
                    print(f"Test4")
                    if (args.config):
                        out = conn.send_config_set(cmds)
                        commit = conn.send_command("commit")
                        print(f"[{ip}] {out}\n{commit}")
                    else:
                        for cmd in cmds:
                            # EXEC commands
                            if cmd.startswith(("do ", "show ", "sh ")):
                                out = conn.send_command(cmd)
                            # CONFIG commands
                            else:
                                out = conn.send_config_set([cmd])

                else:  # IOS-XE
                    if (args.config):
                        print(f"Test5")
                        print(f"Sending: {cmds}")
                        out = conn.send_config_set(cmds)
                        save = conn.send_command("write memory")
                        print(f"[{ip}] {out}\n{save}")
                    else:
                        print(f"Test5b")
                        print(f"{cmds}")
                        for cmd in cmds:
                            print(f"{cmd}")
                            # EXEC commands
                            if cmd.startswith(("do ", "show ", "sh ")):
                                print(f"Test 5c")
                                out = conn.send_command(cmd)
                            # CONFIG commands
                            else:
                                out = conn.send_config_set([cmd])
                print(f"Test6")
                conn.disconnect()
                print(f"Printing results:")
                print(out)
                
            except Exception as e:
                print(f"[FAIL] {ip}: {e}")
    except KeyboardInterrupt:
        print("\n[ABORTED] Ctrl-C pressed, exiting cleanly.")
        
if __name__ == "__main__":
    main()
