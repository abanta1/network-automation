#!/usr/bin/env python3
# Usage
# python backup_configs.py --ip 10.0.0.1 --outdir ./configs --save-creds
# python backup_configs.py --file devices.txt --outdir ./configs
#
# Windows Dependencies
# py -m pip install netmiko cryptography
# OpenSSH Client installed

import argparse, getpass, os, socket, json
from netmiko import ConnectHandler
from cryptography.fernet import Fernet
from datetime import datetime, date

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
    ips = []
    if args.ip: ips.append(args.ip)
    if args.ipfile:
        with open(args.ipfile) as f:
            ips += [l.strip() for l in f if l.strip()]
    return ips

def main():
    try:
        ap = argparse.ArgumentParser()
        ap.add_argument("--ip")
        ap.add_argument("--ipfile")
        ap.add_argument("--type", required=True, help="Override autodetect (ios, junos, iosxr)")
        ap.add_argument("--reset", help="Resets credentials")
        ap.add_argument("--log", action="store_true", help="Enable logs")
        ap.add_argument("--config", action="store_true", help="Enable Configure Terminal mode")
        ap.add_argument("--outdir", help="Directory to write configs") 
        args = ap.parse_args()

        # DEBUG
        if (args.log):
            print("[DEBUG] DEV TYPE:", args.type)

        # Load or create creds
        if os.path.exists(CRED_FILE):
            if (args.log): print(f"[INFO] Using saved credentials")
        else:
            if (args.log): print(f"[WARN] No saved credentials, obtaining")
            create_creds()

        user,pw = load_creds()

        for ip in get_ips(args):
            # Validate config file
            print("Checking: ", os.path.abspath(os.path.join(args.outdir, ip)))
            if not os.path.isdir(os.path.join(args.outdir, ip)):
                print(f"[WARN] Config dir not found: {os.path.join(args.outdir, ip)}, Creating dir...")
                try:
                    os.mkdir(os.path.join(args.outdir, ip))
                except Exception as e:
                    print("[ERROR] {e}")
            
            curdir = os.path.join(args.outdir, ip)
            
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

            try:
                conn = ConnectHandler(**dev)
                currdatetime = datetime.now().strftime("%Y%m%d-%H%M")
                
                if conn.device_type == "juniper_junos":
                    cfg = conn.send_command("show configuration | display set | no-more")
                elif conn.device_type in ["cisco_xr","cisco_iosxr"]:
                    cfg = conn.send_command("show running-config")
                else:
                    cfg = conn.send_command("show running-config")

                fname = os.path.join(curdir, f"{currdatetime}.cfg")
                with open(fname,"w") as f: f.write(cfg)
                #print(cfg)
                print(f"[OK] {os.path.abspath(args.outdir)}\\{ip}\\{currdatetime}.cfg saved")

                conn.disconnect()
            except Exception as e:
                print(f"[FAIL] {ip}: {e}")
    except KeyboardInterrupt:
        print("\n[ABORTED] Ctrl-C pressed, exiting cleanly.")

if __name__ == "__main__":
    main()
