from room import Room
from player import Player
from world import World

import random
from ast import literal_eval
from utils import Stack, Queue

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
#sanity check length of room list in txt file
print(f"room_graph length: {len(room_graph)}" )


# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []


graph = {}
visited = set()
visitcount = 0

def backup(last_dir):
    backtrack = {'n':'s', 's':'n', 'e':'w', 'w':'e'}
    return backtrack[last_dir]

def randomizer(room_id, doors):
    if len(doors) > 1:
        rando = random. randint(1,len(doors)-1)
        print(f"from randomizer {room_id} {doors[rando]}")
        return doors[rando]
    else:
        return doors[0]

src = None
prev_room = None

while len(visited) < len(room_graph):
    print()
    print(f"round {visitcount} ", end='==============')
    print()
    current_room = player.current_room.id
    # print(current_room)
    visited.add(current_room)

    if current_room not in graph:
        graph[current_room] = {}

        for exit in player.current_room.get_exits():
            graph[current_room][exit] = '?'
    
    availrooms = [key for key,val in graph[current_room].items() if val == '?']

    if len(availrooms) > 0:
        visitcount += 1
        print(f"where am I?: {current_room}")
        print(f"and where have i been? : {visited}") 
        print(f"what is already in graph? : {graph}")
        direction = randomizer(player.current_room.id, availrooms)
        player.travel(direction)
        graph[current_room][direction] = player.current_room.id
        go_back = backup(direction)
        old_room = current_room
        traversal_path.append(direction)
    
    else:
        def backtrack(graph,player):
            q = Queue()
            exploredrooms = set()

            q.enqueue([(player.current_room.id, None)])

            while q.size() > 0 :
                curr_path = q.dequeue()
                lastroom = curr_path[-1][0]

                if '?' in graph[lastroom].values():
                    path = []
                    for p in curr_path:
                        path.append(p[1])
                    print(f"p {p}")
                    return path

                if lastroom not in exploredrooms:
                    exploredrooms.add(lastroom)

                    for k,v in graph[lastroom].items():
                        path_copy = list(curr_path)
                        path_copy.append((v,k))
                        q.enqueue(path_copy)
        retrace_steps = backtrack(graph, player)

        for steps in retrace_steps:
            player.travel(steps)
            traversal_path.append(steps)



# previous failed attempts

# last_dir = None
# prev_room = None


# #sanity check
# # print(player.current_room.id)
# # print(player.current_room.get_exits())
# #['n', 's', 'w', 'e']

# def randomizer(room_id, doors):
#     if len(doors) > 1:
#         rando = random. randint(1,len(doors)-1)
#         print(f"from randomizer {room_id} {doors[rando]}")
#         return doors[rando]
#     else:
#         return doors[0]

# def backup(last_dir):
#     backtrack = {'n':'s', 's':'n', 'e':'w', 'w':'e'}
#     return backtrack[last_dir]



# while len(visited)< len(room_graph):
#     curr_room = player.current_room.id
#     visited.add(curr_room)
    

#     print()
#     print(f"round {visitcount} ", end='==============')
#     print()
#     print(f"where am I?: {curr_room}")
#     print(f"and where have i been? : {visited}") 
#     print(f"what is already in graph? : {graph}")
#     visitcount += 1

#     if curr_room not in graph:
#         graph[curr_room] = {}
#         for doors in player.current_room.get_exits():
#             graph[curr_room][doors] = '?'

#     availdoors = []
#     for k,v in graph[player.current_room.id].items():
#         if v == '?':
#             availdoors.append(k)
#     print(f"what doors are still avail? : {availdoors}")
    

#     if len(availdoors) > 0:
#         print(player.current_room.id)
#         #return a random door from the availdoors, or returns the only avail door left if there is only one to avoid collisions.   
#         direction = randomizer(curr_room, availdoors)
#         print(f"which way do we go? : {direction}")
#         #move to the next room
#         prev_room = curr_room
#         last_dir = direction
#         player.travel(direction)
#         print(curr_room)
#         print(prev_room)
#         graph[curr_room][direction] = player.current_room.id
#         if graph[prev_room][backup(last_dir)] in graph:
#             graph[prev_room][backup(last_dir)] = prev_room
#         prev_room = curr_room
        
#         go_back = backup(last_dir)
#         traversal_path.append(direction)
    
#         print()
#         print(f"sanity check, where am now? : {player.current_room.id}") 
#         print(f"how do i get back to {prev_room} : {go_back} ")
    
#     else:
#         break
        
                    

# print(f"traversal_path {traversal_path}")



# TRAVERSAL TEST
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
