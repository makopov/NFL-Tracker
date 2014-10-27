#!/bin/bash

device='/dev/vda1'
script='harvester.py'

#Run forever
while true
do
	#Check if script is running
	processCount=`ps -x | grep $script | wc -l`
	if [ ${processCount} -gt 1 ]; then
		echo "$script is running"
	else
		#email me
		echo "$script script not runing"
		mail -s "$script stopped execution, attempting a restart" makopov@gmail.com
	fi

	#check disk usage
	let p=`df -k $device | grep -v ^File | awk '{printf ("%i",$3*100 / $2); }'`
	
	if [ $p -ge 90 ]
	then
		df -h $device | mail -s "Low on space" makopov@gmail.com
	fi
	
	sleep 5
done
