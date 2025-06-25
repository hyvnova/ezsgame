from client import LADY_AI, Client, get_character_prompt
from components import DetectNear, DialogueBox
from ezsgame import *
import map

# Initialize the game window
window = Window(title="Toss The Crown", size=Size(1280, 720), show_fps=True, fps=60)
map.load()
# map.edit()


def on_near(obj):
    # Interaction with the lady
    if obj.tags.get("name", "") == "lady":

        @Input().get_text()
        def on_input(text):
            text = text.strip()
            if not text:
                return

            print("User: ", text)
            # dialogue, thought = LADY_AI.send_message("user", text)
            # print("Lady: ", dialogue)
            # print("Thought: ", thought)

            World.search_single(tags={"name": "lady"}).components[DialogueBox].push(["Line 1", "Line 2", "Line 3"])

player = Rect(
    Pos("center", "center"),
    Size(50, 50),
    color="white",

    components=[
        Controller(),
        DetectNear(on_near)
    ],

    tags={"name": "player"},
    z_index=1.1
)

lady = Rect(
    player.pos + Pos(100, 100),
    Size(50, 50),
    color="red",
    components=[
        DialogueBox(
            text="Hello, traveler! What brings you to this land?",
            font_size=20,
            color="white",
            pace=3
        )
    ],
    tags={"name": "lady"}
)


while True:
    window.check_events()
    window.fill("black")


    for obj in World.objects:
        obj.draw()

    window.update()
