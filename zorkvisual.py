import os
import random
import re
import json
import sys
import pickle

inventorydata = []
playerdata = {'health':100,'location':[0x7F,0x7F,0x7F]}

def grammaran(string):
    #If the word starts with a vowel, a -> an
    vowels=["a","e","i","o","u"]
    if vowels.count(string[0]):
        return("n "+string)
    else:
        return(" "+string)

def moveplayer():
    try:
        #if the direction is longer than 1 word, merge
        if len(commandinput)>2:
            movementdir=commandinput[1]+"_"+commandinput[2]
        else:
            movementdir=commandinput[1]
        #the value from the json
        movementvalue=openroom(playerdata['location'],"direction")[movementdir]
        if movementvalue==True:
            print("Moving "+movementdir.replace("_"," ")+".")
            #TODO: actually update player location and read title & description
        elif movementvalue==False:
            print("Something is blocking the way.")
        else:
            print(movementvalue)
    except KeyError:
        print("Direction not found.")     

def inspect():
    if commandinput[1]=="at":
        commandinput.remove(commandinput[1])
    try:
        print(openroom(playerdata['location'],"inspect")[commandinput[1]])
    except KeyError:
        print("You can't seem to find a"+grammaran(commandinput[1])+".")

def opencontainer():
    itemlist=""
    couter=1
    try:
        if commandinput[1]=="the":
            commandinput.remove(commandinput[1])
        if len(openroom(playerdata['location'],"container")[commandinput[1]]) == 0:
            itemlist+="nothing"
        else:
            for item in openroom(playerdata['location'],"container")[commandinput[1]]:
                if len(openroom(playerdata['location'],"container")[commandinput[1]])==couter:
                    itemlist+="a"+grammaran(item)
                else: 
                    itemlist+="a"+grammaran(item)+", and "
                couter+=1
        print("Inside the "+commandinput[1]+" you find "+itemlist+".")
    except KeyError:
        print("You can't seem to find a"+grammaran(commandinput[1])+".")

def openroom(loc, var):
    roomfile=''
    for num in range(0,3):
        roomfile=roomfile+str(hex(loc[num])[2:])
    with open(roomfile+'.json','r') as f:
        roomdata = json.load(f)
        return roomdata[var]

def quitgame():
    pickle.dump(playerdata,open('playerdata.pickle','wb'))
    pickle.dump(inventorydata,open('inventorydata.pickle','wb'))
    sys.exit("Quiting...")

#def getitem():



commands={'move':moveplayer,'go':moveplayer,"quit":quitgame,"exit":quitgame,"inspect":inspect,"look":inspect,"open":opencontainer}

if __name__ == '__main__':

    try:
        playerdata = pickle.load(open('playerdata.pickle','rb'))
    except FileNotFoundError:
        pass
    try:
        inventorydata = pickle.load(open('inventorydata.pickle','rb'))
    except FileNotFoundError:
        pass

    print(openroom(playerdata['location'], "name"))
    while True:
        try:
            commandinput=input('>>> ').casefold().split(' ')
        except KeyboardInterrupt:
            quitgame()
        try:
            commandaction = commands[commandinput[0].lower()]
            commandaction()
        except KeyError:
            print("Command not recoginized.")