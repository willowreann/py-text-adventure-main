import json
from time import perf_counter
import random

 
def main():
    # TODO: allow them to choose from multiple JSON files?
    with open('spooky_mansion.json') as fp:
        game = json.load(fp)
    print_instructions()
    print("You are about to play '{}'! Good luck!".format(game['__metadata__']['title']))
    print("")
    play(game)


def play(rooms):
    
    rooms_ = ['entranceHall', 'basement', 'attic', 'attic2', 'balcony', 'kitchen', 'dumbwaiter',
         'secretroom', 'crypt']
    
    t1_start = perf_counter()  

    # Where are we? Look in __metadata__ for the room we should start in first.
    current_place = rooms['__metadata__']['start']
    # The things the player has collected.
    stuff = ['Cell Phone; no signal or battery...']
    #creating a cat
    cat_place = random.choice(rooms_)


    while True:
        # Figure out what room we're in -- current_place is a name.
        here = rooms[current_place]
        # Print the description.
        print(here["description"])
        print("Items in this room :", here['items'])
        
        if current_place == cat_place:
            print("\n...You found the cat!\n")
            if 'raw fish' in stuff:
                print("Purrrrrrr..\n\n...You have the cat's favorite treat. He's going to wait here and hope that you return.\n")
                #make cat stay in this room, stop random spawning
                cat_place = current_place


        # TODO: print any available items in the room...
        # e.g., There is a Mansion Key.

        # Is this a game-over?
        if here.get("ends_game", False):
            break

        # Allow the user to choose an exit:
        usable_exits = find_visible_exits(here)
        # Print out numbers for them to choose:
        for i, exit in enumerate(usable_exits):
            print("  {}. {}".format(i+1, exit['description']))

        # See what they typed:
        action = input("> ").lower().strip()

        # If they type any variant of quit; exit the game.
        if action in ["quit", "escape", "exit", "q"]:
            print("You quit.")
            break
        if action == "help":
            print_instructions()
            continue
        if action == "stuff":  
            if len(stuff) > 0:
                print("Your stuff:", stuff)
            else:
                print("You have nothing")
            continue
        if action == "take":
            print(here['items'])
            for x in here['items']:
                stuff.append(x)
            continue
        if action == "drop":
            delete = input("Which item would you like to drop?")
            if delete in stuff:
                stuff.remove(delete)
                new_list = here['items']
                new_list.append(delete)
                print("\n...You dropped", delete, "...\n")
                    
            else:
                print("\n...I don't understand", delete, "...\n")
            continue
                
        if action == "search":
            for exit in here["exits"]:
                if exit.get("hidden", False):
                    exit["hidden"] = False
                    print("\n..You found hidden exits!...\n")
                    print(exit)              
            continue

            
        # TODO: if they type "stuff", print any items they have (check the stuff list!)
        # TODO: if they type "take", grab any items in the room.
        # TODO: if they type "search", or "find", look through any exits in the room that might be hidden, and make them not hidden anymore!
        

        
        # Try to turn their action into an exit, by number.
        
        try:
                 
            num = int(action) - 1
            selected = usable_exits[num]
            print(selected)
            if 'required_key' in selected:
                key_needed = selected['required_key']
                
                if key_needed in stuff:
        
                    print("\n...You may pass...\n")
                    current_place = selected['destination']
                    print('...')
                    continue
           
                else:
                    print("\n...Come back with the key!...\n")
                    continue
            print("...")
            current_place = selected['destination']

        
        except:
            print("I don't understand '{}'...".format(action))
  
        
    print("")
    print("")
    print("=== GAME OVER ===")
    t1_stop = perf_counter() 
    

    time_play = t1_stop-t1_start 
    if time_play > 60:
        time_min = time_play // 60
        time_sec = time_play % 60
        print("Time Elapsed:", time_min, "minutes and ", time_sec, "seconds")
    else:
        print("Time Elapsed:", t1_stop-t1_start, "seconds")

        
    
  
    

def find_visible_exits(room):
    """
    Given a room, and the player's stuff, find a list of exits that they can use right now.
    That means the exits must not be hidden, and if they require a key, the player has it.
    RETURNS
     - a list of exits that are visible (not hidden) and don't require a key!
    """
    usable = []
    for exit in room['exits']:
        if exit.get("hidden", False):
            continue            
        usable.append(exit)
    return usable



def print_instructions():
    print("=== Instructions ===")
    print(" - Type a number to select an exit.")
    print(" - Type 'stuff' to see what you're carrying.")
    print(" - Type 'take' to pick up an item.")
    print(" - Type 'drop' to leave an item in current room.")
    print(" - Type 'quit' to exit the game.")
    print(" - Type 'search' to take a deeper look at a room.")
    print(" - Type 'help' to view instructions again.")
    print("=== Instructions ===")
    print("")


if __name__ == '__main__':
    main()