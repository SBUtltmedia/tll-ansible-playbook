"""
1. Run update_hostnames() from scripts/update_hostnames.py
2. Update inventory.ini file: Run update_inventory_ini() from from scripts/update_hostnames.py
3. Run scipts/generate.py to generate the new hosts file
4. Run scripts/push_and_run.py to push the command into machines and run it.
5. Run ansible-playbook -i inventory.ini setup.yml -Kk
6. Gain admin privilages by running makemeadmin.command in the remote hosts
7. Run ansible-playbook -i inventory.ini install-softwares.yml -k
"""

import subprocess
import os
import sys
import logging

# Assume other scripts are in a 'scripts' directory relative to this file
# This is a good practice for organizing your project
# We will use this path to import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))

try:
    from update_hostnames import update_hostnames, update_inventory_ini, become_admin
    from generate import generate_hosts_file
    from push_and_run import push_and_run
except ImportError as e:
    logging.error(f"Error importing required modules. Please ensure all scripts are in the 'scripts' directory.")
    logging.error(f"ImportError: {e}")
    sys.exit(1)


def run_ansible_playbook(playbook_name, inventory_file='inventory.ini'):
    """
    Executes an Ansible playbook using the subprocess module.

    Args:
        playbook_name (str): The name of the playbook file (e.g., 'setup.yml').
        inventory_file (str): The path to the inventory file.
    """
    ansible_command = [
        'ansible-playbook',
        '-i', inventory_file,
        playbook_name,
        '-K', # Ask for sudo password
        '-k'  # Ask for SSH password
    ]
    
    print(f"Executing Ansible command: {' '.join(ansible_command)}")
    
    try:
        # Use subprocess.run to execute the command and wait for it to finish
        result = subprocess.run(ansible_command, check=True, capture_output=True, text=True)
        logging.info("Standard Output:")
        logging.info(result.stdout)
        logging.info("Standard Error:")
        logging.info(result.stderr)
        logging.info(f"Successfully ran '{playbook_name}'")
    except subprocess.CalledProcessError as e:
        logging.error(f"An error occurred while running playbook '{playbook_name}':")
        logging.error("Standard Output:")
        logging.error(e.stdout)
        logging.error("Standard Error:")
        logging.error(e.stderr)
        sys.exit(1)
    except FileNotFoundError:
        logging.error("Error: 'ansible-playbook' command not found. Please ensure Ansible is installed and in your PATH.")
        sys.exit(1)


def main_pipeline():
    """
    Main function to run the complete pipeline of steps.
    """
    logging.info("--- Starting Pipeline ---")

    # Step 1: Run update_hostnames()
    logging.info("Step 1: Running update_hostnames()")
    # In a real scenario, this function would return the list of hosts to be used
    try:
        new_hosts = update_hostnames()
        logging.info(f"New hostnames received: {new_hosts}")
    except Exception as e:
        logging.error(f"Step 1 failed: {e}")
        sys.exit(1)

    # Step 2: Update inventory.ini file
    logging.info("Step 2: Updating inventory.ini file with new hostnames")
    try:
        update_inventory_ini('inventory.ini', new_hosts)
    except Exception as e:
        logging.error(f"Step 2 failed: {e}")
        sys.exit(1)

    # Step 3: Run generate.py to generate the new hosts file
    logging.info("Step 3: Running generate.py to generate the new hosts file")
    try:
        generate_hosts_file()
    except Exception as e:
        logging.error(f"Step 3 failed: {e}")
        sys.exit(1)
    
    # Step 4: Run push_and_run.py to push and run the command
    logging.info("Step 4: Running push_and_run.py to push and run the command on machines")
    try:
        push_and_run()
    except Exception as e:
        logging.error(f"Step 4 failed: {e}")
        sys.exit(1)

    # Step 5: Run ansible-playbook -i inventory.ini setup.yml -Kk
    logging.info("Step 5: Running Ansible playbook 'setup.yml'")
    run_ansible_playbook('setup.yml')
    
    # Step 7: Get admin privs on all remote machines
    logging.info("Gaining admin privs on all remote machines")
    become_admin()

    # Step 7: Run ansible-playbook -i inventory.ini install-softwares.yml -k
    logging.info("Step 6: Running Ansible playbook 'install-softwares.yml'")
    run_ansible_playbook('install-softwares.yml')
    
    logging.info("\n--- Pipeline Completed Successfully ---")

if __name__ == "__main__":
    main_pipeline()