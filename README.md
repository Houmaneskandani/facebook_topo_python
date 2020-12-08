# facebook_topo_python
## Introduction
  In this project, I use Mininet to emulate a network topology consisting of one server and
three client nodes and implement a simple Facebook application on top of this topology using a
client - server model. Clients run client codes to make use of the capabilities they are provided
with and the server is responsible for authenticating users, receiving posts and messages from
users and sending them to the proper intended recipient. The topology is shown in the picture below:

![alt text](https://github.com/jthak002/fb-python/blob/master/topol.png)

## Run command
 The command for running the topology is: 
 ```sudo mn --custom finalTopol.py --topo mytopo -x```
## Functionality
1. Whenever a user connects to the server, they should be asked for their username and
password.
2. Username should be entered as clear text but passwords should not (should be either
obscured or hidden).
3. User should log in successfully if username and password are entered correctly. A set of
username/password pairs are hardcoded on the server side.
4. User should be provided with a menu. The menu includes all possible options (commands)
user can use and how they can use them. These options include Logout, Change Password,
etc. As you add functionality, you can add new options to this menu.
5. Change Password: User should be able to change their password. To do this, old and new
passwords should be entered (neither as clear text).
6. Logout: User should be able to logout and close their connections with the server.
7. A user should see their messages in real - time (live) if they are online when someone
sends them messages. 
8. Send Message: A user should be able to send a private message to any other user
(whether or not the recipient of the message is online).
9. View Count of Unread Messages: A user should see the number of unread messages when
logging in.
10. Read Unread Messages: A user should be able to read all unread messages.
11. Send Broadcast message: A user should be able to send a message to the server which
only forwards to all clients who are currently connected.
12. List all the available groups: The server should maintain a list of available chat groups. The
user can check the available groups by requesting the server.
13. Request to join the group: A user can request to join in the chat group.
14. Send Group Message: A user in the chat group should be able to send message to all the
users in the group.
15. Quit group: A user in that chat group can choose to quit the group
16. Change TCP: Change the underlying TCP variant to New Reno and CUBIC.
17. Enable/Disable ECN: Enable and disable support for ECN at the switch 1.
18. Simulate congestion: Create congestion in the network using extra ping messages from
clients to server.
19. Measure Response time: Measure response time for different scenarios discussed above.
The response time in this case is the time when a message is sent from a client to the time
when the actual recipient receives it. Provide justification for the difference in response
times for each of them.
