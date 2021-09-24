from socket import *

serverPort = 11050
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print("RUNNING")


def server_register():
    # receive username, ip address, and port number from client
    regName, clientAddress = serverSocket.recvfrom(2048)
    regIP, clientAddress = serverSocket.recvfrom(2048)
    regPort, clientAddress = serverSocket.recvfrom(2048)

    # decode username, ip address, and port number
    decodeName = regName.decode()
    decodeIP = regIP.decode()
    decodePort = regPort.decode()

    success = "SUCCESS"

    # return success message to client
    serverSocket.sendto(success.encode(), clientAddress)


def server_setupDHT():
    print(2)


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
