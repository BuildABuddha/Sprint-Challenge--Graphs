from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
traversal_map = {}

def explore(way_back=None, last_movement=None, previous_room=None):
    
    current_room = player.current_room.id
    exits = player.current_room.get_exits()

    # Have we been here before? If so, remove last movement from travel path and go back.
    if current_room in traversal_map:
        traversal_map[previous_room][last_movement] = current_room
        traversal_path.pop(-1)
        player.travel(way_back)

    # Recursively explore each exit (except the way back)
    else:
        # Update the traversal map with what we've learned.
        traversal_map[current_room] = {direction: '?' for direction in exits}
        if previous_room is not None:
            traversal_map[current_room][way_back] = previous_room
            traversal_map[previous_room][last_movement] = current_room

        # Try to explore, north, east, south, and then west. 
        for direction, opposite_direction in [('n', 's'), ('e', 'w'), ('s', 'n'), ('w', 'e')]:
            if direction in traversal_map[current_room] and direction != way_back:
                traversal_path.append(direction)
                player.travel(direction)
                explore(opposite_direction, direction, current_room)

        # Once we've explored all paths, go back the way we came. 
        if way_back is not None:
            traversal_path.append(way_back)
            player.travel(way_back)

# Now... go explore!
explore()

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
