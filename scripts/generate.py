import json


hosts="""
127.0.0.1	localhost
255.255.255.255	broadcasthost
::1             localhost
"""

with open('machines.json') as json_data:
    d = json.load(json_data)
    json_data.close()

for machine in d:
    host = machine["machineName"] 
    hosts+=f'{machine["ip"]}\t{host}\n'

with open("hosts", "a") as f:
     f.write(hosts)