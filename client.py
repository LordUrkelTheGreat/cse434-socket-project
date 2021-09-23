from socket import *
from pip._vendor.distlib.compat import raw_input
import re

serverName = '127.0.0.1'
serverPort = 11050
clientSocket = socket(AF_INET, SOCK_DGRAM)

message = raw_input('Input lowercase sentence:')
clientSocket.sendto(message.encode(), (serverName, serverPort))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print(modifiedMessage.decode())
clientSocket.close()


# register <user-name> <IPv4-address> <port>
def client_register():
    print("qwert")


client_register()
