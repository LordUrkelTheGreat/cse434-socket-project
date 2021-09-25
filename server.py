from socket import *
import sys

serverPort = 11050
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print("RUNNING")

arr = []
# terminalIP = sys.argv[1]


class UserInfo:
    def __init__(self, userName, ipAddr, portNum, state):
        self.userName = userName
        self.ipAddr = ipAddr
        self.portNum = portNum
        self.state = state


def server_register():
    # receive username, ip address, and port number from client
    regName, clientAddress = serverSocket.recvfrom(2048)
    regIP, clientAddress = serverSocket.recvfrom(2048)
    regPort, clientAddress = serverSocket.recvfrom(2048)

    # random boolean statement set to true as default
    valid = True

    # decode username, ip address, and port number
    decodeName = regName.decode()
    decodeIP = regIP.decode()
    decodePort = regPort.decode()
    state = "Free"

    # Truth Value Testing method where the array variable's value is inverted
    # to make the condition true
    if not arr:
        # add decoded information to array via userInfo
        arr.append(UserInfo(decodeName, decodeIP, decodePort, state))
        # print statements
        print(f'Username: {decodeName}')
        print(f'IP Address: {decodeIP}')
        print(f'Port Number: {decodePort}')
        print(f'State: {state}')
        print(f'Values are stored')
        # update return code statement and send it back to client
        returnCode = "SUCCESS"
        serverSocket.sendto(returnCode.encode(), clientAddress)

    # checks if username exists in the array. if it does,
    # then return FAILURE to indicate that register function
    # failed to create new user
    for user in arr:
        if user.userName == decodeName or user.portNum == decodePort:
            returnCode = "FAILURE"
            serverSocket.sendto(returnCode.encode(), clientAddress)
            valid = False

    # checks if valid is true if the above for loop changed it
    if valid == True:
        # add decoded information to array via userInfo
        arr.append(UserInfo(decodeName, decodeIP, decodePort, state))
        # print statements
        print(f'Username: {decodeName}')
        print(f'IP Address: {decodeIP}')
        print(f'Port Number: {decodePort}')
        print(f'State: {state}')
        print(f'Values are stored')
        # update return code statement and send it back to client
        returnCode = "SUCCESS"
        serverSocket.sendto(returnCode.encode(), clientAddress)


def server_setupDHT():
    # receive n and username from client
    setupN, clientAddress = serverSocket.recvfrom(2048)
    setupUserName, clientAddress = serverSocket.recvfrom(2048)

    # random boolean statement set to false by default
    valid = False

    # decode n and username
    decodeN = setupN.decode()
    decodeName = setupUserName.decode()

    for user in arr:
        if user.userName == decodeName and decodeN >= len(arr):
            valid = True


def server_completeDHT():
    print(3)


def server_queryDHT():
    print(4)


def server_leaveDHT():
    print(5)


def server_rebuiltDHT():
    print(6)


def server_deregister():
    print(7)


def server_joinDHT():
    print(8)


def server_teardownDHT():
    print(9)


def server_teardownComplete():
    print(10)


while True:
    # message, clientAddress = serverSocket.recvfrom(2048)
    # modifiedMessage = message.decode().upper()
    # serverSocket.sendto(modifiedMessage.encode(), clientAddress)

    # receives encoded command from client and decodes it
    encodedCommand, clientAddress = serverSocket.recvfrom(2048)
    command = encodedCommand.decode()

    # if the command is from 1-10, it will execute one of the many functions
    if command == "1":
        server_register()
    if command == "2":
        server_setupDHT()
    if command == "3":
        server_completeDHT()
    if command == "4":
        server_queryDHT()
    if command == "5":
        server_leaveDHT()
    if command == "6":
        server_rebuiltDHT()
    if command == "7":
        server_deregister()
    if command == "8":
        server_joinDHT()
    if command == "9":
        server_teardownDHT()
    if command == "10":
        server_teardownComplete()
