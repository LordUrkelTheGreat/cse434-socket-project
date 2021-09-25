from socket import *
import sys

arr = []
dht = []

# do not delete
# serverPort = int(sys.argv[1])

# if serverPort < 11000 or serverPort > 11500:
#   print("Error: Port number must be in the range of 11000-11500")
#   exit()

# this is for running on PC not asu general
serverPort = 11000

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print("RUNNING")


class UserInfo:
    def __init__(self, userName, ipAddr, portNum, state):
        self.userName = userName
        self.ipAddr = ipAddr
        self.portNum = portNum
        self.state = state
        #self.dhtLineNo =

class DHT:
    def __init__(self, countryCode, shortName, tableName, longName, twoAlphaCode,currencyUnit,region,wb2Code,latestPopulationCensus):
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
    regName, clientAddress = serverSocket.recvfrom(2048)
    regIP, clientAddress = serverSocket.recvfrom(2048)
    regPort, clientAddress = serverSocket.recvfrom(2048)

    # random boolean statement set to true as default
    valid = True
    valid1 = False

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
        valid1 = True
        # update return code statement and send it back to client
        returnCode = "SUCCESS"
        serverSocket.sendto(returnCode.encode(), clientAddress)

    # checks if username exists in the array. if it does,
    # then return FAILURE to indicate that register function
    # failed to create new user
    if valid1 == False:
        for user in arr:
            if user.userName == decodeName or user.portNum == decodePort:
                returnCode = "FAILURE: Username already exists or port number is already in use"
                serverSocket.sendto(returnCode.encode(), clientAddress)
                valid = False
                break

    # checks if valid is true if the above for loop changed it
    # if valid == True:
        # add decoded information to array via userInfo
        # arr.append(UserInfo(decodeName, decodeIP, decodePort, state))
        # print statements
        # print(f'Username: {decodeName}')
        # print(f'IP Address: {decodeIP}')
        # print(f'Port Number: {decodePort}')
        # print(f'State: {state}')
        # print(f'Values are stored')
        # update return code statement and send it back to client
        # returnCode = "SUCCESS"
        # serverSocket.sendto(returnCode.encode(), clientAddress)


def server_setupDHT():
    # receive n and username from client
    setupN, clientAddress = serverSocket.recvfrom(2048)
    setupUserName, clientAddress = serverSocket.recvfrom(2048)

    # random boolean statement set to false by default
    valid = False

    # decode n and username
    decodeN = setupN.decode()
    decodeName = setupUserName.decode()
    
    #Set up the .csv file into the dht array
    file = open("StatsCountry.csv", "r")
    file.readline()
    lines = []
    for f in file:
        line = file.readline()
        data = line.split(",")
        print(data)
        if len(data) > 1:
            dht.append(DHT(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8].rstrip()))

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


def server_deRegister():
    # receive username from client
    deRegisterUserName, clientAddress = serverSocket.recvfrom(2048)

    # random boolean variable set to false by default
    statement = False

    # decode username
    decodeName = deRegisterUserName.decode()

    # finds user
    for person in arr:
        # if the username is the same as the decode name and its state is Free
        if person.userName == decodeName and person.state == "Free":
            print(person.ipAddr)
            # delete user and their info
            statement = True
            # update return code statement and send it back to client
            returnCode = "SUCCESS"
            serverSocket.sendto(returnCode.encode(), clientAddress)
            break

    # if the user wasn't found or the state isn't Free
    if statement == False:
        # update return code statement and send it back to client
        returnCode = "FAILURE: The user is a node maintaining the DHT or user doesn't exist"
        serverSocket.sendto(returnCode.encode(), clientAddress)


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
    print(command)

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
