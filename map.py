from ezsgame import *
import json

DEFAULT_MAP_FILE = "./map.json"

MAP_OBJECTS = []

# SIMUALTION OF A POINTER HEHE
CURRENT_RECT = [
    None
]

def edit(
    map_file: str = DEFAULT_MAP_FILE # path to json file
):
    """
    Allow real-time editing of the map
    """

    """
    A rectangle will be on the mouse,
    With Arrow left and right, you can adjust the width
    With Arrow up and down, you can adjust the height
    With "<" and ">" you can adjust color from a predifined list
    With "s" you can save the map
    With "l" you can load the map

    On click the rectangle will be added to the world
    With AWSD you can move the "camera"
    """

    colors = [
        "red",
        "green",
        "blue",
        "yellow",
        "purple",
        "orange",
        "pink",
        "black",
        "white",
    ]

    color = colors[0]

    default_rect = lambda: Rect(
        get_mouse_pos(),
        Size(50, 50),
        color=color,
    )

    rect = default_rect()

    CURRENT_RECT[0] = rect

    add_to_size = [
        0, 0, # width, height
    ]

    @on_event("mousemotion")
    def on_mouse_move():
        CURRENT_RECT[0].pos = get_mouse_pos()

    @on_event("mousedown")
    def on_mouse_down():
        World.objects_to_add.add(CURRENT_RECT[0])
        MAP_OBJECTS.append(CURRENT_RECT[0])
        CURRENT_RECT[0] = default_rect()

    on_key("down", "q")(save)
    on_key("down", "l")(load)

    def mod_val(source, index, value):
        source[index] = value

    # LEFT
    on_key_updown("left", lambda: mod_val(add_to_size, 0, -5), lambda: mod_val(add_to_size, 0, 0))

    # RIGHT
    on_key_updown("right", lambda: mod_val(add_to_size, 0, 5), lambda: mod_val(add_to_size, 0, 0))

    # UP
    on_key_updown("up", lambda: mod_val(add_to_size, 1, -5), lambda: mod_val(add_to_size, 1, 0))

    # DOWN
    on_key_updown("down", lambda: mod_val(add_to_size, 1, 5), lambda: mod_val(add_to_size, 1, 0))

    @on_key("down", "c")
    def on_key_down():
        CURRENT_RECT[0].styles.color = random.choice(colors)
        CURRENT_RECT[0].styles.resolve(CURRENT_RECT[0].parent.size)

    @on_key("down", "esc")
    def on_key_down():
        save()
        World.window.quit()


    @on_event("update")
    def reflect_preview_changes():
        CURRENT_RECT[0].size.width += add_to_size[0]
        CURRENT_RECT[0].size.height += add_to_size[1]


def save(
    map_file: str = DEFAULT_MAP_FILE # path to json file
):
    """
    Saves all objects in the world to a json file
    """
    print("Saving map...")

    # create file as an empty file
    with open(map_file, "w") as f:
        f.write("")
    
    json_data = list(map(lambda obj: str(repr(obj)), MAP_OBJECTS))

    json.dump(json_data, open(map_file, "w"), indent=4)


def load(
    map_file: str = DEFAULT_MAP_FILE # path to json file
):
    """
    Loads all objects from a json file to the world
    """
    print("Loading map...")
    
    # if file does not exist, create it
    if not os.path.exists(map_file):
        with open(map_file, "w") as f:
            f.write("[]")
        
        return

    try:
        json_data = json.load(open(map_file, "r"))
    except:
        # write empty list to file
        with open(map_file, "w") as f:
            f.write("[]")

        # default to empty list
        json_data = []
    
    for obj_repr in json_data:
 
        obj = eval(obj_repr) # creating object automacally adds it to the world
        MAP_OBJECTS.append(obj)

        # Add delete handler to object
        @add_event("click", obj, "delete on click")
        def delete_obj():
            World.objects_to_remove.add(obj)
            MAP_OBJECTS.remove(obj)
