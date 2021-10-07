import random
from socket import *
import sys
import csv

# dictionaries (don't delete)
userDict = {}
dhtDict = []
# countriesDict = {}
countriesDict = {"Country Code": [], "Short Name": [], "Table Name": [], "Long Name": [], "2-Alpha Code": [],
                 "Currency Unit": [], "Region": [], "WB-2 Code": [], "Latest Population Census": []}


def setupCountriesDict():
    # open csv file
    # countriesDict = {"Country Code": [], "Short Name": [], "Table Name": [], "Long Name": [], "2-Alpha Code": [], "Currency Unit": [], "Region": [], "WB-2 Code": [], "Latest Population Census": []}
    file = open('StatsCountry.csv', 'r', encoding='unicode_escape')
    # read csv values
    reader = csv.reader(file)
    # skip header
    next(reader, None)
    # store csv values separately as key-value pairs in a dictionary
    for row in reader:
        # print(row[0])
        countriesDict["Country Code"].append(row[0])
        countriesDict["Short Name"].append(row[1])
        countriesDict["Table Name"].append(row[2])
        countriesDict["Long Name"].append(row[3])
        countriesDict["2-Alpha Code"].append(row[4])
        countriesDict["Currency Unit"].append(row[5])
        countriesDict["Region"].append(row[6])
        countriesDict["WB-2 Code"].append(row[7])
        countriesDict["Latest Population Census"].append(row[8])
        # countriesDict['{\'Country Code\': \'' + row[0] + '\'}'] = {'Short Name': row[1], 'Table Name': row[2],
        #                                                          'Long Name': row[3], '2-Alpha Code': row[4],
        #                                                          'Currency Unit': row[5], 'Region': row[6],
        #                                                          'WB-2 Code': row[7],
        #                                                          'Latest Population Census': row[8]}
    print(countriesDict)  # test countriesDict


def setupUser():
    decodeName = input("Enter decode Name: ")
    decodeIP = input("Enter decode IP: ")
    decodePort = input("Enter decode Port: ")
    state = "free"

    userDict[decodeName] = decodeIP, decodePort, state


def setupDHTdict():
    dhtSize = input("Enter size of DHT")
    dhtSize = int(dhtSize)

    usernames = userDict.keys()
    for rowIndex in range(dhtSize):
        word = countriesDict["Long Name"][rowIndex]
        sumOfChar = sum(ord(ch) for ch in word)

        pos = sumOfChar % 353
        id = (pos % dhtSize) - 1
        
        #Calculate pos and id for all values in countries Dictionary and store dhtdict with collisions
        
        print(id)
        # if rowIndex == 0:
        #    dhtDict[id] = decodeName
        #
        #    userDict[decodeName][2] = "leader"
        #
        # else:
        #   index = random.randint(0,len(usernames)-1)
        #   leaderCheck = true
        #    while leaderCheck:
        #        leaderCheck == (usernames[index] == decodeName)
        #    dhtDict[id] = usernames[index]
        #    userDict[usernames[index]][2] = "INDHT"


setupCountriesDict()

# for x in range(6):
#  setupUser()

# print(userDict)

setupDHTdict()
