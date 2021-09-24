from socket import *
from pip._vendor.distlib.compat import raw_input
import re

serverName = '127.0.0.1'
serverPort = 11050
clientSocket = socket(AF_INET, SOCK_DGRAM)


# message = raw_input('Input lowercase sentence:')
# clientSocket.sendto(message.encode(), (serverName, serverPort))
# modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
# print(modifiedMessage.decode())
# clientSocket.close()


# register <user-name> <IPv4-address> <port>
def client_register():
    # prints register and then lets user input 3 strings separated by spaces
    userName, ipAddr, portNum = input("register ").rsplit(None, 2)

    if userName.isalpha() and len(userName) <= 15:
        # the 1 lets server know this is a register command
        clientSocket.sendto("1".encode(), (serverName, serverPort))

        # send username, ip address, and port number to server
        clientSocket.sendto(userName.encode(), (serverName, serverPort))
        clientSocket.sendto(ipAddr.encode(), (serverName, serverPort))
        clientSocket.sendto(portNum.encode(), (serverName, serverPort))

        # command message returned and printed
        commandMessage, serverAddress = clientSocket.recvfrom(2048)
        print(commandMessage.decode())
        exit()
    else:
        # when the conditions of the above if statement isnt met
        print("Invalid input. Try again.")
        exit()


# input1 = list(map(str, input().split()))
# if input1[0] in 'register':
client_register()
