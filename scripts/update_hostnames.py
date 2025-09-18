from util import run_command_on_all_machines
import json
import logging
import configparser

INI_FILE_PATH = "inventory.ini"

def update_hostnames():
    with open("scripts/machines.json") as data:
        d = json.load(data)
        data.close()
        
    res = run_command_on_all_machines("tltmedia", "/Users/tltmedia/.ssh/id_rsa.pub", "hostname")
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
    
    return True

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
        run_command_on_all_machines("tltmedia", "/Users/tltmedia/.ssh/id_rsa.pub", "./Users/Shared/makeadmin.command")
    except Exception as e:
        logging.error(f"Error becoming admin: {e}")