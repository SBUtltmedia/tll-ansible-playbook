import paramiko
import json
import sys
import os

os.path.dirname(os.path.abspath(__file__))

username = "tltmedia"
password = sys.argv[1]
TURNOFFSFTP = False
port = 22
with open('scripts/machines.json') as json_data:
    d = json.load(json_data)
    json_data.close()

ssh_client = paramiko.SSHClient()
for machine in d:
    try:
        if not TURNOFFSFTP:
            host = machine['machineName']
            ip = machine['ip']
            print(host)
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname=ip,port=port,username=username,password=password, timeout=1)
            ftp = ssh_client.open_sftp()
            ftp.put("scripts/checkForXcodeCLI.command","/Users/Shared/checkForXcodeCLI.command")
            print(f'Moved file to {host}')
    except Exception as e:
        print(f"Could not copy over {host}: {e}")
