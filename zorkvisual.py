import os
import random
import re
import json
import sys
import pickle
inventoryData = []
# Location is a list of hex [North South, East West, Up Down]
playerData = {'health':100,'location':[0x7F,0x7F,0x7F]}

def grammarAn(string):
    #If the word starts with a vowel, a -> an
    vowels=['a','e','i','o','u']
    if vowels.count(string[0]):
        return('n '+string)
    else:
        return(' '+string)

def movePlayer():
    try:
        #if the direction is longer than 1 word, merge
        if len(commandinput)>2:
            movementdir=commandinput[1]+'_'+commandinput[2]
        else:
            movementdir=commandinput[1]
        #the value from the json
        movementvalue=openRoom(playerdata['location'],'direction')[movementdir]
        if movementvalue==True:
            print('Moving '+movementdir.replace('_',' ')+'.')
            #TODO: actually update player location and read title & description
        elif movementvalue==False:
            print('Something is blocking the way.')
        else:
            print(movementvalue)
    except KeyError:
        print('Direction not found.')     

def inspect():
    if commandinput[1]=='at':
        commandinput.remove(commandinput[1])
    try:
        print(openRoom(playerData['location'],'inspect')[commandinput[1]])
    except KeyError:
        print('You can\'t seem to find a'+grammarAn(commandinput[1])+'.')

def isLocked(lockContainer):
    if 'Locked' in openRoom(playerData['location'],'Containers')[lockContainer]:
        keyItem = [x for x in inventoryData if x['UUID'] == openRoom(playerData['location'],'Containers')[lockContainer]['Locked']['KeyItem']]
        if keyItem:
            return False
        else:
            return True
    else:
        return False

def openContainer():
    itemlist=''
    couter=1
    if isLocked(commandinput[1]):
        print(openRoom(playerData['location'],'Containers')[commandinput[1]]['Locked']['LockMessage'])
    else:
        try:
            if commandinput[1]=='the':
                commandinput.remove(commandinput[1])
            #put each item that is not in the players inventory into a list
            validItems = [x for x in openRoom(playerData['location'],'Containers')[commandinput[1]]['Items'] if x not in inventoryData]
            #If the list is empty
            if len(validItems) == 0:
                itemlist+='nothing'
            else:
                for item in validItems:
                    if len(validItems)==couter:
                        #if there is one item or is the last item in the list
                        itemlist+='a'+grammarAn(item['Name'])
                    else: 
                        itemlist+='a'+grammarAn(item['Name'])+', and '
                    couter+=1
            print('Inside the '+commandinput[1]+' you find '+itemlist+'.')
        except KeyError:
            print('You can\'t seem to find a'+grammarAn(commandinput[1])+'.')

def openRoom(loc, var):
    roomfile=''
    for num in range(0,3):
        roomfile=roomfile+str(hex(loc[num])[2:])
    with open(roomfile+'.json','r') as f:
        roomdata = json.load(f)
        return roomdata[var]

def quitGame():
    pickle.dump(playerdata,open('playerdata.pkl','wb'))
    pickle.dump(inventorydata,open('inventorydata.pkl','wb'))
    sys.exit('Quiting...')

def getItem():
    #get item from container
    if commandinput[2]=='from':
        commandinput.remove(commandinput[2])
    if isLocked(commandinput[2]):
        print(openRoom(playerData['location'],'Containers')[commandinput[2]]['Locked']['LockMessage'])
    else:
        try:
            inventoryData.append([x for x in openRoom(playerData['location'],'Containers')[commandinput[2]]['Items'] if x['Name'] == commandinput[1]][0])
            print('You pick up the '+commandinput[1]+'.')
        except KeyError:
            print('You can\'t seem to find a'+grammarAn(commandinput[2])+'.')
        except IndexError:
            print('You can\'t seem to find a'+grammarAn(commandinput[1]+' in the '+commandinput[2]+'.'))

commandslist = {'move':movePlayer, 'go':movePlayer, 'quit':quitGame,'exit':quitGame, 'inspect':inspect, 'look':inspect, 'open':openContainer, 'get':getItem}

if __name__ == '__main__':
    try:
        playerdata = pickle.load(open('playerdata.pkl','rb'))
    except FileNotFoundError:
        print('Player data not found')
    try:
        inventorydata = pickle.load(open('inventorydata.pkl','rb'))
    except FileNotFoundError:
        print('Inventory data not found')

    print(openRoom(playerData['location'], 'Name'))

    while True:
        try:
            commandinput=input('>>> ').casefold().split(' ')
            for item in commandinput:
                if item=="the":
                    commandinput.remove(item)
        except KeyboardInterrupt:
             quitGame()
        try:
            commandaction = commandslist[commandinput[0].lower()]
            commandaction()
        except KeyError:
            print('Command not recoginized.')