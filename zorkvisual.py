import os, random, re, simplify
floors=[]
floordata=[]
cleanedfloor=[]
nicefloors=[]
coll=[]
location=[0,0,0]
health=100
for file in os.listdir():
    if file[-4:]==".flr":
        floors.append(file)
for file in floors:
    openfile=open(file,"r")
    floordata=openfile.readlines()
    for line in floordata:
        line=re.sub("\/\/.+\\n","",line)
        line=line.replace("\n","")
        if line[:1]=="[":
            line=line.replace(" ","")
        cleanedfloor.append(line)
    nicefloors.append(cleanedfloor)
    cleanedfloor=[]
def searchfloor(loc,index):
    currentloc=str(loc).replace(" ","")
    for item in nicefloors:
        coll.append(item[index])
    try:
        room=coll.index(currentloc)
    except:
        print("oops that's an error")
        quit()
    newroom=nicefloors[room]
    return newroom
def userinput():
    userin=input(">>> ")
    userin=userin.lower()
    userin=simplify.simplify(userin)
    if userin=="move north":
        location[1]+=1
        print(searchfloor(location,0)[1])
    elif userin=="move south":
        location[1]-=1
        print(searchfloor(location,0)[1])
    elif userin=="move east":
        location[0]+=1
        print(searchfloor(location,0)[1])
    elif userin=="move west":
        location[0]-=1
        print(searchfloor(location,0)[1])
    elif userin=="describe":
        print(searchfloor(location,0)[2])

print (searchfloor(location,0)[1])
while health>0:
    userinput()
