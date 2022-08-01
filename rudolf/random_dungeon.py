import random
import json
from pprint import pprint

"""
  Coordinates
  xy  xy  xy  xy  xy
  00  10  20  30  40
  01  11  21  31  41
  02  12  22  32  42
  03  13  23  33  43
"""

directions={
    "1":{ "name":"north",  "x" : 0, "y" : -1, "opp" : "2"},
    "2":{ "name":"south",  "x" : 0, "y" :  1, "opp" : "1"},
    "3":{ "name":"east" ,  "x" : 1, "y" :  0, "opp" : "4"},
    "4":{ "name":"west" ,  "x" :-1, "y" :  0, "opp" : "3"}
}

def random_dungeon(location,location_file):
    print("random dungeon. location_file:" + location_file)
    with open(location_file) as file:
        data = json.load(file)
    #DungeonData
    duda={}
    #DungeonEntryData
    ed=data["locations"][location]
    x=ed["x"]
    y=ed["y"]
    #Create x dict if it doesn't exist'
    if not x in duda: duda[x]={}
    
    #just initialize opposite direction with non direction
    odir=5
    cdir=0
    
    duda[x][y]=ed
    duda[x][y]["name"]=location
    prev_room_name=location
    
    noreturn=data["dungeon_settings"]["noreturn"]

    for i in range(data["dungeon_settings"]["steps"]):
        print("room " + str(i))
        #possible directions
        pdir=[]
        for dir in directions:
            #print("direction: " + directions[dir]["name"])
            ny=y + directions[dir]["y"]
            nx=x + directions[dir]["x"]
            if (ny) in range(data["dungeon_settings"]["height"]) and ( #not out of y coordinates
                nx) in range(data["dungeon_settings"]["width"])  and ( #not out of x coordinates
                dir != odir ):# not in opposite direction
                doappend=True
                
                #Check if Room already exists
                if nx in duda:
                    if ny in duda[nx] and len(pdir) > 0 and noreturn <=0: #allow direction if there is no other possible direction (would end in error then)
                        doappend=False #if Room already exists do not go this direction
                    else:
                        noreturn=data["dungeon_settings"]["noreturn"] #reset noreturn
                if doappend:
                    #more weight for same direction
                    if dir == cdir:
                        for j in range(data["dungeon_settings"]["samedirection"]):
                            pdir.append(dir) #append multiple times
                    else:
                        pdir.append(dir)
        noreturn-=1
                
        print("possible directions: " +','.join(pdir))
        #print("possible directions len: " + str(len(pdir)))
        #chosen direction
        cdir=pdir[random.randint(0,len(pdir)-1)]
        #opposite direction
        odir=directions[cdir]["opp"]
        print("chosen direction: " + str(cdir))
        
        px = x
        py = y
        x = x + directions[cdir]["x"]
        y = y + directions[cdir]["y"]
        
        #corridor from previous room to new room
        duda[px][py][directions[cdir]["name"]]={
            "name" : (data["dungeon_settings"]["name"] + " " + str(x) + " " + str(y)),
            "type" : "random_dungeon",
            "file" : location_file
        }
        
    
        if not x in duda: duda[x]={}
        
        #If room already exists make an additional direction there
        if y in duda[x]:
            oppDirName=directions[odir]["name"]
            duda[x][y][oppDirName]={
                "name" : duda[px][py]["name"],
                "type" : "random_dungeon",
                "file" : location_file
            }
        else:
            duda[x][y]={
                "x": x,
                "y": y,
                "name" : (data["dungeon_settings"]["name"] + " " + str(x) + " " + str(y)),
                "description" : (data["dungeon_settings"]["name"] + " " + str(x) + " " + str(y)),
                directions[odir]["name"] : {
                    "name" : prev_room_name,
                    "type" : "random_dungeon",
                    "file" : location_file
                }
            }

        #save number of step for showing in debug render
        if 'stepnr' in duda[x][y]:
            duda[x][y]['stepnr'].append(i)
        else:
            duda[x][y]['stepnr']=[i]
    
    #Dumping and writing File is for testing purposes now
    #want to visually see if dungeon makes sense
    print(json.dumps(duda,indent=2))
    
    outfile=open("test_output/random_dungeon.html","w")
    out=''
    out+="""
    <html>
        <head>
        <title>Random Dungeon</title>
        <style>
            body {
                background: black;
            }
            table {
                border-spacing: 1px;
                /*border-collapse: collapse;*/
            }
            td{
                height:100px;
                width:100px;
            }
            td.block {
                border: 20px solid black;
                background-color: #111111;
                height:100px;
                width:100px;

            }
            td.room {
                border: 20px solid black;
                background-color: #cccccc;
                height:100px;
                width:100px;

            }
            td.north {
                border-top: 20px solid #cccccc;
            }
            td.south {
                border-bottom: 20px solid #cccccc;
            }
            td.east {
                border-right: 20px solid #cccccc;
            }
            td.west {
                border-left: 20px solid #cccccc;
            }
        </style>
    </html>
    """
    
    out+='<table>'
    for y in range(data["dungeon_settings"]["height"]):
        out+='<tr>'
        for x in range(data["dungeon_settings"]["width"]):
            if x in duda and y in duda[x]:
                classes=['room']
                for key in duda[x][y]:
                    if key in ["north","south","east","west"]:
                        classes.append(key)
                #cell content
                if 'stepnr' in duda[x][y]:
                    cont=str(duda[x][y]['stepnr'])
            else:
                classes=['block']
                cont=""
            out+='<td class="' + ' '.join(classes) + '">'
            out+=cont
            out+='</td>'
            
        out+='</tr>'
    out+='</table>'
    
    outfile.write(out)
    outfile.close()