from socket import *
import threading
import sys

dht = []
lockout = []
processing = []
arrayStorage = []

# do not delete
serverPort = int(sys.argv[1])

# this is for running on PC not asu general
# serverPort = 11000

if serverPort < 11000 or serverPort > 11499:
    print("Error: Port number must be in the range of 11000-11500")
    exit()

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print(serverSocket.getsockname())
print("RUNNING")


class UserInfo:
    def __init__(self, userName, ipAddr, portNum, state):
        self.userName = userName
        self.ipAddr = ipAddr
        self.portNum = portNum
        self.state = state


class DHT:
    def __init__(self, countryCode, shortName, tableName, longName, twoAlphaCode, currencyUnit, region, wb2Code,
                 latestPopulationCensus):
        self.countryCode = countryCode
        self.shortName = shortName
        self.tableName = tableName
        self.longName = longName
        self.twoAlphaCode = twoAlphaCode
        self.currencyUnit = currencyUnit
        self.region = region
        self.wb2Code = wb2Code
        self.latestPopulationCensus = latestPopulationCensus


def server_register():
    # receive username, ip address, and port number from client
    regName, clientAddressRegister = serverSocket.recvfrom(2048)
    regIP, clientAddressRegister = serverSocket.recvfrom(2048)
    regPort, clientAddressRegister = serverSocket.recvfrom(2048)

    # random boolean statement set to true as default
    # valid = True
    valid1 = False

    # decode username, ip address, and port number
    decodeName = regName.decode()
    decodeIP = regIP.decode()
    decodePort = regPort.decode()
    state = "Free"

    # Truth Value Testing method where the array variable's value is inverted
    # to make the condition true
    if not arrayStorage:
        # add decoded information to array via userInfo
        arrayStorage.append(UserInfo(decodeName, decodeIP, decodePort, state))
        # print statements
        print(f'Username: {decodeName}')
        print(f'IP Address: {decodeIP}')
        print(f'Port Number: {decodePort}')
        print(f'State: {state}')
        print(f'Values are stored')
        valid1 = True
        # update return code statement and send it back to client
        returnCode = "SUCCESS: User registered"
        serverSocket.sendto(returnCode.encode(), clientAddressRegister)

    # checks if username exists in the array. if it does,
    # then return FAILURE to indicate that register function
    # failed to create new user
    if valid1 is False:
        for user in arrayStorage:
            if user.userName == decodeName or user.portNum == decodePort:
                returnCode = "FAILURE: Username already exists or port number is already in use"
                serverSocket.sendto(returnCode.encode(), clientAddressRegister)
                # valid = False
                break


def server_setupDHT():
    # receive n and username from client
    setupN, clientAddressSetUp = serverSocket.recvfrom(2048)
    setupUserName, clientAddressSetUp = serverSocket.recvfrom(2048)

    # random boolean statement set to false by default
    valid = True

    # decode n and username
    decodeN = setupN.decode()
    decodeName = setupUserName.decode()

    if lockout:
        returnCode = "FAILURE"
        serverSocket.sendto(returnCode.encode(), clientAddressSetUp)
    else:
        if valid:
            file = open("StatsCountry.csv", "r")

            for f in file:
                line = file.readline()
                data = line.split(",")
                if len(data) > 1:
                    dht.append(
                        DHT(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8].rstrip()))

            for user in arrayStorage:
                if user.userName == decodeName:
                    user.state = "LEADER"
                    lockout.append(1)


def server_completeDHT():
    # receive username from client
    completeUserName, clientAddressComplete = serverSocket.recvfrom(2048)

    # random boolean statement set to false by default
    valid = True

    # decode username
    decodeName = completeUserName.decode()

    for user in arrayStorage:
        if user.state == "LEADER" and user.userName == decodeName:
            if dht:
                valid = True
            else:
                returnCode = "FAILURE: DHT not setup"
                serverSocket.sendto(returnCode.encode(), clientAddressComplete)
                valid = False
        else:
            returnCode = "FAILURE: User is not the leader or User isn't registered"
            serverSocket.sendto(returnCode.encode(), clientAddressComplete)
            valid = False

    if valid is True:
        returnCode = "SUCCESS"
        serverSocket.sendto(returnCode.encode(), clientAddressComplete)

    # print(3) #test if command is sent


def server_queryDHT():
    print(4)


def server_leaveDHT():
    print(5)


def server_rebuiltDHT():
    print(6)


def server_deRegister():
    # receive username from client
    deRegisterUserName, clientAddressDeRegister = serverSocket.recvfrom(2048)

    # random boolean variable set to false by default
    statement = False

    # decode username
    decodeName = deRegisterUserName.decode()

    # finds user
    for person in arrayStorage:
        # if the username is the same as the decode name and its state is Free
        if person.userName == decodeName and person.state == "Free":
            # delete user and their info
            # add decoded information to array via userInfo
            # arr.append(UserInfo(decodeName, decodeIP, decodePort, state))
            arrayStorage.remove(person)
            # print(person)
            statement = True
            # update return code statement and send it back to client
            returnCode = "SUCCESS: User de-registered"
            serverSocket.sendto(returnCode.encode(), clientAddressDeRegister)
            break

    # if the user wasn't found or the state isn't Free
    if statement is False:
        # update return code statement and send it back to client
        returnCode = "FAILURE: The user is a node maintaining the DHT or user doesn't exist"
        serverSocket.sendto(returnCode.encode(), clientAddressDeRegister)


def server_joinDHT():
    print(8)


def server_teardownDHT():
    print(9)


def server_teardownComplete():
    print(10)


def thread0():
    print(11)


# x1 = threading.Thread(target=server_register())
# x2 = threading.Thread(target=server_setupDHT())
# x3 = threading.Thread(target=server_completeDHT())
# x7 = threading.Thread(target=server_deRegister())

# x1.start()
# x2.start()
# x3.start()
# x7.start()


while True:
    # receives encoded command from client and decodes it
    encodedCommand, clientAddress = serverSocket.recvfrom(2048)
    command = encodedCommand.decode()
    print(f'Command Number: {command}')

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
        server_deRegister()
    if command == "8":
        server_joinDHT()
    if command == "9":
        server_teardownDHT()
    if command == "10":
        server_teardownComplete()
