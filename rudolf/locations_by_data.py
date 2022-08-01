import random
import json
from pprint import pprint
import random_dungeon

class room:
    def __init__(self, location):
        self.location = location
        self.description = ""
        self.monsters = []
        self.east = self.location
        #_data is just for "non standard" rooms like randomized dungeons or the like
        self.east_data = {}
        self.west = self.location
        self.west_data = {}
        self.south = self.location
        self.south_data = {}
        self.north = self.location
        self.north_data = {}
        self.area_type = "Wild"

def locate(location):

    location_type="static"
    location_file='rudolf/dungeon_data/locations.viridis.world.json'

    if(type(location) is dict):
        if 'name' in location: location_name = location['name']
        if 'type' in location: location_type = location['type']
        if 'file' in location: location_file = location['file']
    else:
        location_name=location

    data = None

    if location_type == "static":
        with open(location_file) as file:
            data = json.load(file)
        #print(type(data))
    if location_type == "random_dungeon":
        #TODO currently always a new dungeon is created. Dungeon should only be created new "as needed"
        data = random_dungeon.random_dungeon(location_name,location_file)

    # Error Handling: Aborts and returns False if no Data was returned
    if data is None:
        return False

    if location_name in data['locations']:
        #print(data['locations'][location])
        ldat=data['locations'][location_name]
        here = room(location_name)
        here.description = ldat['description']
        #TODO should be able to write this shorter. iterate through all simple strings ['east','north','area_type'] and so on
        if "east" in ldat:
            here.east = ldat['east']
        if "north" in ldat:
            here.north = ldat['north']
        if "south" in ldat:
            here.south = ldat['south']
        if "west" in ldat:
            here.west = ldat['west']
        if "area_type" in ldat:
            here.area_type = ldat['area_type']
        if "monsters" in ldat:
            for monster in ldat['monsters']:
                for i in range(monster['count']):
                    here.monsters.append(monster['name'])
    return here

        
        

    
