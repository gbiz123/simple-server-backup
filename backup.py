"""
Back up servers that are listed in your /etc/hosts file.

Runs the following linux command:
ssh root@{hostname} "dd if={device_name} bs=4M status=progress" | dd of=/path/to/backup/{hostname}.img bs=4

Your /etc/hosts must have a block meeting the following requirements:
    - Starts with # BACKUP START
    - Ends with # BACKUP END
    - Each host has a comment with the name of the device to copy

Your remote server must allow root login and have ssh configured properly.

# BACKUP START
138.197.107.25 dispersions-db # /dev/vda
93.127.215.242 mailserver # /dev/sda
192.168.1.8 fedora-desktop # /dev/sdb
# BACKUP END
"""

import re
import subprocess

BACKUP_PATH = "/home/gregb/Backup"

with open("/etc/hosts") as f:
    etc_hosts = f.read()

in_backup_block = False
hosts = []
for line in etc_hosts.splitlines():
    if line.startswith("# BACKUP START"):
        in_backup_block = True
        continue
    if line.startswith("# BACKUP END"):
        in_backup_block = False
        continue
    if in_backup_block:
        cleaned_line = re.sub("#", "", line)
        cleaned_line = re.sub(r"\s+", " ", cleaned_line)
        print(cleaned_line)
        ip, host, device = cleaned_line.strip().split()
        hosts.append(
            {
                "ip": ip,
                "host": host,
                "device": device
            }
        )

for host in hosts:
    cmd = 'ssh root@{host} "dd if={device} bs=4M status=progress" | dd of={backup_path}/{host}.img bs=4'.format(
            ip=host["ip"],
            backup_path=BACKUP_PATH,
            host=host["host"],
            device=host["device"]
    )
    print("-"*30)
    print(cmd)
    subprocess.run([cmd], capture_output=True, text=True, shell=True)
