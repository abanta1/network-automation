#!/usr/bin/env python3

from netmiko import ConnectHandler
import getpass, datetime

ftddevice = {
 'device_type': 'cisco_ftd',
 'host': '10.0.0.1',
 'username': 'username',
 'password': 'Password123',
 }
iosxedevice = {
 'device_type': 'cisco_xe',
 'host': '10.0.0.1',
 'username': 'username',
 'password': 'Password123',
 }

all_devices = [ftddevice, iosxedevice]

start_time = datetime.datetime.now()
for a_device in all_devices:
 ssh = ConnectHandler(**a_device)
 prompt = ssh.find_prompt()
 output = ssh.send_command("show run")
 output2 = ssh.send_command("show vrf")
 output3 = ssh.send_command("show ip route")
 output4 = ssh.send_command("show ipv route")
 output5 = ssh.send_command("show ip int br")
 output6 = ssh.send_command("show ipv int br")
 output7 = ssh.send_command("show ip proto")
 output8 = ssh.send_command("show ipv proto")
 output9 = ssh.send_command("show cdp nei")
 output10 = ssh.send_command("show lldp nei")
 output11 = ssh.send_command("show ip bgp nei")
 output12 = ssh.send_command("show bgp ipv4 uni nei")
 output13 = ssh.send_command("show bgp ipv6 uni nei")
 output14 = ssh.send_command("show bgp top")
 output15 = ssh.send_command("show bgp sum")
 output16 = ssh.send_command("show kospf nei")
 output17 = ssh.send_command("show ospf int")
 output18 = ssh.send_command("show ospf datab")
 output19 = ssh.send_command("show eigrp proto")
 output20 = ssh.send_command("show ip eigrp nei")
 output21 = ssh.send_command("show ip eigrp top")
 output22 = ssh.send_command("show ip eigrp int")
 output23 = ssh.send_command("show vtp stat")
 output24 = ssh.send_command("show vtp dev")
 output25 = ssh.send_command("show ntp ass")
 output26 = ssh.send_command("show ntp stat")
 print(f"\n\n------------------------- Device {a_device['host']} ----------------------------")
 print(prompt + " show run")
 print(output)
 print(prompt + " show vrf")
 print(output2)
 print(prompt + " show ip route")
 print(output3)
 print(prompt + " show ipv route")
 print(output4)
 print(prompt + " show ip int br")
 print(output5)
 print(prompt + " show ipv int br")
 print(output6)
 print(prompt + " show ip proto")
 print(output7)
 print(prompt + " show ipv proto")
 print(output8)
 print(prompt + " show cdp nei")
 print(output9)
 print(prompt + " show lldp nei")
 print(output10)
 print(prompt + " show ip bgp nei")
 print(output11)
 print(prompt + " show bgp ipv4 uni nei")
 print(output12)
 print(prompt + " show bgp ipv6 uni nei")
 print(output13)
 print(prompt + " show bgp top")
 print(output14)
 print(prompt + " show bgp sum")
 print(output15)
 print(prompt + " show kospf nei")
 print(output16)
 print(prompt + " show ospf int")
 print(output17)
 print(prompt + " show ospf datab")
 print(output18)
 print(prompt + " show eigrp proto")
 print(output19)
 print(prompt + " show ip eigrp nei")
 print(output20)
 print(prompt + " show ip eigrp top")
 print(output21)
 print(prompt + " show ip eigrp int")
 print(output22)
 print(prompt + " show vtp stat")
 print(output23)
# print(prompt + " show vtp dev")
# print(output24)
 print(prompt + " show ntp ass")
 print(output25)
 print(prompt + " show ntp stat")
 print(output26)
 print(f"\n\n------------------------------ End {a_device['host']} --------------------------------")
 ssh.disconnect()

end_time = datetime.datetime.now()
total_time = end_time - start_time
print(total_time)
