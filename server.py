from socket import *
import sys
import csv
import random

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
lockout2 = False

# previous key
previousKey = ""

# right neighbor
rightNeighbor = ""

# removed key
removedDict = {}
removedKey = ""

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
    decodePort = int(decodePort)
    leftPort = int(decodePort * 2)
    rightPort = int(leftPort + 11)
    queryPort = int(decodePort + 100)
    userDict[decodeName] = [decodeName, decodeIP, decodePort, state, leftPort, rightPort, queryPort]

    # keeps track of how many users are registered by adding 1 to itself
    global numOfUsers
    numOfUsers += 1

    # print statements
    print(f'Username: {userDict[decodeName][0]}')
    print(f'IP Address: {userDict[decodeName][1]}')
    print(f'Port Number: {userDict[decodeName][2]}')
    print(f'State: {userDict[decodeName][3]}')
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
                    userDict[decodeName][3] = newState
                    dhtDict[decodeName][3] = newState
                    # add node id
                    dhtDict[decodeName].append(0)
                    # add record list
                    dhtDict[decodeName].append(records)

                    # node id
                    global nodeID, previousKey
                    previousKey = decodeName
                    nodeID = 0

                    # print(dhtDict)

                    # copy data from user dictionary to dht dictionary
                    for key in userDict:
                        if userDict[key][3] is not 'Leader':
                            # copy data
                            dhtDict[key] = userDict[key].copy()

                            # change user state from Free to InDHT
                            dhtDict[key][3] = "InDHT"
                            userDict[key][3] = "InDHT"

                            # add node id
                            dhtDict[key].append(0)
                            nodeID += 1
                            dhtDict[key][7] = nodeID

                            # add records
                            dhtDict[key].append(records)

                    # connect the ports to form a circle
                    for key in dhtDict:
                        # node 1 is the last node in DHT
                        if dhtDict[key][7] == 1 and dhtDict[key][7] == (decodeN - 1):
                            # node 1 left port is equal to node 0 right port
                            dhtDict[key][4] = dhtDict[previousKey][5]
                            # node 1 right port is equal to node 0 left port
                            dhtDict[key][5] = dhtDict[previousKey][4]
                        # last node in the DHT is not node 1
                        elif dhtDict[key][7] == (decodeN - 1):
                            # last node left port is equal to left neighbor node right port
                            dhtDict[key][4] = dhtDict[previousKey][5]
                            # last node right port is equal to node 0 left port
                            dhtDict[key][5] = dhtDict[decodeName][4]
                        # node that is not the last node in DHT
                        else:
                            # makes sure node 0 left and right ports are not updated
                            if dhtDict[key][7] != 0:
                                # current node left port is equal to left neighbor node right port
                                dhtDict[key][4] = dhtDict[previousKey][5]
                            previousKey = key

                    # print(dhtDict)
                    # print(userDict)

                    # store country records in corresponding node id
                    for key in countriesDict.items():
                        # find country's long name and find the sum of the ASCII value of each character
                        word = countriesDict[key[0]][3]
                        sumOfCharacters = sum(ord(ch) for ch in word)
                        # print(word)

                        # calculate the position of the country that will be stored in the node
                        position = sumOfCharacters % 353
                        # print(f'Position: {position}')
                        # calculate the node id the country record will be stored in
                        storeInWhichNode = position % decodeN
                        # print(f'Store in which node: {storeInWhichNode}')

                        # store record in correct position and node
                        for k, v in dhtDict.items():
                            # print(dhtDict[k][3])
                            ID = dhtDict[k][7]
                            if storeInWhichNode is ID:
                                # print(dhtDict[k][7][0])
                                dhtDict[k][8][position] = countriesDict[key[0]].copy()
                                # print(f'ID: {ID}')
                                # print(dhtDict[k][7][position])

                    # print(dhtDict)
                    # print(countriesDict)

                    # lockout setup-dht and return success code
                    lockout1 = True
                    returnCode = "SUCCESS: setup dht is complete"
                    serverSocket.sendto(returnCode.encode(), clientAddressSetUp)
                    global lockout2
                    lockout2 = True

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
            if userDict[key][3] == 'Leader':
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
    # receive username from client
    queryUserName, clientAddressQuery = serverSocket.recvfrom(2048)

    # decode username
    decodeName = queryUserName.decode()

    # random boolean statement set to false by default
    valid = False

    # if setup-dht wasn't completed
    global lockout2
    if lockout2 is False:
        returnCode = "FAILURE: setup-dht must be completed first"
        serverSocket.sendto(returnCode.encode(), clientAddressQuery)
        return

    # if dht-complete wasn't execute after setup-dht
    global lockout1
    if lockout1 is True:
        returnCode = "FAILURE: dht-complete must be executed first right after setup-dht"
        serverSocket.sendto(returnCode.encode(), clientAddressQuery)
        return

    # check if user exists and state is Free
    for key, value in userDict.items():
        if decodeName in key:
            if 'Free' in value:
                valid = True
                break

    # if the user wasn't found or the state isn't Free
    if valid is False:
        # update return code statement and send it back to client
        returnCode = "FAILURE: The user is a node maintaining the DHT or user doesn't exist"
        serverSocket.sendto(returnCode.encode(), clientAddressQuery)
        return

    # FAILURE checks are done now to do the function

    # pick random n user
    randomUser = random.choice(list(dhtDict.keys()))
    # print(randomUser)

    # send random user to client
    randomUserString = f'Random user in the DHT that will start the query: {randomUser}'
    serverSocket.sendto(randomUserString.encode(), clientAddressQuery)

    # returns long name of country from client
    longName, clientAddressQuery = serverSocket.recvfrom(2048)
    decodeLongName = longName.decode()
    # print(decodeLongName)

    # starting at random index, go through dht dictionary finding long name
    # find the sum of the ASCII value of each character in long name
    word = decodeLongName
    sumOfCharacters = sum(ord(ch) for ch in word)
    # print(word)

    # calculate the position of the country that will be stored in the node
    position = sumOfCharacters % 353
    inWhichID = position % len(dhtDict)

    # find node ID
    returnCode = "FAILURE: Long-name search didn't work"
    for key, value in dhtDict.items():
        # store node id
        ID = dhtDict[key][7]
        # if node ID is the same as calculated ID and if long name is found in records
        if inWhichID is ID and word is dhtDict[key][7][position][3]:
            # return record to client
            record0 = dhtDict[key][8][position][0]
            record1 = dhtDict[key][8][position][1]
            record2 = dhtDict[key][8][position][2]
            record3 = dhtDict[key][8][position][3]
            record4 = dhtDict[key][8][position][4]
            record5 = dhtDict[key][8][position][5]
            record6 = dhtDict[key][8][position][6]
            record7 = dhtDict[key][8][position][7]
            record8 = dhtDict[key][8][position][8]
            returnRecord = f'Country Code: {record0}, Short Name: {record1}, Table Name: {record2}, Long Name: {record3}, 2-Alpha Code: {record4}, Currency Unit: {record5}, Region: {record6}, WB-2 Code: {record7}, Latest Population Census: {record8}'
            serverSocket.sendto(returnRecord.encode(), clientAddressQuery)

            # return success
            returnCode = "SUCCESS: Long-name found in DHT"
            serverSocket.sendto(returnCode.encode(), clientAddressQuery)
            return
        else:
            returnCode = "FAILURE: Long-name not found in DHT"

    serverSocket.sendto(returnCode.encode(), clientAddressQuery)
    return


def server_leaveDHT():
    # receive username from client
    leaveUserName, clientAddressLeave = serverSocket.recvfrom(2048)

    # decode username
    decodeName = leaveUserName.decode()

    # checks if dht is empty
    if len(dhtDict) is 0:
        returnCode = "FAILURE: DHT doesn't exist"
        serverSocket.sendto(returnCode.encode(), clientAddressLeave)
        return

    # checks if user is maintaining the dht
    if userDict[decodeName][3] != 'Leader' and userDict[decodeName][3] != 'InDHT':
        returnCode = "FAILURE: user is not maintaining the DHT"
        serverSocket.sendto(returnCode.encode(), clientAddressLeave)
        return

    # FAILURE conditions are done. now to work on the success part.
    # user store the 3-tuple (username, ip address, and port number) of its right neighbor

    # find node id of right neighbor if leader is not the right neighbor
    # store leader key just in case if leader is the right neighbor
    currentNodeID = dhtDict[decodeName][7]
    leader = decodeName
    global rightNeighbor
    rightNeighbor = ""
    for key in dhtDict.keys():
        temp = dhtDict[key][7]
        # if key is leader
        if dhtDict[key][3] == 'Leader':
            leader = key
        # if key is the right neighbor
        if temp == currentNodeID + 1:
            rightNeighbor = key

    # checks if right neighbor is the leader and stores it
    if currentNodeID == len(dhtDict) - 1:
        # store the right neighbor's 3-tuple
        rightNeighborUserName = dhtDict[leader][0]
        rightNeighborIpAddress = dhtDict[leader][1]
        rightNeighborPortNumber = dhtDict[leader][2]
        rightNeighborState = dhtDict[leader][3]
        rightNeighborLeftPort = dhtDict[leader][4]
        rightNeighborRightPort = dhtDict[leader][5]
        rightNeighborQueryPort = dhtDict[leader][6]
        rightNeighborNodeID = dhtDict[leader][7]
        rightNeighborRecords = dhtDict[leader][8]
        # print(f'Right Neighbor Username: {rightNeighborUserName}')
        # print(f'Right Neighbor IP Address: {rightNeighborIpAddress}')
        # print(f'Right Neighbor Port Number: {rightNeighborPortNumber}')
        # print(f'Right Neighbor State: {rightNeighborState}')
        # print(f'Right Neighbor Left Port: {rightNeighborLeftPort}')
        # print(f'Right Neighbor Right Port: {rightNeighborRightPort}')
        # print(f'Right Neighbor Query Port: {rightNeighborQueryPort}')
        # print(f'Right Neighbor Node ID: {rightNeighborNodeID}')
        # print(f'Right Neighbor Records: {rightNeighborRecords}')
    # if right neighbor is not the leader and stores it
    else:
        # store the right neighbor's 3-tuple
        rightNeighborUserName = dhtDict[rightNeighbor][0]
        rightNeighborIpAddress = dhtDict[rightNeighbor][1]
        rightNeighborPortNumber = dhtDict[rightNeighbor][2]
        rightNeighborState = dhtDict[rightNeighbor][3]
        rightNeighborLeftPort = dhtDict[rightNeighbor][4]
        rightNeighborRightPort = dhtDict[rightNeighbor][5]
        rightNeighborQueryPort = dhtDict[rightNeighbor][6]
        rightNeighborNodeID = dhtDict[rightNeighbor][7]
        rightNeighborRecords = dhtDict[rightNeighbor][8]
        # print(f'Right Neighbor Username: {rightNeighborUserName}')
        # print(f'Right Neighbor IP Address: {rightNeighborIpAddress}')
        # print(f'Right Neighbor Port Number: {rightNeighborPortNumber}')
        # print(f'Right Neighbor State: {rightNeighborState}')
        # print(f'Right Neighbor Left Port: {rightNeighborLeftPort}')
        # print(f'Right Neighbor Right Port: {rightNeighborRightPort}')
        # print(f'Right Neighbor Query Port: {rightNeighborQueryPort}')
        # print(f'Right Neighbor Node ID: {rightNeighborNodeID}')
        # print(f'Right Neighbor Records: {rightNeighborRecords}')

    # remove node and set right neighbor as leader if leader node was removed
    global removedKey, removedDict
    for key in dhtDict.keys():
        if key == decodeName:
            if key == leader:
                dhtDict[rightNeighbor][3] = 'Leader'

            # store removed values
            user = dhtDict[key][0]
            ipAddress = dhtDict[key][1]
            portNumber = dhtDict[key][2]
            state = dhtDict[key][3]
            leftPort = dhtDict[key][4]
            rightPort = dhtDict[key][5]
            queryPort = dhtDict[key][6]
            ID = dhtDict[key][7]
            records = dhtDict[key][8]

            # create removed key dictionary
            removedDict = {}
            removedKey = key
            removedDict[key] = [user, ipAddress, portNumber, state, leftPort, rightPort, queryPort, ID, records]

            # remove key
            dhtDict.pop(key)
            break

    # renumber node IDs
    renumberNodeID = 0
    for key in dhtDict.keys():
        dhtDict[key][7] = renumberNodeID
        renumberNodeID += 1

    # reset left and right neighbors through left and right ports
    global nodeID, previousKey
    node0 = ""

    # re-connects the ports to form a circle after node was removed
    for key in dhtDict:
        # list of countries that each node will store
        records = [[]] * 353

        # remove records in order to update DHT an re-sort records again
        dhtDict[key].remove(dhtDict[key][8])
        dhtDict[key].append(records)

        # store country records in corresponding node id
        for key1 in countriesDict.items():
            # find country's long name and find the sum of the ASCII value of each character
            word = countriesDict[key1[0]][3]
            sumOfCharacters = sum(ord(ch) for ch in word)

            # calculate the position of the country that will be stored in the node
            position = sumOfCharacters % 353
            # calculate the node id the country record will be stored in
            storeInWhichNode = position % len(dhtDict)

            # store record in correct position and node
            for k, v in dhtDict.items():
                ID = dhtDict[k][7]
                if storeInWhichNode is ID:
                    dhtDict[k][8][position] = countriesDict[key1[0]].copy()

        # if there is only 1 node in the DHT
        if len(dhtDict) == 1:
            break
        # if there is more than 1 node in the DHT
        else:
            # node 1 is the last node in DHT
            if dhtDict[key][7] == 1 and dhtDict[key][7] == (len(dhtDict) - 1):
                # node 1 left port is equal to node 0 right port
                dhtDict[key][4] = dhtDict[previousKey][5]
                # node 1 right port is equal to node 0 left port
                dhtDict[key][5] = dhtDict[previousKey][4]
            # last node in the DHT is not node 1
            elif dhtDict[key][7] == (len(dhtDict) - 1):
                # last node left port is equal to left neighbor node right port
                dhtDict[key][4] = dhtDict[previousKey][5]
                # last node right port is equal to node 0 left port
                dhtDict[key][5] = dhtDict[node0][4]
            else:
                # if current node is node 0 store key in random variable
                if dhtDict[key][3] is 'Leader':
                    node0 = key
                # makes sure node 0 left and right ports are not updated
                if dhtDict[key][7] != 0:
                    # current node left port is equal to left neighbor node right port
                    dhtDict[key][4] = dhtDict[previousKey][5]
                previousKey = key

    # print stuff from dht dict (comment if not testing)
    # for key in dhtDict.keys():
        # user
        # print(f'User: {dhtDict[key][0]}')
        # ip address
        # print(f'IP Address: {dhtDict[key][1]}')
        # port number
        # print(f'Port Number: {dhtDict[key][2]}')
        # state
        # print(f'State: {dhtDict[key][3]}')
        # left port
        # print(f'Left Port: {dhtDict[key][4]}')
        # right port
        # print(f'Right Port: {dhtDict[key][5]}')
        # query port
        # print(f'Query Port: {dhtDict[key][6]}')
        # node id
        # print(f'Node ID: {dhtDict[key][7]}')
        # records
        # print(f'Records: {dhtDict[key][8]}')

    # send return code statement to client
    returnCode = "SUCCESS: user left the DHT"
    serverSocket.sendto(returnCode.encode(), clientAddressLeave)
    return


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
