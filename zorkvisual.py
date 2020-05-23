import os
import random
import re
import json
import sys
import pickle

inventorydata = []
# Location is a list of hex [North South, East West, Up Down]
playerdata = {'health':100,'location':[0x7F,0x7F,0x7F]}

def grammaran(string):
    #If the word starts with a vowel, a -> an
    vowels=['a','e','i','o','u']
    if vowels.count(string[0]):
        return('n '+string)
    else:
        return(' '+string)

def moveplayer():
    try:
        #if the direction is longer than 1 word, merge
        if len(commandinput)>2:
            movementdir=commandinput[1]+'_'+commandinput[2]
        else:
            movementdir=commandinput[1]
        #the value from the json
        movementvalue=openroom(playerdata['location'],'direction')[movementdir]
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
        print(openroom(playerdata['location'],'inspect')[commandinput[1]])
    except KeyError:
        print('You can\'t seem to find a'+grammaran(commandinput[1])+'.')

def opencontainer():
    itemlist=''
    couter=1
    try:
        if commandinput[1]=='the':
            commandinput.remove(commandinput[1])
        validitems = [x for x in openroom(playerdata['location'],'containers')[commandinput[1]]['items'] if x not in inventorydata]
        if len(openroom(playerdata['location'],'containers')[commandinput[1]]['items']) == 0:
            itemlist+='nothing'
        else:
            for item in validitems:
                if len(validitems)==couter:
                    itemlist+='a'+grammaran(item['name'])
                else: 
                    itemlist+='a'+grammaran(item['name'])+', and '
                couter+=1
        print('Inside the '+commandinput[1]+' you find '+itemlist+'.')
    except KeyError:
       print('You can\'t seem to find a'+grammaran(commandinput[1])+'.')

def openroom(loc, var):
    roomfile=''
    for num in range(0,3):
        roomfile=roomfile+str(hex(loc[num])[2:])
    with open(roomfile+'.json','r') as f:
        roomdata = json.load(f)
        return roomdata[var]

def quitgame():
    pickle.dump(playerdata,open('playerdata.pkl','wb'))
    pickle.dump(inventorydata,open('inventorydata.pkl','wb'))
    sys.exit('Quiting...')

def getitem():
    #get item from container
    if commandinput[2]=='from':
        commandinput.remove(commandinput[2])
        
    inventorydata.append([x for x in openroom(playerdata['location'],'containers')[commandinput[2]]['items'] if x["name"] == commandinput[1]][0])

commandslist = {'move':moveplayer, 'go':moveplayer, 'quit':quitgame,'exit':quitgame, 'inspect':inspect, 'look':inspect, 'open':opencontainer, 'get':getitem}

if __name__ == '__main__':
    try:
        playerdata = pickle.load(open('playerdata.pkl','rb'))
    except FileNotFoundError:
        print('Player data not found')
    try:
        inventorydata = pickle.load(open('inventorydata.pkl','rb'))
    except FileNotFoundError:
        print('Inventory data not found')

    print(openroom(playerdata['location'], 'name'))
    while True:
        try:
            commandinput=input('>>> ').casefold().split(' ')
        except KeyboardInterrupt:
             quitgame()
        try:
            commandaction = commandslist[commandinput[0].lower()]
            commandaction()
        except KeyError:
            print('Command not recoginized.')