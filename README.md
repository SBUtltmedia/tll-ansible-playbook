## How to setup new computer
1. Prepare the host file:
    Delete the existing scripts/hosts file. Run python3 scripts/generate.py to generate new hosts file
    Update scripts/machines.json and inventory.ini to add the new machine's information.
    Run scripts/sshkey.command to gather SSH fingerprints for all machines.
   
2. Push a script to remote machines:
    Run python3 scripts/pushScript.py <tltmedia's password> to send checkForXcodeCLI.command to the /Users/Shared directory on each machine.

3. Install a tool on remote machines:
    On each remote machine, manually execute checkForXcodeCLI.command to install the xcode-select tool, which is required for Ansible.

4. Run Ansible playbooks:
    Run ansible-playbook -i inventory.ini setup.yml -Kk. This will prompt you for tltmedia's password twice (once for SSH connection and once for sudo).

5. Gain admin privileges on remote machines:
    On each remote machine, manually execute makemeadmin.sh located in /Users/Shared to elevate the current user's privileges to admin.

6. Install packages and apps on the new machine through brew
   Run ansible-playbook -i inventory.ini install-softwares.yml -k

## What does setup.yml do
This playbook first renames the computer to its code name e.g riley, huey. Then sets the permissions for brew. It sends makemeadmin.sh, hosts,and sudoers file to the remote machines. Finally it installs brew. 

## What do scripts inside /scripts do
- sudoers is the sudoers file that will be put to the new remote machine. It gives a standard user  the privilgie to run sudo deseditgroup without an admin's passwords

- makemeadmin.sh makes a ordinary user admin (need to reboot to sync the change on settings page)

- getMachineName.py feeds sshkey.command names of the machines for it scan for ssh fingerprint

## Command to run ansible
tltmedia is the default admin account. inventory.ini specifies the machines ansible will connect to. 
run with command
```
 ansible-playbook -i inventory.ini <playbook name> -Kk
```
It will prompt you to enter tltmedia account's password and sudo password for tltmedia

## Create Inventroy

List Host Address of all computers into the ``` inventory.ini``` file. Edit inventory file by add or remove machine names from localhosts list

## Create playbook

All playbook starts with
```
---
- name: 
  hosts: 
  become: 

```

name is the playbook name.
host is the hosts in inventory.ini
become: true enable sudo on controlled node

task is the task to be run on each machine. consulate https://docs.ansible.com/ansible/latest/collections for list of supported operations
