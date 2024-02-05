## Command
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
