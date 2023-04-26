from ezsgame import *

window: Window = Window(show_fps=True, color="black")

# -------- Coding a counter!! --------

# current count value
current_value = [0] # We use a list so the value can be modified from other scopes 

container = Rect(
    pos=Pos("center", "center"),
    size=Size("30%", "2/4"),
    styles=Styles(
        color="white",
        stroke=1
    )
)

counter_text = Text(
    text=f"Count is {current_value[0]}",
    font_size=23,
    pos=("center", "center"), 
    parent=container
)

# Let's make buttons to modify the count
increase_button = Rect(
    pos=Pos("right-center", "center"),
    size= Size(50,50),
    styles=Styles(
        border_radius=[ 5 ],
        color="green"
    )
)

# Lets add an event listerner to the button
@add_event(event="click", object=increase_button)
def increase_count():
    # This method will only be called when `increase_button` is clicked
    current_value[0] += 1
    
    # We also need to update the text in the counter
    counter_text.text.set(f"Count is {current_value[0]}")
    

decrease_button = Rect(
    pos=Pos("left-center", "center"),
    size=Size(50,50),
    styles=Styles(
        border_radius=[ 5 ],
        color="red"
    )
)

@add_event(event="click", object=decrease_button)
def decrease_count():
    # This method will only be called when `decrease_button` is clicked
    current_value[0] -= 1
    counter_text.text.set(f"Count is {current_value[0]}")
    

# Group everthing so you don't have to call draw method one-by-one
counter = Group(container, counter_text, decrease_button, increase_button)


while True:
    window.check_events()
    window.fill()
    
    # Draw the counter
    counter.draw()
    
    window.update()