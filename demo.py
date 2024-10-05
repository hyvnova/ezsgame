from agent import Agent
from ezsgame import *
from components import *


window = Window(title="AI Agent pathfinding")

"""
UI
0 -> Select Agent
1 -> Select Goal
2 -> Select Obstacle
"""
SELECTED: int | None = None
Agents = Group()
Obstacles = Group()
Goals = Group()

def select(index: int):
    global SELECTED

    if index == SELECTED:
        SELECTED = None
        return

    SELECTED = index

def create_callback(index: int):
    return lambda: select(index)


UI = Group(
    (Rect(
        Pos(x_position, "bottom"),
        Size(90, 30),
        color="white",
        stroke=2,
        border_radius=[5],
        margins=[5],
        components=[
            Label(
                text=label,
                color="white",
                font_size=20,
            ),
            Selectable(
                on_select=create_callback(i),
            ),
        ],
    )
    for i, x_position, label in zip(
        range(3),  # Select options  0, 1, 2
        ("left-center", "center", "right-center"),  # x position
        ("Agent", "Goal", "Obstacle"),  # Labels
    )),

    playground=Rect(
        Pos("center", "5%"),
        Size("90%", "70%"),
        color="white",
        stroke=1,
        border_radius=[5],
        margins=[10, 0],
    ),
)


@add_event("click", UI.playground)
def on_click():
    global SELECTED

    if SELECTED is None:
        return

    pos = get_mouse_pos()
    print(f"Clicked at {pos} with SELECTED {SELECTED}")

    # Spawn Agent
    if SELECTED == 0:
        Agents.add(
            Agent(
                pos,
                Goals,
                Obstacles,
                Agents
            )
        )

    # Spawn Goal
    if SELECTED == 1:
        Goals.add(
            Rect( 
                pos,
                Size(20),
                color="green",
                stroke=4,
                border_radius=[0],
            )
        )

    # Spawn Obstacle
    if SELECTED == 2:
        Obstacles.add(
            Rect(
                pos,
                Size(20),
                color="red",
                stroke=4,
                border_radius=[5],
            )
        )

@add_event("rightclick", UI.playground)
def on_right_click():
    global SELECTED

    if SELECTED is None:
        return

    pos = get_mouse_pos()
    print(f"Right Clicked at {pos} with SELECTED {SELECTED}")

    # Remove last agent
    if SELECTED == 0:
        if Agents:
            Agents.pop()    

    # Remove last goal
    if SELECTED == 1:
        if Goals:
            Goals.pop()

    # Remove last obstacle
    if SELECTED == 2:
        if Obstacles:
            Obstacles.pop()


def remove_goals():
    """
    Remove goals being visited by the agent
    """

while True:
    window.check_events()
    window.fill("black")

    # Updates
    remove_goals()

    UI.draw()
    Agents.draw()
    Goals.draw()
    Obstacles.draw()

    window.update()
