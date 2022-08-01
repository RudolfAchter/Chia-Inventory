import locations_by_data
from pprint import pprint
import settings


my_here=locations_by_data.locate("Kingdom Street")
if my_here:
    pprint(vars(my_here))

print("\n\n--------------------------------------\n\n")

my_here=locations_by_data.locate("Tavern")
if my_here:
    pprint(vars(my_here))

print("\n\n--------------------------------------\n\n")

my_here=locations_by_data.locate("Deep Slime Forest")
if my_here:
    pprint(vars(my_here))


print("\n\n--------------------------------------\n\n")

my_loc={
    "name": "entry",
    "file": "deep_slime_forest.random_dungeon.json",
    "type": "random_dungeon"
}

my_here=locations_by_data.locate(my_loc)
if my_here:
    pprint(vars(my_here))
    

#FIXME filepath is wrong
#for dir in ["north","south","east","west"]:
#    if(hasattr(my_here,dir)):
#        my_here=locations_by_data.locate(getattr(my_here, dir))