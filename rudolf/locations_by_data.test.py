import locations_by_data
from pprint import pprint


#my_here=locations_by_data.locate("Kingdom Street")
#if my_here:
#    pprint(vars(my_here))
#
#print("\n\n--------------------------------------\n\n")
#
#my_here=locations_by_data.locate("Tavern")
#if my_here:
#    pprint(vars(my_here))
#
#print("\n\n--------------------------------------\n\n")
#
#my_here=locations_by_data.locate("Deep Slime Forest")
#if my_here:
#    pprint(vars(my_here))

my_here=locations_by_data.locate(location="entry",location_type="random_dungeon",location_file="rudolf/deep_slime_forest.dungeon.json")
if my_here:
    pprint(vars(my_here))