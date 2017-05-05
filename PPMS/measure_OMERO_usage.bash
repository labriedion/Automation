#!/bin/bash

#This script extracts the folder size of OMERO's Managed Repository, strips out the PPMS user names and saves everything in a log file like this: DATE USERNAME SIZE

dt=`date +%F`
log="/home/omero/Documents/omerospace.log"
repo="/omerohd/OMERO/ManagedRepository/*"

du -s $repo > /tmp/omerodu.txt

while read line
do
	echo -n "$dt " >> $log		
		echo -n $line | grep -Po 'ManagedRepository/\K[^_]+' | tr -d "\n" >> $log
		echo -n $line | awk '{print " " $1}' >> $log
		
done < /tmp/omerodu.txt

rm /tmp/omerodu.txt
