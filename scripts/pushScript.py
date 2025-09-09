import paramiko
import json
import sys
import os
import logging

os.path.dirname(os.path.abspath(__file__))

def run_command_over_ssh(hostname, username, key_file, command):
    """
    Connects to a remote machine via SSH and executes a command using a key file.
    Logs success, output, and any errors encountered.

    Args:
        hostname (str): The IP address or hostname of the machine.
        username (str): The user ID for SSH login.
        key_file (str): The path to the private SSH key file.
        command (str): The shell command to execute.
    """
    ssh_client = paramiko.SSHClient()
    # Automatically add the server's host key. For a more secure approach,
    # you would manage known hosts.
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    logging.info(f"Attempting to connect to {hostname} using key file...")
    try:
        ssh_client.connect(
            hostname=hostname,
            username=username,
            key_filename=key_file,
            timeout=10
        )
        logging.info(f"Successfully connected to {hostname}.")

        # Execute the command
        logging.info(f"Executing command: '{command}' on {hostname}...")
        stdin, stdout, stderr = ssh_client.exec_command(command)
        
        # Read the command's output
        stdout_output = stdout.read().decode('utf-8').strip()
        stderr_output = stderr.read().decode('utf-8').strip()

        # Log the output and errors
        if stdout_output:
            logging.info(f"--- Standard Output for {hostname} ---")
            logging.info(stdout_output)
            logging.info(f"--- End Standard Output ---")
        
        if stderr_output:
            logging.error(f"--- Standard Error for {hostname} ---")
            logging.error(stderr_output)
            logging.error(f"--- End Standard Error ---")
            
        logging.info(f"Command execution on {hostname} completed.")

    except paramiko.AuthenticationException:
        logging.error(f"Authentication failed for {hostname}. Please check username and key file.")
    except paramiko.SSHException as ssh_err:
        logging.error(f"SSH error on {hostname}: {ssh_err}")
    except FileNotFoundError:
        logging.error(f"SSH key file not found at path: {key_file}. Please ensure the path is correct.")
    except Exception as e:
        logging.error(f"Could not connect to or execute command on {hostname}. Error: {e}")
    finally:
        # Close the connection whether it was successful or not
        if 'ssh_client' in locals() and ssh_client:
            ssh_client.close()
        logging.info(f"Connection to {hostname} closed.\n")


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
            print("Runing command")
            run_command_over_ssh(ip, "tltmedia", "key.pem", "./Users/Shared/checkForXcodeCLI.command")
    except Exception as e:
        print(f"Could not copy over {host}: {e}")
