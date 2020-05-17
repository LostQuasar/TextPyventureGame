import os, random, re, json, sys
floors=[]
floordata=[]
cleanedfloor=[]
nicefloors=[]
coll=[]
location=[0x7F,0x7F,0x7F]
health=100

def grammaran(string):
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
        movementvalue=openroom(location,"direction")[movementdir]
        if movementvalue==True:
            print("Moving "+movementdir.replace("_"," ")+".")
            #TODO: actually update room and read title & description
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
        print(openroom(location,"inspect")[commandinput[1]])
    except KeyError:
        print("You can't seem to find a"+grammaran(commandinput[1])+".")

def opencontainer():
    itemlist=""
    couter=1
    try:
        if commandinput[1]=="the":
            commandinput.remove(commandinput[1])
        for item in openroom(location,"container")[commandinput[1]]:
            if len(openroom(location,"container")[commandinput[1]])==couter:
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
    with open(roomfile+'.json') as f:
        roomdata = json.load(f)
        return roomdata[var]
def quitgame():
    sys.exit("Quiting...")

commands={'move':moveplayer,'go':moveplayer,"quit":quitgame,"exit":quitgame,"inspect":inspect,"look":inspect,"open":opencontainer}

if __name__ == '__main__':
    print(openroom(location, "name"))
    while True:
        try:
            commandinput=input('>>> ').casefold().split(' ')
        except KeyboardInterrupt:
           quitgame()
        try:
            commandaction=commands[commandinput[0].lower()]
            commandaction()
        except KeyError:
            print("Command not recoginized.")