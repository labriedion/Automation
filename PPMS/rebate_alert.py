#!/usr/bin/env python
#get the usage from the "Usage per group" report on ppms.us/Douglas and send an alert for groups 
#who used more than the rebate amount on one microscope this current billing year (August 1st to July 31st)

import requests
import pandas as pd
import win32api

rebateat = 50.0 #rebate at 50 hours, change this to change the rebate

#fetch the microscope usage from PPMS and format it with Pandas
ppms = requests.get("https://ppms.us/douglas/API2/", data={'action': 'Report38', 'dateformat' : 'print', 'outformat': 'json', 'apikey': '(removed for upload)', 'coreid' : 2})
usage = pd.DataFrame(ppms.json())
to_rebate = usage[usage['Used hours'].astype('float64') >= rebateat]
rebates = to_rebate[['Group name','Instrument']]

#get the current ongoing rebates from the log, saved in the current folder
rebates_old = pd.read_csv("rebates.txt") 

#compare the current usage with the ongoing rebates to find the new elements
compare = pd.concat([rebates, rebates_old])
compare = compare.reset_index(drop=True)
compare_gpby = compare.groupby(['Group name','Instrument'])
new_elements = [x[0] for x in compare_gpby.groups.values() if len(x) == 1]

#if there's a new rebate to be activated, send an alert message and save the updated list	
if len(new_elements) != 0:
	new_rebates = compare.reindex(new_elements)
	win32api.MessageBox(0,new_rebates[['Group name', 'Instrument', 'Used hours']].to_csv(), 'REBATES DUE - UPDATE PRICING ON PPMS')
	updated_rebates = compare.drop_duplicates()
	updated_rebates.to_csv("rebates.txt", index = False)
