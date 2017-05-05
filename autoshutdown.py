# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 09:22:41 2017

@author: Étienne Labrie-Dion

Autoshutdown is an IoT routine that checks whether a batch scan was performed under the Autosthudown account of the Olympus VS120 Slide Scanner. If so, it will perform an automatic shutdown of the system, first by remotely shutting down the computer, then by cutting off power from all components using an mPower Pro Ethernet-connected powerstrip.
"""

import time
from datetime import datetime
import os
import paramiko
import subprocess


def read_email(): #Open the latest email in the mail folder and detect when a batch scan is finished
    
    #open the newest email
    os.chdir("C:\inetpub\mailroot\Drop")
    newestmail = max(os.listdir("."), key = os.path.getctime)
    fp = open(newestmail)
    email = fp.readlines()
    fp.close()
    
    #get the date and status of the scan from the email
    timeFormat = "%Y-%m-%d %H:%M:%S"
    todayTime = time.strftime(timeFormat)
    scanTime = email[-3][0:19]
    scanState = email[-2][-21:-1]
    scanUser = email[-2][27:-23]
    
    #measure the time between the end of the scan and now
    diff = datetime.strptime(todayTime, timeFormat) - datetime.strptime(scanTime, timeFormat)
    minutesPassed = diff.seconds/60
     
    #If the mail says there's a batch scan finished from Autoshutdown that finished in the last 15 min,
    #then turn off the computer and the components of the slide scanner 
    if scanState == "Batch Scan finished." and scanUser == "Autoshutdown" and minutesPassed < 15:
        turn_off_cpu()
        
        #wait 6 minutes for computer to shut down safely (although it's not controller by the mPower)
        #with this delay, we also avoid the script running twice on the same batch since it runs every 10 minutes only
        time.sleep(360)        
        ssh = mPower_connect()
        mPower_turn_off(ssh)

def turn_off_cpu():
    #turn off the slide scanner computer
    cmd = 'shutdown /m \\CPUNAMEREMOVEDFORUPLOAD /s /f /c “The slide scanner will shutoff in a few minutes, please save all work.” /t 120'
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

#set-up the SSH connection       
def mPower_connect():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('IPADDRESSREMOVEDFORUPLOAD', username = 'REMOVEDFORUPLOAD', password = 'REMOVEDFORUPLOAD')
    return ssh
    
#turn off all the ports
def mPower_turn_off(ssh):
    for port in range(1,9):
        stdin, stdout, stderr = ssh.exec_command("echo 0 > /proc/power/relay%d" %port)
    
#turn on all the ports (not used in the current routine)
def mPower_turn_on(ssh):
    for port in range(1,9):
        stdin, stdout, stderr = ssh.exec_command("echo 1 > /proc/power/relay%d" %port)

if __name__ == "__main__":
    read_email()
