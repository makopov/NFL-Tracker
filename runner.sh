#!/bin/bash

device='/dev/vda1'
script='harvester.py'
email_address='makopov@gmail.com'

bPreviouslyRan=false

#Run forever
while true
do
	#Check if script is running
	processCount=`ps -x | grep $script | wc -l`
	
	if [ ${processCount} -gt 1 ]; then
		#echo "$script is running"
		bPreviouslyRan=true
	else
		#email me
		#echo "$script script not running"
		echo -e "$script stopped execution, attempting a restart" | mail -s "$script is not running" $email_address 
		python $script &
	fi

	#check disk usage
	let p=`df -k $device | grep -v ^File | awk '{printf ("%i",$3*100 / $2); }'`
	
	if [ $p -ge 70 ]
	then
		df -h $device | mail -s "Harvester is low on space" $email_address
	fi
	
	sleep 5
done
