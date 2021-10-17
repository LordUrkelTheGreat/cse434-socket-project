from socket import *
import sys
import csv
import random

# dictionaries (don't delete)
userDict = {}
dhtDict = {}
countriesDict = {}
tempDHTDict = {}

# number of registered users
numOfUsers = 0

# node id
nodeID = 0

# setup DHT lockout
lockout = False

# setup DHT complete lockout
lockout1 = False
lockout2 = False

# leave-dht lockout
lockout3 = False

# teardown-dht lockout
lockout4 = False

# previous key
previousKey = ""

# right neighbor
rightNeighbor = ""

# removed username
removedUserName = ""

# add username
addUserName = ""

# leader username
leaderUserName = ""

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

    # if teardown-complete wasn't executed after teardown-dht
    global lockout4
    if lockout4 is True:
        returnCode = "FAILURE: teardown-complete must be completed after teardown-dht"
        serverSocket.sendto(returnCode.encode(), clientAddressRegister)
        return

    # if rebuilt-dht wasn't executed after leave-dht
    global lockout3
    if lockout3 is True:
        returnCode = "FAILURE: dht-rebuilt must be completed after leave-dht or join-dht"
        serverSocket.sendto(returnCode.encode(), clientAddressRegister)
        return

    # if dht-complete wasn't execute after setup-dht
    if lockout1 is True:
        returnCode = "FAILURE: dht-complete must be executed first right after setup-dht"
        serverSocket.sendto(returnCode.encode(), clientAddressRegister)
        return

    # decode username, ip address, and port number
    decodeName = regName.decode()
    decodeIP = regIP.decode()
    decodePort = regPort.decode()
    state = "Free"

    # checks if username exists in the dictionary. if it does,
    # then return FAILURE to indicate that register function
    # failed to create new user
    # checks if username is registered
    for key in userDict:
        # check if decodeName is in dictionary
        if decodeName == key:
            returnCode = "FAILURE: Username already exists"
            serverSocket.sendto(returnCode.encode(), clientAddressRegister)
            return
    # checks if port number is registered
    for key in userDict:
        # check if decodePort is in dictionary
        portNumber = int(userDict[key][2])
        if int(decodePort) == portNumber:
            returnCode = "FAILURE: Port number is already in use"
            serverSocket.sendto(returnCode.encode(), clientAddressRegister)
            return

    # add decoded information to dictionary
    decodePort = int(decodePort)
    leftPort = int(decodePort * 2)
    rightPort = int(decodePort * 3 + 11)
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

    # if teardown-complete wasn't executed after teardown-dht
    global lockout4
    if lockout4 is True:
        returnCode = "FAILURE: teardown-complete must be completed after teardown-dht"
        serverSocket.sendto(returnCode.encode(), clientAddressSetUp)
        return

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

                    # copy data from user dictionary to dht dictionary
                    for key in userDict:
                        if userDict[key][3] is not 'Leader' and nodeID < (decodeN - 1):
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

                    # store country records in corresponding node id
                    for key in countriesDict.items():
                        # find country's long name and find the sum of the ASCII value of each character
                        word = countriesDict[key[0]][3]
                        sumOfCharacters = sum(ord(ch) for ch in word)

                        # calculate the position of the country that will be stored in the node
                        position = sumOfCharacters % 353
                        # calculate the node id the country record will be stored in
                        storeInWhichNode = position % decodeN

                        # store record in correct position and node
                        for k, v in dhtDict.items():
                            ID = dhtDict[k][7]
                            if storeInWhichNode is ID:
                                dhtDict[k][8][position] = countriesDict[key[0]].copy()

                    # lockout setup-dht and return success code
                    lockout1 = True
                    returnCode = "SUCCESS: setup dht is complete"
                    serverSocket.sendto(returnCode.encode(), clientAddressSetUp)
                    global lockout2
                    lockout2 = True

                    print(f'List of {len(dhtDict)} users that will construct the DHT')
                    for key in dhtDict.keys():
                        print(f'User: ({dhtDict[key][0]}) IP Address: ({dhtDict[key][1]}) Port Number: ({dhtDict[key][2]})')

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

    # if teardown-complete wasn't executed after teardown-dht
    global lockout4
    if lockout4 is True:
        returnCode = "FAILURE: teardown-complete must be completed after teardown-dht"
        serverSocket.sendto(returnCode.encode(), clientAddressQuery)
        return

    # if rebuilt-dht wasn't executed after leave-dht
    global lockout3
    if lockout3 is True:
        returnCode = "FAILURE: dht-rebuilt must be completed after leave-dht or join-dht"
        serverSocket.sendto(returnCode.encode(), clientAddressQuery)
        return

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

    # send random user to client
    randomUserString = f'Random user in the DHT that will start the query: {randomUser}'
    serverSocket.sendto(randomUserString.encode(), clientAddressQuery)

    # returns long name of country from client
    longName, clientAddressQuery = serverSocket.recvfrom(2048)
    decodeLongName = longName.decode()

    # starting at random index, go through dht dictionary finding long name
    # find the sum of the ASCII value of each character in long name
    word = decodeLongName
    sumOfCharacters = sum(ord(ch) for ch in word)

    # calculate the position of the country that will be stored in the node
    position = sumOfCharacters % 353
    inWhichID = position % len(dhtDict)

    # find node ID
    returnCode = "FAILURE: Long-name search didn't work"
    for key in dhtDict.keys():
        # store node id
        ID = int(dhtDict[key][7])
        longName = dhtDict[key][8][position][3]
        # if node ID is the same as calculated ID and if long name is found in records
        if inWhichID == ID and word == longName:
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

    # if teardown-complete wasn't executed after teardown-dht
    global lockout4
    if lockout4 is True:
        returnCode = "FAILURE: teardown-complete must be completed after teardown-dht"
        serverSocket.sendto(returnCode.encode(), clientAddressLeave)
        return

    # if rebuilt-dht wasn't executed after leave-dht
    global lockout3
    if lockout3 is True:
        returnCode = "FAILURE: dht-rebuilt must be completed after leave-dht or join-dht"
        serverSocket.sendto(returnCode.encode(), clientAddressLeave)
        return

    # if setup-dht wasn't completed
    global lockout2
    if lockout2 is False:
        returnCode = "FAILURE: setup-dht must be completed first"
        serverSocket.sendto(returnCode.encode(), clientAddressLeave)
        return

    # if dht-complete wasn't execute after setup-dht
    global lockout1
    if lockout1 is True:
        returnCode = "FAILURE: dht-complete must be executed first right after setup-dht"
        serverSocket.sendto(returnCode.encode(), clientAddressLeave)
        return

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

    # FAILURE conditions are done

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

    # remove node and set right neighbor as leader if leader node was removed
    global removedUserName
    removedUserName = ""
    for key in dhtDict.keys():
        if key == decodeName:
            if key == leader:
                dhtDict[rightNeighbor][3] = 'Leader'
                userDict[rightNeighbor][3] = 'Leader'

            # store removed user
            removedUserName = key

            # set removed key state to free
            userDict[key][3] = 'Free'

            # remove key
            dhtDict.pop(key)
            break

    # print(userDict)

    # renumber node IDs
    renumberNodeID = 0
    for key in dhtDict.keys():
        dhtDict[key][7] = renumberNodeID
        renumberNodeID += 1

    # reset left and right neighbors through left and right ports
    global nodeID, previousKey
    node0 = decodeName
    previousKey = decodeName

    # re-connects the ports to form a circle after node was removed
    for key in dhtDict:
        # list of countries that each node will store
        records = [[]] * 353

        # remove records in order to update DHT an re-sort records again
        dhtDict[key].remove(dhtDict[key][8])
        dhtDict[key].append(records)

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

    # store country records in corresponding node id
    for key in countriesDict.items():
        # find country's long name and find the sum of the ASCII value of each character
        word = countriesDict[key[0]][3]
        sumOfCharacters = sum(ord(ch) for ch in word)

        # calculate the position of the country that will be stored in the node
        position = sumOfCharacters % 353
        # calculate the node id the country record will be stored in
        storeInWhichNode = position % len(dhtDict)

        # store record in correct position and node
        for k, v in dhtDict.items():
            ID = dhtDict[k][7]
            if storeInWhichNode is ID:
                dhtDict[k][8][position] = countriesDict[key[0]].copy()

    # this makes sure that user has to rebuild dht first before removing another user from dht
    lockout3 = True

    # reset temporary dht dictionary
    global tempDHTDict
    tempDHTDict = {}

    # send return code statement to client
    returnCode = "SUCCESS: user left the DHT"
    serverSocket.sendto(returnCode.encode(), clientAddressLeave)
    return


def server_rebuiltDHT():
    global dhtDict

    # receive username and new leader from client
    rebuiltUserName, clientAddressRebuilt = serverSocket.recvfrom(2048)
    rebuiltNewLeader, clientAddressRebuilt = serverSocket.recvfrom(2048)

    # decode username and new leader
    decodeUserName = rebuiltUserName.decode()
    decodeNewLeader = rebuiltNewLeader.decode()

    # if teardown-complete wasn't executed after teardown-dht
    global lockout4
    if lockout4 is True:
        returnCode = "FAILURE: teardown-complete must be completed after teardown-dht"
        serverSocket.sendto(returnCode.encode(), clientAddressRebuilt)
        return

    # if setup-dht wasn't completed
    global lockout2
    if lockout2 is False:
        returnCode = "FAILURE: setup-dht must be completed first"
        serverSocket.sendto(returnCode.encode(), clientAddressRebuilt)
        return

    # if dht-complete wasn't execute after setup-dht
    global lockout1
    if lockout1 is True:
        returnCode = "FAILURE: dht-complete must be executed first right after setup-dht"
        serverSocket.sendto(returnCode.encode(), clientAddressRebuilt)
        return

    # if old username is not the same as removed username
    global removedUserName
    if decodeUserName != removedUserName and decodeUserName != addUserName:
        returnCode = "FAILURE: old username does not match leave-dht or join-dht username"
        serverSocket.sendto(returnCode.encode(), clientAddressRebuilt)
        return

    # if new leader matches username. should not happen since username was removed from DHT
    if decodeNewLeader == removedUserName and decodeNewLeader != addUserName:
        returnCode = "FAILURE: new leader cannot be deleted username"
        serverSocket.sendto(returnCode.encode(), clientAddressRebuilt)
        return

    # check if new leader is in dht. if not return failure.
    valid = False
    for key in dhtDict.keys():
        if key == decodeNewLeader:
            valid = True
            break
    if valid is False:
        returnCode = "FAILURE: new leader is not in DHT"
        serverSocket.sendto(returnCode.encode(), clientAddressRebuilt)
        return

    # FAILURE checks finished

    # find if new leader is not old leader, set new leader as leader and old leader as InDHT
    for key in dhtDict.keys():
        if dhtDict[key][3] == 'Leader' and decodeNewLeader != dhtDict[key][3]:
            userDict[key][3] = "InDHT"
            dhtDict[key][3] = "InDHT"
            userDict[decodeNewLeader][3] = "Leader"
            dhtDict[decodeNewLeader][3] = "Leader"
            break

    # print(userDict)

    # store new leader in the temporary dht dictionary first
    global tempDHTDict
    tempDHTDict[decodeNewLeader] = dhtDict[decodeNewLeader].copy()

    # set new leader node as node 0
    tempDHTDict[decodeNewLeader][7] = 0

    # node id
    global nodeID
    nodeID = 0

    # copy dht dictionary data to temporary dht dictionary
    for key in dhtDict.keys():
        # leader is already copied
        if dhtDict[key][3] != 'Leader':
            # copy data
            tempDHTDict[key] = dhtDict[key].copy()

            # change node ID and renumber them
            nodeID += 1
            tempDHTDict[key][7] = nodeID

        # reset left and right ports since user left and right ports have been updated
        tempDHTDict[key][4] = userDict[key][4]
        tempDHTDict[key][5] = userDict[key][5]

        # remove records
        tempDHTDict[key].remove(tempDHTDict[key][8])

        # add empty records
        records = [[]] * 353
        tempDHTDict[key].append(records)

    # re-connect each node left and right ports
    global previousKey
    previousKey = decodeNewLeader
    node0 = decodeNewLeader
    for key in tempDHTDict.keys():
        # if there is only 1 node in the DHT
        if len(tempDHTDict) == 1:
            break
        # if there is nore than 1 node in the DHT
        else:
            # node 1 is the last node in the DHT
            if tempDHTDict[key][7] == 1 and tempDHTDict[key][7] == (len(tempDHTDict) - 1):
                # node 1 left port is equal to node 0 right port
                tempDHTDict[key][4] = tempDHTDict[previousKey][5]
                # node 1 right port is equal to node 0 left port
                tempDHTDict[key][5] = tempDHTDict[previousKey][4]
            # last node in the DHT is not node 1
            elif tempDHTDict[key][7] == (len(tempDHTDict) - 1):
                # last node left port is equal to left neighbor node right port
                tempDHTDict[key][4] = tempDHTDict[previousKey][5]
                # last node right port is equal to node 0 left port
                tempDHTDict[key][5] = tempDHTDict[node0][4]
            else:
                # if current node is node 0 store key in random variable
                if tempDHTDict[key][3] is 'Leader':
                    node0 = key
                # makes sure node 0 left and right ports are not updated
                if tempDHTDict[key][7] != 0:
                    # current node left port is eqal to left neighbor node right port
                    tempDHTDict[key][4] = tempDHTDict[previousKey][5]
                previousKey = key

    # store country records in corresponding node id
    for key in countriesDict.items():
        # find country's long name and find the sum of the ASCII value of each character
        word = countriesDict[key[0]][3]
        sumOfCharacters = sum(ord(ch) for ch in word)

        # calculate the position of the country that will be stored in the node
        position = sumOfCharacters % 353
        # calculate the node id the country record will be stored in
        storeInWhichNode = position % len(tempDHTDict)

        # store record in correct position and node
        for k, v in tempDHTDict.items():
            ID = tempDHTDict[k][7]
            if storeInWhichNode is ID:
                tempDHTDict[k][8][position] = countriesDict[key[0]].copy()

    # copy temporary dht dictionary data into dht dictionary
    dhtDict = {}
    for key in tempDHTDict.keys():
        dhtDict[key] = tempDHTDict[key].copy()

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

    # print(userDict)
    print(f'List of {len(dhtDict)} users that is in the rebuilt DHT')
    for key in dhtDict.keys():
        print(f'User: ({dhtDict[key][0]}) IP Address: ({dhtDict[key][1]}) Port Number: ({dhtDict[key][2]})')

    # empty temporary dht dictionary
    tempDHTDict = {}

    # sets lockout 3 to false meaning every other function can work now
    global lockout3
    lockout3 = False

    # send success to client
    returnCode = "SUCCESS: DHT has been rebuilt"
    serverSocket.sendto(returnCode.encode(), clientAddressRebuilt)


def server_deRegister():
    # receive username from client
    deRegisterUserName, clientAddressDeRegister = serverSocket.recvfrom(2048)

    # if teardown-complete wasn't executed after teardown-dht
    global lockout4
    if lockout4 is True:
        returnCode = "FAILURE: teardown-complete must be completed after teardown-dht"
        serverSocket.sendto(returnCode.encode(), clientAddressDeRegister)
        return

    # if rebuilt-dht wasn't executed after leave-dht
    global lockout3
    if lockout3 is True:
        returnCode = "FAILURE: dht-rebuilt must be completed after leave-dht or join-dht"
        serverSocket.sendto(returnCode.encode(), clientAddressDeRegister)
        return

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
    # receive username from client
    joinUserName, clientAddressJoin = serverSocket.recvfrom(2048)

    # decode username
    decodeUserName = joinUserName.decode()

    # if teardown-complete wasn't executed after teardown-dht
    global lockout4
    if lockout4 is True:
        returnCode = "FAILURE: teardown-complete must be completed after teardown-dht"
        serverSocket.sendto(returnCode.encode(), clientAddressJoin)
        return

    # if rebuilt-dht wasn't executed after leave-dht
    global lockout3
    if lockout3 is True:
        returnCode = "FAILURE: dht-rebuilt must be completed after leave-dht or join-dht"
        serverSocket.sendto(returnCode.encode(), clientAddressJoin)
        return

    # if setup-dht wasn't completed
    global lockout2
    if lockout2 is False:
        returnCode = "FAILURE: setup-dht must be completed first"
        serverSocket.sendto(returnCode.encode(), clientAddressJoin)
        return

    # if dht-complete wasn't execute after setup-dht
    global lockout1
    if lockout1 is True:
        returnCode = "FAILURE: dht-complete must be executed first right after setup-dht"
        serverSocket.sendto(returnCode.encode(), clientAddressJoin)
        return

    # check if username is already in dht
    for key in dhtDict.keys():
        if decodeUserName == key:
            returnCode = "FAILURE: user is already in dht"
            serverSocket.sendto(returnCode.encode(), clientAddressJoin)
            return

    # check if username is in user dictionary
    valid = False
    for key in userDict.keys():
        if decodeUserName == key:
            valid = True
            break
    if valid is False:
        returnCode = "FAILURE: user does not exist"
        serverSocket.sendto(returnCode.encode(), clientAddressJoin)
        return

    # check if username is in dht dictionary
    for key in dhtDict.keys():
        if decodeUserName == key:
            returnCode = "FAILURE: user is maintaining the DHT"
            serverSocket.sendto(returnCode.encode(), clientAddressJoin)
            return

    # FAILURE checks done

    # add username
    global addUserName
    addUserName = decodeUserName

    # Add user to the end of DHT
    userName = userDict[decodeUserName][0]
    ipAddress = userDict[decodeUserName][1]
    portNumber = userDict[decodeUserName][2]
    userDict[decodeUserName][3] = "InDHT"
    state = userDict[decodeUserName][3]
    leftPort = userDict[decodeUserName][4]
    rightPort = userDict[decodeUserName][5]
    queryPort = userDict[decodeUserName][6]
    dhtDict[decodeUserName] = [userName, ipAddress, portNumber, state, leftPort, rightPort, queryPort]

    # add node id (random number)
    dhtDict[decodeUserName].append(0)
    dhtDict[decodeUserName][7] = portNumber * 100

    # add records
    records = [[]] * 353
    dhtDict[decodeUserName].append(records)

    # renumber node IDs
    renumberNodeID = 0
    for key in dhtDict.keys():
        dhtDict[key][7] = renumberNodeID
        renumberNodeID += 1

    # re-connect left and right ports
    # reset left and right neighbors through left and right ports
    global nodeID, previousKey
    node0 = decodeUserName
    previousKey = decodeUserName

    # re-connects the ports to form a circle after node was removed
    for key in dhtDict:
        # remove records in order to update DHT an re-sort records again
        dhtDict[key].remove(dhtDict[key][8])
        dhtDict[key].append(records)

        # reset left and right ports
        dhtDict[key][4] = userDict[key][4]
        dhtDict[key][5] = userDict[key][5]

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

    # this makes sure that user has to rebuild dht first before removing another user from dht
    lockout3 = True

    # reset temporary dht dictionary
    global tempDHTDict
    tempDHTDict = {}

    returnCode = "SUCCESS: User joined the DHT"
    serverSocket.sendto(returnCode.encode(), clientAddressJoin)
    return


def server_teardownDHT():
    # receive username from client
    teardownUserName, clientAddressTeardown = serverSocket.recvfrom(2048)

    # decode username
    decodeUserName = teardownUserName.decode()

    # if rebuilt-dht wasn't executed after leave-dht
    global lockout3
    if lockout3 is True:
        returnCode = "FAILURE: dht-rebuilt must be completed after leave-dht or join-dht"
        serverSocket.sendto(returnCode.encode(), clientAddressTeardown)
        return

    # if setup-dht wasn't completed
    global lockout2
    if lockout2 is False:
        returnCode = "FAILURE: setup-dht must be completed first"
        serverSocket.sendto(returnCode.encode(), clientAddressTeardown)
        return

    # if dht-complete wasn't execute after setup-dht
    global lockout1
    if lockout1 is True:
        returnCode = "FAILURE: dht-complete must be executed first right after setup-dht"
        serverSocket.sendto(returnCode.encode(), clientAddressTeardown)
        return

    # list of keys
    dhtList = list(dhtDict.keys())

    # check if user is leader
    valid = True
    for key in dhtList:
        if key == decodeUserName:
            if str(dhtDict[key][3]) == 'Leader':
                valid = True
                break
    if valid is False:
        returnCode = "FAILURE: user is not leader or user is not in dht"
        serverSocket.sendto(returnCode.encode(), clientAddressTeardown)
        return

    # delete dht starting with node 1
    for key in list(dhtDict.keys()):
        if dhtDict[key][3] != 'Leader':
            dhtDict.pop(key)

    # delete leader
    dhtDict.pop(decodeUserName)

    # store leader
    global leaderUserName
    leaderUserName = decodeUserName

    # lockout
    global lockout4
    lockout4 = True

    # return code to client
    returnCode = "SUCCESS: DHT is deleted"
    serverSocket.sendto(returnCode.encode(), clientAddressTeardown)


def server_teardownComplete():
    # receive username from client
    teardownUserName, clientAddressTeardown = serverSocket.recvfrom(2048)

    # decode username
    decodeUserName = teardownUserName.decode()

    # if rebuilt-dht wasn't executed after leave-dht
    global lockout3
    if lockout3 is True:
        returnCode = "FAILURE: dht-rebuilt must be completed after leave-dht or join-dht"
        serverSocket.sendto(returnCode.encode(), clientAddressTeardown)
        return

    # if setup-dht wasn't completed
    global lockout2
    if lockout2 is False:
        returnCode = "FAILURE: setup-dht must be completed first"
        serverSocket.sendto(returnCode.encode(), clientAddressTeardown)
        return

    # if dht-complete wasn't execute after setup-dht
    global lockout1
    if lockout1 is True:
        returnCode = "FAILURE: dht-complete must be executed first right after setup-dht"
        serverSocket.sendto(returnCode.encode(), clientAddressTeardown)
        return

    # if user is not leader
    if decodeUserName != leaderUserName:
        returnCode = "FAILURE: user is not leader"
        serverSocket.sendto(returnCode.encode(), clientAddressTeardown)
        return

    # change all user states to free
    for key in userDict.keys():
        userDict[key][3] = "Free"

    # lockout is disabled
    global lockout4
    lockout4 = False
    lockout2 = False
    global lockout
    lockout = False

    # send return code to client
    returnCode = "SUCCESS: dht is completely deleted"
    serverSocket.sendto(returnCode.encode(), clientAddressTeardown)
    return


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
