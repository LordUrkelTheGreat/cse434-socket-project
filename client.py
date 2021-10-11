from socket import *
import re
import sys

# this is used to check if the IPv4 address is valid
regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
regexCompile = re.compile(regex)

clientSocket = socket(AF_INET, SOCK_DGRAM)
commandInput = ""
firstRegister = False
commandNum = ""

# do not delete
serverName = sys.argv[1]
serverPort = int(sys.argv[2])

# this is for running on PC not asu general
# serverName = '127.0.0.1'
# serverPort = 11000

if serverPort < 11000 or serverPort > 11500:
    print("Error: Port number must be in the range of 11000-11500")
    exit()

if re.search(regexCompile, serverName) is None:
    print("Error: IP address must be IPv4 dotted decimal notation")
    exit()


# register <user-name> <IPv4-address> <port>
def client_register():
    # stores indices from command input to username, ip address, and port number
    userName = commandInput[1]
    ipAddr = commandInput[2]
    portNum = commandInput[3]

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
        print("Error: Username must only contain alphabets, username length must be less than or equal to 15 "
              "characters, IPv4 address is incorrect, or the port number is not a digit")


def client_setupDHT():
    # stores indices from command input to n and username
    n = commandInput[1]
    userName = commandInput[2]

    # the 2 lets the server know this is the setup-dht command
    clientSocket.sendto("2".encode(), (serverName, serverPort))

    # sends the n and username to server
    clientSocket.sendto(n.encode(), (serverName, serverPort))
    clientSocket.sendto(userName.encode(), (serverName, serverPort))

    # command message returned and printed
    commandMessage, serverAddress = clientSocket.recvfrom(2048)
    print(commandMessage.decode())

    # returns a list of n users that will construct the DHT
    print(f'List of {n} users that will construct the DHT')


def client_completeDHT():
    # command input is stored into username
    userName = commandInput[1]

    # the 3 lets the server know this is the complete command
    clientSocket.sendto("3".encode(), (serverName, serverPort))

    # sends the username to the server
    clientSocket.sendto(userName.encode(), (serverName, serverPort))

    # command message returned and printed
    commandMessage, serverAddress = clientSocket.recvfrom(2048)
    print(commandMessage.decode())


def client_queryDHT():
    # command input is stored into username
    userName = commandInput[1]

    # the 4 lets the server know this is the query command
    clientSocket.sendto("4".encode(), (serverName, serverPort))

    # sends the username to the server
    clientSocket.sendto(userName.encode(), (serverName, serverPort))

    # server sends client random user in DHT
    randomUser, serverAddress = clientSocket.recvfrom(2048)
    print(randomUser.decode())

    # send long name of country to server
    longNameInput = input("Enter long name of country to query: ")
    clientSocket.sendto(longNameInput.encode(), (serverName, serverPort))

    # server sends back record
    recordTable, serverAddress = clientSocket.recvfrom(2048)
    print(recordTable)

    # command message returned and printed
    commandMessage, serverAddress = clientSocket.recvfrom(2048)
    print(commandMessage.decode())


def client_leaveDHT():
    # fix client_queryDHT() cause return code statement is buggy
    # prints the return code correctly but does the user input as if code works fine

    # command input is stored into username
    userName = commandInput[1]

    # the 5 lets the server know this is the leave dht command
    clientSocket.sendto("5".encode(), (serverName, serverPort))

    # sends the username to the server
    clientSocket.sendto(userName.encode(), (serverName, serverPort))

    # command message returned and printed
    commandMessage, serverAddress = clientSocket.recvfrom(2048)
    print(commandMessage.decode())


def client_rebuiltDHT():
    # command input 1 is stored intousername
    userName = commandInput[1]

    # command input 2 is stored into new Leader
    newLeader = commandInput[2]

    # the 6 lets the server know this is the rebuilt command
    clientSocket.sendto("6".encode(), (serverName, serverPort))

    # sends the old username and new username to server
    clientSocket.sendto(userName.encode(), (serverName, serverPort))
    clientSocket.sendto(newLeader.encode(), (serverName, serverPort))

    # command message returned and printed
    commandMessage, serverAddress = clientSocket.recvfrom(2048)
    print(commandMessage.decode())


def client_deRegister():
    # command input is stored into username
    userName = commandInput[1]

    # the 7 lets the server know this is the de-register command
    clientSocket.sendto("7".encode(), (serverName, serverPort))

    # sends the username to the server
    clientSocket.sendto(userName.encode(), (serverName, serverPort))

    # command message returned and printed
    commandMessage, serverAddress = clientSocket.recvfrom(2048)
    print(commandMessage.decode())


def client_joinDHT():
    # command input is stored into username
    userName = commandInput[1]

    # the 8 lets the server know this is the join command
    clientSocket.sendto("8".encode(), (serverName, serverPort))

    # sends the username to the server
    clientSocket.sendto(userName.encode(), (serverName, serverPort))

    # command message returned and printed
    commandMessage, serverAddress = clientSocket.recvfrom(2048)
    print(commandMessage.decode())


while True:
    print()
    print("Please enter command")
    commandInput = list(map(str, input().split()))

    if commandInput[0] == "register":
        firstRegister = True
        commandNum = "1"
        client_register()
    elif commandInput[0] == "setup-dht" and firstRegister is True:
        commandNum = "2"
        client_setupDHT()
    elif commandInput[0] == "dht-complete" and firstRegister is True:
        commandNum = "3"
        client_completeDHT()
    elif commandInput[0] == "query-dht" and firstRegister is True:
        commandNum = "4"
        client_queryDHT()
    elif commandInput[0] == "leave-dht" and firstRegister is True:
        commandNum = "5"
        client_leaveDHT()
    elif commandInput[0] == "dht-rebuilt" and firstRegister is True:
        commandNum = "6"
        client_rebuiltDHT()
    elif commandInput[0] == "deregister" and firstRegister is True:
        commandNum = "7"
        client_deRegister()
    elif commandInput[0] == "join-dht" and firstRegister is True:
        commandNum = "8"
        client_joinDHT()
    else:
        print("Please enter command correctly or use the register command first.")
