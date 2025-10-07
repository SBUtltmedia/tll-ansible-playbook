from util import run_command_on_all_machines
import json
import logging
import configparser
import os
import subprocess
import sys

INI_FILE_PATH = "inventory.ini"

key_file = os.getenv("KEY_PATH")

def update_hostnames():
    with open("scripts/machines.json") as data:
        d = json.load(data)
        data.close()
        
    res = run_command_on_all_machines("tltmedia", key_file, "hostname")
    print("RES: ", res)
    for ip in res:
        try:
            if res[ip]["stderr"] == "":
                for machine in d:
                    if machine["ip"] == ip:
                        machine["machineName"] = res[ip]["stdout"]
            else:
                logging.error(f"Could not get hostname for ip: {ip}")
                return False
        except Exception as e:
            logging.error(f"Error - Key not found in update_hostnames()")
            return False
    
    logging.info("Updating hostfile")

    process = subprocess.Popen(
        ["sh", "scripts/commands/sshkey.command"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1  # Important for real-time line-by-line output
    )

    # Stream stdout in real-time
    for line in iter(process.stdout.readline, ''):
        logging.info(f"[STDOUT] {line.strip()}")
    
    # Stream stderr in real-time
    for line in iter(process.stderr.readline, ''):
        logging.error(f"[STDERR] {line.strip()}")
        
    # Wait for the process to complete and get the return c
    return_code = process.wait()

    if return_code == 0:
        logging.info(f"Successfully ran sshkey.command with exit code {return_code}.")
        return True
    else:
        logging.error(f"An error occurred while running sshkey.command. Exited with code {return_code}.")
        return False   

def update_inventory_ini():
    try:
        config = configparser.ConfigParser(allow_no_value=True)
        config.read(INI_FILE_PATH)
    except Exception as e:
        logging.error(f"An unexpected error occurred while reading the INI file: {e}")
        return
    
    config.remove_section('localhost')
    config.add_section('localhost')

    with open("scripts/machines.json", "r") as file:
        data = json.load(file)
        for machine in data:
            config['localhost'][machine['machineName']] = None
    
    try:
        # Write the updated configuration back to the file
        with open(INI_FILE_PATH, 'w') as configfile:
            config.write(configfile)
        logging.info(f"Successfully updated '[localhost]' section in '{INI_FILE_PATH}' with the new hostnames.")
        return True
    except Exception as e:
        logging.error(f"An error occurred while writing to the file: {e}")
        return False


def become_admin():
    try:
        run_command_on_all_machines("tltmedia", key_file, "./Users/Shared/makeadmin.command")
    except Exception as e:
        logging.error(f"Error becoming admin: {e}")
