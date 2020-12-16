import socket
import sys
from thread import *
import getpass
import os
import time
import datetime
'''
Function Definition
'''

def receiveThread(s):
	while True:
		try:
			reply = s.recv(4096) # receive msg from server
			print reply 
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


'''
TODO: Part-1.3: User should log in successfully if username and password are entered correctly. A set of username/password pairs are hardcoded on the server side. 
'''
reply = s.recv(5)
if reply == 'valid': # TODO: use the correct string to replace xxx here!
	ss = s.recv(4096)
	print ss
	
	''' 
	part2: Please printout the number of unread message once a new client login
	'''
	#ds = s.recv(1024)
	#print ds

	# Start the receiving thread
	start_new_thread(receiveThread ,(s,))

	message = ""
	while True :	
		# TODO: Part-1.4: User should be provided with a menu. Complete the missing options in the menu!
		message = raw_input("Choose an option (type the number): \n 1. Logout \n 2. Send a message \n 3. Change password \n 4. Group Configuration \n 5. Offline message \n 6. Simulate Congestion \n 7. Send Friend Request \n 8. Friend Request \n 9. Friend List \n")
		



		try :
			# TODO: Send the selected option to the server
			# HINT: use sendto()/sendall()
			if message == str(1):
				s.sendall(message)
				print 'Logout'
				# TODO: add logout operation
				break
			
			#==========================================================
			if message == str(2):
				s.sendall(message)
				while True:
					optionmsg = raw_input("Choose an option (type the number): \n 1. Private message \n 2. Broadcast message \n 3. Group message \n")
					try:
						'''
						Part2 : send option to server
						'''
						s.sendall(optionmsg)
						if optionmsg == str(1):
							pmsg = raw_input("Enter your private message\n")
							try:
								'''
								part2: send private message
								'''
								s.sendall(pmsg)
							except socket.error:
								print 'Private Message Send Failed'
								sys.exit()
							rcv_id = raw_input("Enter the recevier ID: \n")
							try:
								'''
								part2: send private message
								'''
								s.sendall(rcv_id)
								break
							except socket.error:
								print 'recv_id send failed'
								sys.exit()

						#====================================================================						
						if optionmsg == str(2):
							bmsg = raw_input("Enter your broadcast message \n")
							try:
								'''
								part2: send broadcast message
								'''
								s.sendall(bmsg)
								break
							except socket.error:
								print 'Broadcast Message Send Failed'
								sys.exit()
						#======================================================================
						if optionmsg == str(3):
							gmsg = raw_input("Enter your group message\n")
							try:
								'''
								part2: send group message
								'''
								s.sendall(gmsg)
							except socket.error:
								print 'Group Message Send Failed'
								sys.exit()

							g_id = raw_input("Enter the Group ID:\n")
							try:
								'''
								part2 : send group message
								'''
								s.sendall(g_id)
								break
							except socket.error:
								print 'g_id Send Failed'
								sys.exit()

					except socket.error:
						print ' Message Send failed'
						sys.exit()


				#s.sendall(message)
				#print 'Enter your message below'
				#msg = raw_input( 'message : ')
				#s.sendall(msg)
				#print 'Message has been send!'	


			#=====================================================================
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
			#=====================================================================
			if message == str(4):
				s.sendall(message)
				option = raw_input("Do you want to: 1. Join Group 2. Quit Group: \n")
				s.sendall(option)
				if option == str(1):
					group = raw_input("Enter the Group you want to join: ")
					s.sendall(group)
					try:
						'''
						part2: Join a particular group
						'''
						#text = s.recv(1024)
						print reply
							
					except socket.error:
						print 'group info send failed'
						sys.exit()
				#===================================================================================
				elif option == str(2):
					group = raw_input("Enter the Group you want to quit: ")
					s.sendall(group)
					try :
						'''
						part2: Quit a particular group
						'''
						#text = s.recv(1024)
						print reply
					except socket.error:
						print 'group info send failed'
						sys.exit()

				else:
					print 'Option not valid'

			#=====================================================================			
			if message == str(5):
				s.sendall(message)
				while not os.getpgrp() == os.tcgetpgrp(sys.stdout.fileno()):
					pass
				option = raw_input("Do you want to: 1. View all offline messages; 2. View only from a particular Group\n")
				s.sendall(option)
				if option == str(1):
					try:
						'''
						part2: view all offline messages
						'''
						#offmsg = s.recv(1024)
						print reply

					except socket.error:
						print 'msg Send Failed'
						sys.exit()
			
				#===================================================================================
				elif option == str(2):
					group = raw_input("Enter the group you want to view the messages from: ")
					s.sendall(group)
					try:
						'''
						part2: view only from a particular group
						'''
						#groupmsg = s.recv(1024)
						print reply

					except socket.error:
						print ' group Send Failed'
						sys.exit()
				else:
					print 'Option not valid'

			#=================================================================
			if message == str(6):
				#s.sendall(message)
				print ' simulate congestion'
				for num in range(1000000):
					s.sendall(message)
					currenttime = datetime.datetime.now()
					s.sendall("From client : " + str(num) + "send at time " + str(currenttime) + "\n")
				

					#newmessg = s.recv(1024)
					#print (newmessg)
				#newm = s.recv(1024)
				#print newm

			#=================================================================
			if message == str(7):
				s.sendall(message)
				print ' send friend request'
				name = raw_input("Enter the id which you want to send friend request to : ")
				s.sendall(name)
				
				g = s.recv(1024)
				print g
				#print reply


			#=================================================================
			if message == str(8):
				s.sendall(message)
				print ' friend request list'
				flist = s.recv(1024)
				print flist
				q = s.recv(1024)
				if q != "nalid":
					post = raw_input( " do you want to accept or reject the request? 1. accept  2. reject ")
					s.sendall(post)
				else:
					s.sendall("nalid")
				q = s.recv(1024)
				print q


			#=================================================================
			if message == str(9):
				print 'friend list : \n'
				a = s.recv(1024)
				print a
				



	
		except socket.error:
			print 'Send failed'
			sys.exit()
else:
	print 'Invalid username or passwword'

s.close()
