import paramiko
import json
import os
import logging
from util import run_command_on_all_machines

os.path.dirname(os.path.abspath(__file__))

TURNOFFSFTP = False
port = 22

def push_files():
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
                ssh_client.connect(hostname=ip,port=port, key_filename="/Users/tltmedia/.ssh/id_rsa.pub", timeout=15)
                ftp = ssh_client.open_sftp()
                ftp.put("scripts/checkForXcodeCLI.command","/Users/Shared/checkForXcodeCLI.command")
                ftp.put("scripts/makemeadmin.command","/Users/Shared/makemeadmin.command")
                logging.info(f'Moved file to {host}')
                # logging.info("Runing command")
                # run_command_over_ssh(ip, "tltmedia", "/Users/tltmedia/.ssh/id_rsa.pub", "./Users/Shared/checkForXcodeCLI.command")
        except Exception as e:
            logging.error(f"Could not copy over {host}: {e}")
            return False

    return True

def run_checkforxcode_cli():
    res = run_command_on_all_machines(username="tltmedia", key_file="/Users/tltmedia/.ssh/id_rsa.pub", command="sh /Users/Shared/checkForXcodeCLI.command")
    for ip in res:
        if "error" in res[ip] and res[ip]["error"] != "":
            return False
    
    return True

def run_makemeadmin():
    res = run_command_on_all_machines(username="tltmedia", key_file="/Users/tltmedia/.ssh/id_rsa.pub", command="sh /Users/Shared/makemeadmin.command")
    for ip in res:
        if "error" in res[ip] and res[ip]["error"] != "":
            return False
    
    return True
