from socket import *
import re
import sys

serverName = '127.0.0.1'
serverPort = 11050
clientSocket = socket(AF_INET, SOCK_DGRAM)

commandInput = ""
firstRegister = False
# do not delete
# terminalIP = sys.argv[1]
# terminalPort = sys.argv[2]


# message = raw_input('Input lowercase sentence:')
# clientSocket.sendto(message.encode(), (serverName, serverPort))
# modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
# print(modifiedMessage.decode())
# clientSocket.close()


# register <user-name> <IPv4-address> <port>
def client_register():
    # stores indices from command input to username, ip address, and port number
    userName = commandInput[1]
    ipAddr = commandInput[2]
    portNum = commandInput[3]

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
    else:
        # when the conditions of the above if statement isn't met
        print("Invalid input. Try again.")


def client_setupDHT():
    # stores indices from command input to n and username
    n = commandInput[1]
    userName = commandInput[2]

    # the 2 lets the server know this is the setup-dht command
    clientSocket.sendto("2".encode(), (serverName, serverPort))

    clientSocket.sendto(n.encode(), (serverName, serverPort))
    clientSocket.sendto(userName.encode(), (serverName, serverPort))

    commandMessage, serverAddress = clientSocket.recvfrom(2048)
    print(commandMessage.decode())


while True:
    print("Please enter command")
    commandInput = list(map(str, input().split()))

    if commandInput[0] == "register":
        firstRegister = True
        client_register()
    elif commandInput[0] == "setup-dht" and firstRegister == True:
        client_setupDHT()
    else:
        print("Please enter command correctly or use the register command first.")
