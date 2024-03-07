## How to setup new computer
- delete scripts/hosts file
- run scripts/sshkey.command to get fingerprints of all all machines
- update scripts/machines.json and inventory.ini to include the new machine
- run python3 generate.py to generate hosts file
- run python3 pushScript.py <tltmeida's passwords> to push checkForXcodeCLI.command to /Users/Shared directory of each machine
- On remote machine, run checkForXcideCL.command to install xcode-select tool which is used by ansible
- run ansible-playbook -i inventory.ini setup.yml -Kk which ask you to input tltmedia's password to twice. One for ssh connection and the other for sudo
-  ansible-playbook -i inventory.ini install-softwares.yml -k to use brew to install softwares
- On remote machine, run makemeadmin.sh in /Users/Shared to make you admin 

## What does setup.yml do
This playbook first renames the computer to its code name e.g riley, huey. Then sets the permissions for brew. It sends makemeadmin.sh, hosts,and sudoers file to the remote machines. Finally it installs brew.

## What does each file inside scripts do
- sudoers is the sudoers file that will be put to the new remote machine. It gives a standard user privilgies to run sudo deseditgroup without an admin's passwords

- makemeadmin.sh makes a ordinary user admin (need to reboot to sync the change on settings page)

## Command to run ansible
tltmedia is the default admin account 
run with command
```
 ansible-playbook -i inventory.ini <playbook name> -Kk
```
It will prompt you to enter tltmedia account's password and sudo password for tltmedia

## Create Inventroy

List Host Address of all computers into the ``` inventory.ini``` file

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
