import os, random, re, simplify
floors=[]
floordata=[]
cleanedfloor=[]
nicefloors=[]
coll=[]
location=[0x7F,0x7F,0x7F]
health=100
movementdir={'north':1,'east':2,'south':3,'west':4,'up':5,'down':6}

def moveplayer():
    print("moved "+str(movementdir[userin.split(' ')[1].lower()]))

def openroom(loc):
    roomfile=''
    for num in range(0,3):
        roomfile=roomfile+str(hex(loc[num])).replace("0x","")
    room = open(roomfile+".flr",'r')
    print(room.readlines()[0])
    room.close()

commands={'move':moveplayer}

if __name__ == '__main__':
    openroom(location)
    userin=input('>>> ')
    commandaction = commands[userin.split(' ')[0].lower()]
    commandaction()