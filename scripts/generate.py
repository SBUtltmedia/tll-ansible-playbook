import json

def generate_hosts_file():
    hosts = """
    127.0.0.1	localhost
    255.255.255.255	broadcasthost
    ::1             localhost
    """

    with open('scripts/machines.json') as json_data:
        d = json.load(json_data)
        json_data.close()

    for machine in d:
        host = machine["machineName"] 
        hosts+=f'{machine["ip"]}\t{host}\n'

    with open("scripts/hosts", "a+") as f:
        f.write(hosts)
