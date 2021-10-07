# dictionary
myDict = {"Name": [], "Address": [], "Age": []}

# adding values to keys
myDict["Name"].append("alex")
myDict["Name"].append("adam")
myDict["Address"].append("phoenix")
myDict["Address"].append("tucson")
myDict["Age"].append(21)

# print dictionary
print(myDict)

# search for key in dictionary
print("Name" in myDict.keys())      # true if string is found, false if not found

# search for value
print("adam" in myDict["Name"])     # true if string is found, false if not found

# search for value
value = "alex"
key = "Name"
print(value in myDict[key])         # true if string is found, false if not found

# print value
print(myDict.values())      # only prints values
print(myDict.items())       # prints values with their respective keys
print(myDict.keys())   # prints the names of the keys
print(myDict["Name"][0])    # prints a specific index of a key

# delete element from dictionary
value = "tucson"
for v in myDict.values():   # .values() only looks at elements not keys
    if value in v:          # check if the value and v are the same
        v.remove(value)     # delete value
        print(myDict)

# delete key (with all of its elements) from dictionary
key = "Age"
myDict.pop(key)     # pop is more useful than del
print(myDict)
