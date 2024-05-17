import paramiko
import json
import sys
username = "tltmedia"
password = sys.argv[1]
TURNOFFSFTP=False
port = 22
with open('scripts/machines.json') as json_data:
    d = json.load(json_data)
    json_data.close()

ssh_client = paramiko.SSHClient()
for machine in d:
    if(not TURNOFFSFTP):
        host = machine
        try:
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname=host,port=port,username=username,password=password)
            ftp = ssh_client.open_sftp()
            ftp.put("/Users/xiqchen/ansible/scripts/checkForXcodeCLI.command","/Users/Shared/checkForXcodeCLI.command")
            print(f'Moved file to {host}')
        except:
            print(f'An exception occurred with {host}')
