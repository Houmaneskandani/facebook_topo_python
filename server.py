import socket
import sys
from thread import *
import time

'''
Function Definition
'''
def tupleToString(t):
	s=""
	for item in t:
		s = s + str(item) + "<>"
	return s[:-2]

def stringToTuple(s):
	t = s.split("<>")
	return t

'''
Create Socket
'''
HOST = ''	# Symbolic name meaning all available interfaces
PORT = 5000	# Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print 'Socket created'

'''
Bind socket to local host and port
'''
try:
	s.bind((HOST, PORT))
except socket.error , msg:
	print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()
print 'Socket bind complete'

'''
Start listening on socket
'''
s.listen(10)
print 'Socket now listening'

'''
Define variables:
username && passwd
message queue for each user
'''
clients = []
# TODO: Part-1 : create a var to store username && password. NOTE: A set of username/password pairs are hardcoded here. 
# e.g. userpass = [......]
messages = [[],[],[]]
count = 0
usrconn = 0
uname = ''
exist = ''
userpass = []
#userpass = [["user1", "passwd1"], ["user2", "passwd2"], ["user3", "passwd3"]]
subscriptions = [[],[],[]] # store the group info
vld = '0'
offmessage = []
online = []
connid = []
message = []
availablegroup = []
groupnames = ["study group","friends group", "gaming group"]
groupwidconn =[] # group name , id , conn
offgroupmessages = [] # group name, id , data
'''
Function for handling connections. This will be used to create threads
'''
def clientThread(conn):
	global clients
	global count
	# Tips: Sending message to connected client
	conn.send('Welcome to the server. Type your username and password and hit enter\n') #send only takes string
	rcv_msg = conn.recv(1024)
	rcv_msg = stringToTuple(rcv_msg)
	if rcv_msg in userpass:
		user = userpass.index(rcv_msg)
		print (str(user))
		print rcv_msg[0]	
		try :
			conn.sendall('valid')
			online.append(rcv_msg[0])
			connid.append([rcv_msg[0], conn])
			print connid
			print online
		except socket.error:
			print 'Send failed'
			sys.exit()
	
		'''
		Part2 :
		after the user logs in, check the unread message for this user.
		Return the number of the unread messges to this user
		'''		
		count = 0
		for ms in offmessage:
			for name in ms:
				if name == rcv_msg[0]:
					count = count + 1
		
		for ds in offgroupmessages:
			for names in ds:
				if names == rcv_msg[0]:
					count = count + 1
		
		unreadmsg =  "You have " + str(count) + " unread messages. "
		conn.sendall(unreadmsg)	
			
		# Tips: Infinite loop so that function do not terminate and thread do not end.
		while True:		

			try :
				option = conn.recv(1024)
			except:
				break

			if option == str(1):
				print 'user loged out'
				# TODO: Part-1: Add the logout processing here
				conn.close()
				connid.remove([rcv_msg[0], conn])
				online.remove(rcv_msg[0])
				if conn in clients:
					clients.remove(conn)
				
			# =============================================
			elif option == str(2):
				print 'Post a message'
				op = conn.recv(1024)
				if op == str(1):
					'''
					pert2: send private message

					'''
					msg = conn.recv(1024)
					usrid = conn.recv(1024)
					# search for conn of the user
					#nusrid = ["usrid"]
					if not usrid in online:
						msg = "Message from " + rcv_msg[0] + " : " + msg + " \n"
						offmessage.append([usrid,msg])
						print " detected"

					else:
						for i in range(len(connid)):
							for j in range(len(connid[i])):
								if connid[i][j] == usrid:
									usrconn =  connid[i][j+1]
		
						# send msg to that user
						msg = "Message from " + rcv_msg[0] + " : " + msg
						usrconn.sendall(msg)

				if op == str(2):
					'''
					part2: send broadcast message
					'''
					print ' option2 broadcast'
					data = conn.recv(1024)
					data = "Message from " + rcv_msg[0] + " : " + data
					#send msg to all users
					for i in range(len(connid)):
						usrconn = connid[i][1]
						usrconn.sendall(data)

				if op == str(3):
					'''
					part2: send group message
					'''
					print ' option 3 group msg'
					data = conn.recv(1024)
					data = "Message from " + rcv_msg[0] + " : " + data + " \n "
					grpid = conn.recv(1024)
					
					for i in range(len(groupwidconn)):
						if groupwidconn[i][0] == grpid :
							if not groupwidconn[i][2] in clients:
								offgroupmessages.append([grpid,groupwidconn[i][1],data])
								print " message send"
							else:
								usrconn = groupwidconn[i][2]
								usrconn.sendall(data)

			# =============================================
			elif option == str(3):
				print 'change password'
				try:
					oldPass = conn.recv(1024)
					newPass = conn.recv(1024)
				except socket.error:
					print ' not recv'
					sys.exit()

				old = rcv_msg[1]
				usernm = rcv_msg[0]
				
				if oldPass == old:
					print 'it matched and send valid'
					userpass.remove([usernm, old])
					userpass.append([usernm, newPass])
					conn.sendall('valid')
					print 'pass changed successfully!!!' 
				else:
					conn.sendall('nalid')
					print 'Wrong password'

			# ==============================================
			elif option == str(4):
				'''
				part2: join or quit group
				'''
				op = conn.recv(1024)
			
				if op == str(1):
					gid = conn.recv(1024)
					#is gid exist?
					if gid in groupnames:
						 exist = 'false'
						# check if already join
						 for i in range(len(groupwidconn)):
							for j in range(len(groupwidconn[i])):
								if groupwidconn[i][j] == rcv_msg[0]:
									exist = "true"
				        
						 if exist == "false":
							# go head and add 
							groupwidconn.append([gid,rcv_msg[0],conn])
						 	conn.sendall('you have successfully joined the group')
						 else:
							conn.sendall('You already joined this group') 
					else:
						# there is no group name as gid
						conn.sendall('there is no group id found')					
				elif op == str(2):
					gid = conn.recv(1024)
					#id gid exist?
					if gid in groupnames:
						exist = 'false'
						#check is user already joined
						for i in range(len(groupwidconn)):
							if groupwidconn[i][0] == gid :
								if groupwidconn[i][1] == rcv_msg[0] :
									groupwidconn.remove([gid,rcv_msg[0],conn])
									conn.sendall('you have been removed from this group')
								else:
									print ' not found'
						 	else:
								conn.sendall('group does not exist or you have not joined the group yet')
								
					else:
						conn.sendall('the group does not exist!')
	
				else:
					try:
						conn.sendall('Option not valid')
					except socket.error:
						print "Option not valid dailed"
						sys.exit()

			#==============================================
			elif option == str(5):
				'''
				part2: Read offline message
				'''
				op = conn.recv(1024)
				
				if op == str(1):
					if len(offmessage) != 0:
						for i in range(len(offmessage)):
							for j in range(len(offmessage[i])):
								if offmessage[i][j] == rcv_msg[0]:
									offmsg =  offmessage[i][j+1]
									conn.sendall(offmsg)
									offmessage.remove([rcv_msg[0],offmessage[i][1]])
					else:
						conn.sendall('there is no message available')
		
				elif op == str(2):
					groupid = conn.recv(1024)
					if len(offgroupmessages) != 0:
 						for i in range(len(offgroupmessages)):
							for j in range(len(offgroupmessages[i])):
								if offgroupmessages[i][j] == rcv_msg[0]:
									offmsg = offgroupmessages[i][2]
									conn.sendall(offmsg)
									offgroupmessages.remove([groupid,rcv_msg[0],offgroupmessages[i][2]])

					else:
						conn.sendall(' there is no message availble')


				else:
					try:
						conn.sendall('Option not valid')
					except socket.error:
						print 'option not valid send failed'
						sys.exit()
			#==============================================
			else:
				try :
					conn.sendall('Option not valid')
				except socket.error:
					print 'option not valid Send failed'
					conn.close()
					clients.remove(conn)
	else:
		try :
			conn.sendall('nalid')
		except socket.error:
			print 'nalid Send failed'
	print 'Logged out'
	conn.close()
	if conn in clients:
		clients.remove(conn)

def receiveClients(s):
	global clients
	while 1:
		# Tips: Wait to accept a new connection (client) - blocking call
		conn, addr = s.accept()
		print 'Connected with ' + addr[0] + ':' + str(addr[1])
		clients.append(conn)
		# Tips: start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
		start_new_thread(clientThread ,(conn,))

start_new_thread(receiveClients ,(s,))

'''
main thread of the server
print out the stats
'''
while 1:
	message = raw_input()
	if message == 'messagecount':
		print 'Since the server was opened ' + str(count) + ' messages have been sent'
	elif message == 'usercount':
		print 'There are ' + str(len(clients)) + ' current users connected'
	elif message == 'storedcount':
		print 'There are ' + str(sum(len(m) for m in messages)) + ' unread messages by users'
	elif message == 'newuser':
		user = raw_input('User:\n')
		password = raw_input('Password:')
		userpass.append([user, password])
		messages.append([])
		offmessage.append([])
		subscriptions.append([])
		print 'User created'
	elif message == 'listgroup':
		'''
		part2: implement the functionality to list all the available groups
		'''
		for i in range(len(groupnames)):
			availablegroup.append(groupnames[i])
			print str(i+1) + " : " + availablegroup[i]

s.close()

