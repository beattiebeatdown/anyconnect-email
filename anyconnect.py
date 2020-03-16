#!/usr/bin/env python
import paramiko
import time
import sys
import datetime
import os
import smtplib

server=smtplib.SMTP('SMTP SERVER ADDRESS',25)
server.ehlo()
server.login("EMAILUSERNAME","EMAILPASSWORD")

remote_conn_pre = paramiko.SSHClient()
remote_conn_pre.set_missing_host_key_policy(
paramiko.AutoAddPolicy())
password1=os.environ.get('ENV_PW')
#password is set within the is environment variables
remote_conn_pre.connect('IPADDRESS', username='USERNAME', password=password1,allow_agent=False,look_for_keys=False)
print "SSH connection established"

remote_conn = remote_conn_pre.invoke_shell()
password2 = os.environ.get('ENV_PW')
#password is set within the is environment variables
time.sleep(1)
ssh_login1 = remote_conn.recv(50000)
if ">" in ssh_login1:
    print "We are in the fierwall "
else:
    print " Straight to enable mode we go....."
    time.sleep(1)

remote_conn.send("en \n")
time.sleep(2)
remote_conn.send(password2)
remote_conn.send("\n")
time.sleep(2)
ssh_login2 = remote_conn.recv(50000)
if "#" in ssh_login2:
    print "We are in enable mode "
    time.sleep(1)
####################################################################################
timenow = (datetime.datetime.now())
remote_conn.send('terminal page 0\n')
remote_conn.send("show vpn-sessiondb anyconnect sort name | i Username\n")
time.sleep(1)
output1 = remote_conn.recv(50000)
print output1
useroutput1 = output1.split('\n')
emailvar=""
for user in useroutput1:
	if 'HOSTNAME' in user: #Add in hostname of the ASA
		continue
	if 'terminal' in user:
		continue
	else:
		userfinal1 = user.split()
		emailvar = emailvar + userfinal1[2] + '\n'
		print userfinal1[2]
remote_conn.send('show vpn-sessiondb summary | i Any\n')
time.sleep(1)
output2 = remote_conn.recv(500)
output3 = output2.split()
finalnumber = output3[9]
print 'THE TOTAL NUMBER OF ANYCONNECT USERS - ' + finalnumber
timeemail= timenow.strftime("%H:%M:%S")
subject='ENTER SUBJECT HERE'
message='TIME - '+timeemail+'\n'+'THE TOTAL NUMBER OF ANYCONNECT USERS - ' + finalnumber+'\n'+emailvar
msg='Subject: {}\n\n{}'.format(subject, message)
server.sendmail("FRON_EMAIL","TO_EMAIL",msg)
print 'Email sent'
print '#######################################################'
server.close()
