for i in `python3 getMachineNames.py`
do 
ssh-keyscan $i>> ~/.ssh/known_hosts
done
