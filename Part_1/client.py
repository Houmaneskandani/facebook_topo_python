import socket
import sys
from thread import *
import getpass
import os
import time

'''
Function Definition
'''

def receiveThread(s):
	while True:
		try:
			reply = s.recv(4096) # receive msg from server
			var = reply
			# You can add operations below once you receive msg
			# from the server

		except:
			print "Connection closed"
			break
	

def tupleToString(t):
	s = ""
	for item in t:
		s = s + str(item) + "<>"
	return s[:-2]

def stringToTuple(s):
	t = s.split("<>")
	return t

'''
Create Socket
'''
try:
	# create an AF_INET, STREAM socket (TCP)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
	print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
	sys.exit();
print 'Socket Created'

'''
Resolve Hostname
'''
host = '10.0.0.4'
port = 5000
try:
	remote_ip = socket.gethostbyname(host)
except socket.gaierror:
	print 'Hostname could not be resolved. Exiting'
	sys.exit()
print 'Ip address of ' + host + ' is ' + remote_ip

'''
Connect to remote server
'''
s.connect((host , port))
print 'Socket Connected to ' + host + ' on ip ' + remote_ip

'''
TODO: Part-1.1, 1.2: 
Enter Username and Passwd
'''
global var
# Whenever a user connects to the server, they should be asked for their username and password.
# Username should be entered as clear text but passwords should not (should be either obscured or hidden). 
# get username from input. HINT: raw_input(); get passwd from input. HINT: getpass()

# Send username && passwd to server

reply = s.recv(1024)
print '~~' + reply + '~~'

uname = raw_input('username: ')
passwd = getpass.getpass('password: ')

data = uname + '<>' + passwd 

try: 	
	s.sendall(data)
except socket.error:
	print 'login error'
	sys.exit()

##reply = s.recv(1024)
##print 'msg recv'

'''
TODO: Part-1.3: User should log in successfully if username and password are entered correctly. A set of username/password pairs are hardcoded on the server side. 
'''
reply = s.recv(5)
if reply == 'valid': # TODO: use the correct string to replace xxx here!

	# Start the receiving thread
	start_new_thread(receiveThread ,(s,))

	message = ""
	while True :
		
		# TODO: Part-1.4: User should be provided with a menu. Complete the missing options in the menu!
		message = raw_input("Choose an option (type the number): \n 1. Logout \n 2. Post a message \n 3. Change password \n")
		
		try :
			# TODO: Send the selected option to the server
			# HINT: use sendto()/sendall()
			if message == str(1):
				s.sendall(message)
				print 'Logout'
				# TODO: add logout operation
				break
			if message == str(2):
				s.sendall(message)
				print 'Enter your message below'
				msg = raw_input( 'message : ')
				s.sendall(msg)
				print 'Message has been send!'	
			if message == str(3):
				s.sendall(message)
				oldpass = getpass.getpass('Old password: ')
				newpass = getpass.getpass('New password: ')
				try:
					s.sendall(oldpass)
					s.sendall(newpass)
				except socket.error:
					print ' couldnt send the inputs'
					sys.exit()
				
				if oldpass == passwd:
					v = 'valid'
				else:
					v = 'nalid'

				if v == 'valid':
					print 'password has been changed successfully!!'
				else:
					print ' Not correct pasword! please try again!'
			# Add other operations, e.g. change password
		except socket.error:
			print 'Send failed'
			sys.exit()
else:
	print 'Invalid username or passwword'

s.close()
