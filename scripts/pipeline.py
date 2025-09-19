"""
1. Run update_hostnames() from scripts/update_hostnames.py
2. Update inventory.ini file: Run update_inventory_ini() from from scripts/update_hostnames.py
3. Run scipts/generate.py to generate the new hosts file
4. Run scripts/push_and_run.py's push_files() to push the command into machines.
5. Run scripts/push_and_run.py's run_checkforxcode_cli() to run the command checkForXcodeCLI.command
5. Run ansible-playbook -i inventory.ini setup.yml -Kk
6. Run scripts/push_and_run.py's run_makemeadmin() to run the make the user(tltmedia) admin
7. Run ansible-playbook -i inventory.ini install-softwares.yml -k
"""

from dotenv import load_dotenv

import subprocess
import os
import sys
import logging


load_dotenv()
# Assume other scripts are in a 'scripts' directory relative to this file
# This is a good practice for organizing your project
# We will use this path to import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))

root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.INFO)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

root_logger.addHandler(file_handler)
root_logger.addHandler(stream_handler)

try:
    from update_hostnames import update_hostnames, update_inventory_ini, become_admin
    from generate import generate_hosts_file
    from push_and_run import push_files, run_checkforxcode_cli, run_makemeadmin
except ImportError as e:
    logging.error(f"Error importing required modules. Please ensure all scripts are in the 'scripts' directory.")
    logging.error(f"ImportError: {e}")
    sys.exit(1)


def run_ansible_playbook(playbook_name, inventory_file='inventory.ini'):
    """
    Executes an Ansible playbook and streams the output in real-time.

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
        # Use subprocess.Popen to execute the command and get a process object.
        # stdout and stderr are set to subprocess.PIPE to capture the output.
        process = subprocess.Popen(
            ansible_command,
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
            
        # Wait for the process to complete and get the return code
        return_code = process.wait()

        if return_code == 0:
            logging.info(f"Successfully ran '{playbook_name}' with exit code {return_code}.")
        else:
            logging.error(f"An error occurred while running playbook '{playbook_name}'. Exited with code {return_code}.")
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
    res = update_hostnames()

    if not res:
        logging.error("Cound not get all hosts")
        sys.exit(1)

    # Step 2: Update inventory.ini file
    logging.info("Step 2: Updating inventory.ini file with new hostnames")
    if not update_inventory_ini():
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
    logging.info("Step 4: Running push_and_run.py's push_file() to push the files onto all machines")
    if not push_files():
        logging.error(f"Step 4 failed")
        sys.exit(1)
    
    # Step 5: run checkForXcodeCLI on all machines
    logging.info("Step 5: Running push_and_run.py's run_checkforxcode_cli() to run the command on machines")
    if not run_checkforxcode_cli():
        logging.error(f"Step 5 failed")
        sys.exit(1)

    # Step 6: Get admin privs on all remote machines
    logging.info("Step 6: Gaining admin privs on all remote machines")
    if not run_makemeadmin():
        logging.error(f"Step 6 failed")
        sys.exit(1)

    # Step 7: Run ansible-playbook -i inventory.ini setup.yml -Kk
    logging.info("Step 7: Running Ansible playbook 'setup.yml'")
    run_ansible_playbook('setup.yml')

    # Step 8: Run ansible-playbook -i inventory.ini install-softwares.yml -k
    logging.info("Step 8: Running Ansible playbook 'install-softwares.yml'")
    run_ansible_playbook('install-softwares.yml')

    # Step 9: Setup Ollama
    logging.info("Step 9: Running Ansible playbook 'roles/ollama-gateway/tasks/main.yml' to setup Ollama in ollama-tll")
    run_ansible_playbook('roles/ollama-gateway/tasks/main.yml')
    
    logging.info("\n--- Pipeline Completed Successfully ---")

if __name__ == "__main__":
    main_pipeline()
