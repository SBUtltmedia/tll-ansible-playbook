import paramiko
import json
import os
import logging
from util import run_command_on_all_machines

os.path.dirname(os.path.abspath(__file__))

key_file = os.getenv("KEY_PATH")

TURNOFFSFTP = False
port = 22

def error_check(res):
    for ip in res:
        if "error" in res[ip] and res[ip]["error"] != "":
            return False
    
    return True

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
                logging.info(f"Moving files to {host} : {ip}")
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_client.connect(hostname=ip,port=port, key_filename=key_file, timeout=20)
                ftp = ssh_client.open_sftp()
                ftp.put("scripts/commands/checkForXcodeCLINew.command","/Users/Shared/checkForXcodeCLI.command")
                ftp.put("scripts/commands/makemeadmin.command","/Users/Shared/makemeadmin.command")
                ftp.put("scripts/commands/install_brew.sh","/Users/Shared/install_brew.sh")
                ftp.put("scripts/commands/installansible.command","/Users/Shared/installansible.command")
                logging.info(f'Moved files to {host}')
        except Exception as e:
            logging.error(f"Could not copy over {host}: {e}")
            return False

    return True

def run_checkforxcode_cli():
    res = run_command_on_all_machines(username="tltmedia", key_file=key_file, command="sh /Users/Shared/checkForXcodeCLI.command")
    return error_check(res)

def run_makemeadmin():
    res = run_command_on_all_machines(username="tltmedia", key_file=key_file, command="sh /Users/Shared/makemeadmin.command")
    return error_check(res)
