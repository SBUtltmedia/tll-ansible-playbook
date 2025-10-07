import json

def generate_hosts_file():
    hosts = """127.0.0.1	localhost\n255.255.255.255	broadcast\nhost::1             localhost\n"""

    with open('scripts/machines.json') as json_data:
        d = json.load(json_data)
        json_data.close()

    for machine in d:
        if machine["machineName"] != "router":
            host = machine["machineName"] 
            hosts+=f'{machine["ip"]}\t{host}\n'

    with open("scripts/hosts", "w") as f:
        f.write(hosts)
