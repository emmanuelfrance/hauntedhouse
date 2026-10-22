"""A tiny haunted-house text adventure."""


ROOMS = {
    "foyer": {
        "description": "You are in the dusty foyer. The front door is locked.",
        "exits": {"hallway"},
        "objects": {
            "mirror": "a Mirror Wraith",
            "umbrella": "a Grinny Goblin",
        },
    },
    "hallway": {
        "description": "A long hallway stretches between the foyer and kitchen.",
        "exits": {"foyer", "kitchen", "attic"},
        "objects": {
            "painting": "a Portrait Phantom",
            "vase": "a Vexing Viper",
        },
    },
    "kitchen": {
        "description": "The kitchen smells like old cheese. A drawer rattles by itself.",
        "exits": {"hallway"},
        "objects": {
            "fridge": "a Frostbite Beast",
            "drawer": "a Drawer Dragon",
        },
    },
    "attic": {
        "description": "The attic is full of dusty boxes and creaky floorboards.",
        "exits": {"hallway"},
        "objects": {
            "toy": "a Toybox Troll",
            "trunk": "a Trunk Creature",
        },
    },
}


def show_help():
    print(
        "\nCommands:\n"
        "  look                 Look around the room\n"
        "  go <room>            Move to a connected room\n"
        "  touch <thing>        Touch something and meet its monster\n"
        "  inventory            Check your key and hearts\n"
        "  escape               Try to unlock the front door from the foyer\n"
        "  help                 Show these commands\n"
        "  quit                 Leave the haunted house (and the game) behind"
    )


def show_room(room_name, touched):
    room = ROOMS[room_name]
    print(f"\n{room['description']}")
    untouched = [
        name for name in room["objects"] if (room_name, name) not in touched
    ]
    if untouched:
        print("Nearby: " + ", ".join(untouched))
    else:
        print("There is nothing left to touch in here.")
    print("Exits: " + ", ".join(sorted(room["exits"])))


def play():
    room_name = "foyer"
    touched = set()
    hearts = 5
    has_key = False

    print("THE TOUCHY HAUNTED HOUSE")
    print("Every new thing you touch unleashes a monster!")
    print("Find the key and escape before you run out of hearts.")
    show_help()
    show_room(room_name, touched)

    while True:
        command = input("\nWhat do you do? ").strip().lower()
        if not command:
            continue

        if command == "help":
            show_help()
        elif command == "look":
            show_room(room_name, touched)
        elif command == "inventory":
            key_status = "yes" if has_key else "no"
            print(f"You have {hearts} heart(s). Front-door key: {key_status}.")
        elif command == "quit":
            print("Thanks for playing. Watch what you touch!")
            return
        elif command == "escape":
            if room_name != "foyer":
                print("The front door is in the foyer.")
            elif has_key:
                print("You unlock the front door and escape! You win!")
                return
            else:
                print("The front door is locked. Find its key in the kitchen.")
        elif command.startswith("go "):
            destination = command[3:].strip()
            if destination in ROOMS[room_name]["exits"]:
                room_name = destination
                show_room(room_name, touched)
            else:
                print("You can't go there. Exits: " + ", ".join(
                    sorted(ROOMS[room_name]["exits"])
                ))
        elif command.startswith("touch "):
            object_name = command[6:].strip()
            if object_name.startswith("the "):
                object_name = object_name[4:]
            objects = ROOMS[room_name]["objects"]
            if object_name not in objects:
                print("That isn't something you can touch here.")
            elif (room_name, object_name) in touched:
                print("You already touched that. Its monster is gone.")
            else:
                touched.add((room_name, object_name))
                monster = objects[object_name]
                hearts -= 1
                print(f"You touch the {object_name}... {monster} pops out!")
                print(f"You escape, but lose a heart. Hearts left: {hearts}.")
                if room_name == "kitchen" and object_name == "drawer":
                    has_key = True
                    print("Inside the drawer, you find the front-door key!")
                if hearts <= 0:
                    print("You ran out of hearts. The house wins this time!")
                    return
        else:
            print("I don't know that command. Type 'help' to see what you can do.")


if __name__ == "__main__":
    play()