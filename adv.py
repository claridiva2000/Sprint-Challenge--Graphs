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
map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)



# To solve this path, you'll want to construct your own traversal graph. You start in room `0`, which contains exits `['n', 's', 'w', 'e']`. Your starting graph should look something like this:

# ```
# {
#   0: {'n': '?', 's': '?', 'w': '?', 'e': '?'}
# }
# ```

#sanity check
# print(player.current_room.id)
# print(player.current_room.get_exits())
#['n', 's', 'w', 'e']

starting_graph={}
starting_graph[0] = dict()
# print(starting_graph)
#sanity check ok. graph exists and there's stuff in it.

mysteryrooms = player.current_room.get_exits()
# print(f"mysteryrooms sanity check: {mysteryrooms}")

#add rooms to starting_graph[0] as '?'
for room in mysteryrooms:
    starting_graph[0][room] = '?'
# print(f"starting_graph loaded{starting_graph}")
#sanity check ==> starting_graph loaded{0: {'n': '?', 's': '?', 'w': '?', 'e': '?'}}

#sanity check length of room list in txt file
print(f"room_graph length: {len(room_graph)}" )




def randomizer(room_id, doors):
    if len(doors) > 1:
        rando = random. randint(1,len(doors)-1)
        print(f"from randomizer {room_id} {doors[rando]}")
        return doors[rando]
    else:
        return doors[0]

def backup(last_dir):
    backtrack = {'n':'s', 's':'n', 'e':'w', 'w':'e'}
    return backtrack[last_dir]





graph = starting_graph
visited = set()
path = []
visitcount = 1
last_dir = None
prev_room = None

visited.add(0)

while len(visited)< len(room_graph):
    curr_room = player.current_room.id
    visited.add(curr_room)
    

    print()
    print(f"round {visitcount} ", end='==============')
    print()
    print(f"and where have i been? : {visited}") 
    print(f"what is already in graph? : {graph}")
    visitcount += 1

    if curr_room not in graph:
        graph[curr_room] = {}

        for doors in player.current_room.get_exits():
            graph[curr_room][doors] = '?'

    availdoors = []
    for k,v in graph[player.current_room.id].items():
        if v == '?':
            availdoors.append(k)
    print(f"what doors are still avail? : {availdoors}")

    if len(availdoors) > 0:
        #choose a random door from the available ? doors. return 'n' 's' 'e' or 'w'. 
        # if there is only one door left it automatically takes it to avoid collisions.
        direction = randomizer(curr_room, availdoors)
        print(f"which way do we go? : {direction}")
        prev_room = curr_room
        player.travel(direction)
        graph[curr_room][direction] = player.current_room.id
        last_dir = direction
        go_back = backup(last_dir)
        path.append(direction)
    
        print()
        print(f"sanity check, where am now? : {player.current_room.id}") 
        print(f"how do i get back to {prev_room} : {go_back} ")
    
    else:
        def backtrack_rooms(graph, player):
            
            q=Queue()
            finished_rooms = set()

            q.enqueue([player.current_room.id])
            print(f"what's in q right now?: {q}")

            while q.size() > 0:
                curr_path = q.dequeue()
                last_room = curr_path[-1][0]

                if '?' in graph[last_room].values():
                    return [i[1] for i in curr_path[:1]]

                if last_room not in visited:
                    finished_rooms.add(last_room)
                    for key, val in graph[last_room].items():
                        path_copy = list(curr_path)
                        path_copy.append((v,k))
                        q.enqueue(path_copy)

        back_list = backtrack_rooms(graph, player)

        for emptyrooms in back_list:
            player.travel(emptyrooms)
            path.append(emptyrooms)

    
   




        
        # for k,v in graph[player.current_room.id].items():
        #     if v == '?':
        #         availdoors.append(k)
        # print(f"availdoors in room {player.current_room.id} {availdoors}")

        # #check if all doors have already been used
        # if len(availdoors) > 0:
        #     #choose a random door from the available ? doors
        #     direction = randomizer(player.current_room.id, availdoors)
        #     #log the last room and hallway you were in incase backtracking is needed.
        #     last_dir = direction
        #     prev_room = player.current_room.id
        #     print(f"prevroom: {prev_room} ")
        #     #add direction moved to path for later
        #     path.append(direction)
        #     print(f"path: {path}")

        #     #go to the next room
        #     player.travel(direction)
        #     visitcount += 1
        #     visited.add(player.current_room.id)

        #     #sanity check. where am i now?
        #     print(f"sanity check. where am i now? {player.current_room.id}")

        #     add_qs = {}
        #     if player.current_room.id not in visited:
        #     # add new room to graph with all door as ? except for the door we just came through, which is labeled for the previous room
        #         for door in player.current_room.get_exits():
        #         #backup is stored at the top
        #             if door == backup(last_dir):
        #             add_qs[door] = prev_room
        #             else:
        #                 add_qs[door] = '?'

        #         graph[player.current_room.id] = add_qs
        #         graph[prev_room][last_dir] = player.current_room.id
        #         print(f"updated graph: {graph}")


        # else:
        #     print("dead end found")
        #     return path
    # print(f"visited {visited}")
    # return path


    

    

        
    





    # Fill this out with directions to walk
    # traversal_path = ['n', 'n']

traversal_path = path
print(f"traveral_path {traversal_path}")
















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
