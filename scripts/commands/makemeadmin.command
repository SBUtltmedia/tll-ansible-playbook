# run with ./makemeadmin.sh


currentUser=$(who | awk '/console/{print $1}')
echo $currentUser

sudo /usr/sbin/dseditgroup -o edit -a $currentUser -t user admin

if groups $currentUser | grep -q -w admin;
then 
    echo "Is admin now"; 
else 
    echo "Not an admin"; 
fi
