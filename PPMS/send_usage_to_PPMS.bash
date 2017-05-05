#!/bin/bash

#This script copies the daily OMERO usage log and the monthly summary to a new folder, then sends the summary to PPMS. Finally, the log and summary files are deleted to track the next month.

dt='date +%Y-%m'
log="/home/omero/Documents/omerospace.log"
archivelog="/home/omero/Documents/OMERO_past_usage/$(date +%Y-%m)_raw.log"
Rsummary="/home/omero/Documents/summary.csv"
archivesum="/home/omero/Documents/OMERO_past_usage/$(date +%Y-%m)_summary.csv"

cp $log $archivelog
cp $Rsummary $archivesum


while read line
do
	userid="$(echo $line | awk -F "," '{print $1}')"
	usage="$(echo $line | awk -F "," '{print $2}')"
	#usagegb=$(bc <<< "scale=2; $usage / 1024")
	
	#(Production url)
	curl -X POST -H "Content-Type: application/x-www-form-urlencoded" -d "apikey=removedforgithubupload&action=createorder&quantity=$usage&accepted=true&completed=true&completeddate=$dt&serviceid=020005&login=$userid" "https://ppms.us/douglas/pumapi/"

	#(test-url)
	#curl -X POST -H "Content-Type: application/x-www-form-urlencoded" -d "apikey=removedforgithubupload&action=createorder&quantity=$usage&accepted=true&completed=true&completeddate=$dt&serviceid=020005&login=$userid" "https://ppms.us/douglas-test/pumapi/"

done < $Rsummary

rm $log
rm $Rsummary
