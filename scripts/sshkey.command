for i in `python3 scripts/getMachineNames.py`
do 
ssh-keyscan $i>> ~/.ssh/known_hosts
done
