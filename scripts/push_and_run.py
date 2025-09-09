import paramiko
import json
import sys
import os
import logging
from util import run_command_over_ssh

os.path.dirname(os.path.abspath(__file__))

username = "tltmedia"
password = sys.argv[1]
TURNOFFSFTP = False
port = 22

def push_and_run():
    with open('scripts/machines.json') as json_data:
        d = json.load(json_data)
        json_data.close()

    ssh_client = paramiko.SSHClient()
    for machine in d:
        try:
            if not TURNOFFSFTP:
                host = machine['machineName']
                ip = machine['ip']
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_client.connect(hostname=ip,port=port,username=username,password=password, timeout=1)
                ftp = ssh_client.open_sftp()
                ftp.put("scripts/checkForXcodeCLI.command","/Users/Shared/checkForXcodeCLI.command")
                ftp.put("scripts/makeadmin.command","/Users/Shared/makeadmin.command")
                logging.info(f'Moved file to {host}')
                logging.info("Runing command")
                run_command_over_ssh(ip, "tltmedia", "key.pem", "./Users/Shared/checkForXcodeCLI.command")
        except Exception as e:
            logging.error(f"Could not copy over {host}: {e}")
