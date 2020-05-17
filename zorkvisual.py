import os, random, re, json, sys
floors=[]
floordata=[]
cleanedfloor=[]
nicefloors=[]
coll=[]
location=[0x7F,0x7F,0x7F]
health=100
errcodes={1:"Direction not found",2:"Something is blocking the way"}
def moveplayer():
    try:
        errorcode=0
        global location
        if len(commandinput)>2:
            movementdir=commandinput[1]+"_"+commandinput[2]
        else:
            movementdir=commandinput[1]
        movementvalue=openroom(location,"direction")[movementdir]
        if movementvalue==True:
            print("Moving "+movementdir.replace("_"," "))
        elif movementvalue==False:
            errorcode=2
        else:
            print(movementvalue)
    except KeyError:
        errorcode=1        
    return errorcode

def openroom(loc, var):
    roomfile=''
    for num in range(0,3):
        roomfile=roomfile+str(hex(loc[num])[2:])
    with open(roomfile+'.json') as f:
        roomdata = json.load(f)
        return roomdata[var]
def quitgame():
    sys.exit("Quiting...")
commands={'move':moveplayer,'go':moveplayer,"quit":quitgame,"exit":quitgame}

if __name__ == '__main__':
    print(openroom(location, "name"))
    while True:
        try:
            commandinput=input('>>> ').casefold().split(' ')
        except KeyboardInterrupt:
           quitgame()
        commandaction=commands[commandinput[0].lower()]
        error=commandaction()
        if error!=0:
            print(errcodes[error])