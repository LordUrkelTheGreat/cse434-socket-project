from socket import *
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

    # this is used to check if the IPv4 address is valid
    regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
    regexCompile = re.compile(regex)

    # checks if username is an alphabetic string and less than or equal to a length of 15
    # checks if IPv4 address is valid using regex
    # checks if port number is an integer
    if userName.isalpha() and len(userName) <= 15 and re.search(regexCompile, ipAddr) and portNum.isdigit():
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
        # when the conditions of the above if statement isn't met
        print("Invalid input. Try again.")
        exit()


def client_setupDHT():
    # prints setup-dht andthen lets user input n and username that's separated by spaces
    n, userName = input("setup-dht ").rsplit(None, 2)

    # the 2 lets the server know this is the setup-dht command
    clientSocket.sendto("2".encode(), (serverName, serverPort))

    clientSocket.sendto(n.encode(), (serverName, serverPort))
    clientSocket.sendto(userName.encode(), (serverName, serverPort))

    commandMessage, serverAddress = clientSocket.recvfrom(2048)
    print(commandMessage.decode())
    exit()

#client_register()
client_setupDHT()
