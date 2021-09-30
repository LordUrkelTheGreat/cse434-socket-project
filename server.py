from socket import *
import sys
import csv

# dictionaries (don't delete)
userDict = {}
dhtDict = {}
countriesDict = {}

# setup DHT lockout
lockout = False

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


def server_register():
    # receive username, ip address, and port number from client
    regName, clientAddressRegister = serverSocket.recvfrom(2048)
    regIP, clientAddressRegister = serverSocket.recvfrom(2048)
    regPort, clientAddressRegister = serverSocket.recvfrom(2048)

    # random boolean statement set to false as default
    valid = False

    # decode username, ip address, and port number
    decodeName = regName.decode()
    decodeIP = regIP.decode()
    decodePort = regPort.decode()
    state = "Free"

    # checks if username exists in the dictionary. if it does,
    # then return FAILURE to indicate that register function
    # failed to create new user
    if valid is False:
        # checks if username is registered
        for key in userDict.items():
            # check if decodeName is in dictionary
            if decodeName in key:
                returnCode = "FAILURE: Username already exists"
                serverSocket.sendto(returnCode.encode(), clientAddressRegister)
                return
        # checks if port number is registered
        for value in userDict.values():
            # check if decodePort is in dictionary
            if decodePort in value:
                returnCode = "FAILURE: Port number is already in use"
                serverSocket.sendto(returnCode.encode(), clientAddressRegister)
                return

    # add decoded information to dictionary
    # arrayStorage.append(UserInfo(decodeName, decodeIP, decodePort, state))
    userDict[decodeName] = decodeIP, decodePort, state

    # print statements
    print(f'Username: {decodeName}')
    print(f'IP Address: {decodeIP}')
    print(f'Port Number: {decodePort}')
    print(f'State: {state}')
    print(f'Values are stored')

    # update return code statement and send it back to client
    returnCode = "SUCCESS: User registered"
    serverSocket.sendto(returnCode.encode(), clientAddressRegister)


def server_setupDHT():
    # receive n and username from client
    setupN, clientAddressSetUp = serverSocket.recvfrom(2048)
    setupUserName, clientAddressSetUp = serverSocket.recvfrom(2048)

    # random boolean statement set to true by default
    valid = True

    # decode n and username
    decodeN = int(setupN.decode())
    decodeName = setupUserName.decode()

    if lockout is True:
        returnCode = "FAILURE: setup DHT is locked out"
        serverSocket.sendto(returnCode.encode(), clientAddressSetUp)
    else:
        if valid is True and decodeN >= 2:
            print(decodeName)

            # open csv file
            file = open('StatsCountry.csv', 'r', encoding='unicode_escape')
            # read csv values
            reader = csv.reader(file)
            # skip header
            next(reader, None)
            # store csv values separately as key-value pairs in a dictionary
            for row in reader:
                countriesDict['{\'Country Code\': \'' + row[0] + '\'}'] = {'Short Name': row[1], 'Table Name': row[2], 'Long Name': row[3], '2-Alpha Code': row[4], 'Currency Unit': row[5], 'Region': row[6], 'WB-2 Code': row[7], 'Latest Population Census': row[8]}

            # print keys and values
            # for key, value in countriesDict.items():
                # print(key, value)

            # print dictionary
            # print(countriesDict)


def server_completeDHT():
    # receive username from client
    completeUserName, clientAddressComplete = serverSocket.recvfrom(2048)

    # random boolean statement set to true by default
    valid = True

    # if the function doesn't properly execute for some reason
    returnCode = "FAILURE: complete DHT failed to function properly"

    # decode username
    decodeName = completeUserName.decode()

    # search through dictionary
    for key, value in userDict.items():
        # if the user is the key
        if decodeName in key:
            # if the user state is Leader
            if "Leader" in value:
                # if dhtDict exists
                if dhtDict:
                    valid = True
                else:
                    returnCode = "FAILURE: DHT not setup"
                    valid = False
            else:
                returnCode = "FAILURE: User is not the leader"
                valid = False
        else:
            returnCode = "FAILURE: User isn't registered"
            valid = False

    if valid is True:
        returnCode = "SUCCESS"

    serverSocket.sendto(returnCode.encode(), clientAddressComplete)


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
    for key, value in userDict.items():
        # if the username is the same as the decode name and its state is Free
        if decodeName in key:
            if "Free" in value:
                # delete user and their info
                userDict.pop(key)
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


while True:
    # receives encoded command from client and decodes it
    encodedCommand, clientAddress = serverSocket.recvfrom(2048)
    command = encodedCommand.decode()
    print()
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
