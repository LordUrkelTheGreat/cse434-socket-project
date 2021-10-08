from socket import *
import sys
import csv

# dictionaries (don't delete)
userDict = {}
dhtDict = {}
countriesDict = {}

# number of registered users
numOfUsers = 0

# node id
nodeID = 0

# setup DHT lockout
lockout = False

# setup DHT complete lockout
lockout1 = False

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

    # if dht-complete wasn't execute after setup-dht
    if lockout1 is True:
        returnCode = "FAILURE: dht-complete must be executed first right after setup-dht"
        serverSocket.sendto(returnCode.encode(), clientAddressRegister)
        return

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
    userDict[decodeName] = [decodeIP, decodePort, state]

    # keeps track of how many users are registered by adding 1 to itself
    global numOfUsers
    numOfUsers += 1

    # print statements
    print(f'Username: {decodeName}')
    print(f'IP Address: {userDict[decodeName][0]}')
    print(f'Port Number: {userDict[decodeName][1]}')
    print(f'State: {userDict[decodeName][2]}')
    print(f'Values are stored')

    # update return code statement and send it back to client
    returnCode = "SUCCESS: User registered"
    serverSocket.sendto(returnCode.encode(), clientAddressRegister)


def server_setupDHT():
    # receive n and username from client
    setupN, clientAddressSetUp = serverSocket.recvfrom(2048)
    setupUserName, clientAddressSetUp = serverSocket.recvfrom(2048)

    # if dht-complete wasn't execute after setup-dht
    global lockout1
    if lockout1 is True:
        returnCode = "FAILURE: dht-complete must be executed first right after setup-dht"
        serverSocket.sendto(returnCode.encode(), clientAddressSetUp)
        return

    # random boolean statements set to true and false by default
    valid = True
    userInDict = False

    # decode n and username
    decodeN = int(setupN.decode())
    decodeName = setupUserName.decode()

    # check if user is register and set to true if found
    for key in userDict.keys():
        if decodeName in key:
            userInDict = True

    # if user is not registered return with failure
    if userInDict is False:
        returnCode = "FAILURE: user is not registered"
        serverSocket.sendto(returnCode.encode(), clientAddressSetUp)
        return

    # if lockout is true return with failure
    if lockout is True:
        returnCode = "FAILURE: setup DHT is locked out"
        serverSocket.sendto(returnCode.encode(), clientAddressSetUp)
        return
    # if lockout is false continue
    else:
        # if random boolean statement is true
        if valid is True:
            # if n is greater than or equal to 2
            if decodeN >= 2:
                # if n is less than or equal to number of registered users
                if decodeN <= numOfUsers:
                    # storing csv values into a dictionary of lists (DO NOT DELETE)
                    # open csv file
                    file = open('StatsCountry.csv', 'r', encoding='unicode_escape')
                    # read csv values
                    reader = csv.reader(file)
                    # skip header
                    next(reader, None)
                    # store csv values separately as key-value pairs in a dictionary
                    for row in reader:
                        countriesDict[row[0]] = [row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]]
                        # print(countriesDict[row[0]])

                    # list of countries that each node will store
                    records = [[]] * 353

                    # store leader in the dht dictionary first
                    dhtDict[decodeName] = userDict[decodeName].copy()

                    # change the user's state from free to leader
                    newState = "Leader"
                    userDict[decodeName][2] = newState
                    dhtDict[decodeName][2] = newState
                    # add node id
                    dhtDict[decodeName].append(0)
                    # add record list
                    dhtDict[decodeName].append(records)

                    # node id
                    global nodeID
                    nodeID = 0

                    # copy data from user dictionary to dht dictionary
                    for key in userDict:
                        # makes sure that the Leader's data isn't copied again
                        if userDict[key][2] is not 'Leader' and nodeID < (decodeN - 1):
                            # copy data
                            dhtDict[key] = userDict[key].copy()
                            # change user state to InDHT
                            dhtDict[key][2] = "InDHT"
                            userDict[key][2] = "InDHT"
                            # add node id
                            dhtDict[key].append(0)
                            nodeID += 1
                            dhtDict[key][3] = nodeID
                            # add record list
                            dhtDict[key].append(records)

                    # print(dhtDict)
                    # print(userDict)

                    # store country records in corresponding node id
                    for key in countriesDict.items():
                        # find country's long name and find the sum of the ASCII value of each character
                        word = countriesDict[key[0]][2]
                        sumOfCharacters = sum(ord(ch) for ch in word)

                        # calculate the position of the country that will be stored in the node
                        position = sumOfCharacters % 353
                        # print(f'Position: {position}')
                        # calculate the node id the country record will be stored in
                        storeInWhichNode = position % decodeN
                        # print(f'Store in which node: {storeInWhichNode}')

                        # store record in correct position and node
                        for k, v in dhtDict.items():
                            # print(dhtDict[k][3])
                            ID = dhtDict[k][3]
                            if storeInWhichNode is ID:
                                # print(dhtDict[k][4][0])
                                dhtDict[k][4][position] = countriesDict[key[0]].copy()
                                # print(f'ID: {ID}')
                                # print(dhtDict[k][4][position])

                    # print(dhtDict)
                    # print(countriesDict)

                    # lockout setup-dht and return success code
                    lockout1 = True
                    returnCode = "SUCCESS: setup dht is complete"
                    serverSocket.sendto(returnCode.encode(), clientAddressSetUp)

                    # send DHT table of users and their ip addresses and port numbers to client
                    return
                else:
                    returnCode = "FAILURE: n is bigger than the number of registered users"
                    serverSocket.sendto(returnCode.encode(), clientAddressSetUp)
                    return
            # if n is less than 2 than it returns a failure
            else:
                returnCode = "FAILURE: n needs to be greater than or equal to 2"
                serverSocket.sendto(returnCode.encode(), clientAddressSetUp)
                return


def server_completeDHT():
    # receive username from client
    completeUserName, clientAddressComplete = serverSocket.recvfrom(2048)

    # random boolean statement set to False by default
    valid = False

    # decode username
    decodeName = completeUserName.decode()

    # search through dictionary
    for key, value in userDict.items():
        # if the user is the key
        if key == decodeName:
            # if the user state is Leader
            if userDict[key][2] == 'Leader':
                # if dhtDict exists
                if len(dhtDict) != 0:
                    valid = True
                    break

    if valid is True:
        returnCode = "SUCCESS: DHT has been established"
        global lockout
        lockout = True
        global lockout1
        lockout1 = False
    else:
        returnCode = "FAILURE: DHT isn't setup, User isn't the leader, or User isn't registered"

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

    # if dht-complete wasn't execute after setup-dht
    global lockout1
    if lockout1 is True:
        returnCode = "FAILURE: dht-complete must be executed first right after setup-dht"
        serverSocket.sendto(returnCode.encode(), clientAddressDeRegister)
        return

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
                # keeps track of how many users are registered by subtracting 1 to itself
                global numOfUsers
                numOfUsers -= 1
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
