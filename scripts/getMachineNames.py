import json
with open("machines.json", "r") as file:
    data=json.load(file)
    print(" ".join(list(map(lambda x: x['machineName'], data))))
   