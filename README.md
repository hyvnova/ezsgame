# EZSGAME
ezsgame is a library that aims to make the process of creating and manipulating 2D graphics or game development simple, easy, fun, and comfortable as possible for the user.

## Instalation 
```bash
pip install ezsgame
```
### Manual install
- Download ezsgame.zip [here](https://github.com/NoxxDev/ezsgame)

- Clone the repository [here](https://github.com/NoxxDev/ezsgame.git)

# Sample 
```python
window = Window()

# current count value
current_value = [0]  # We use a list so the value can be modified from other scopes

container = Rect(
    Pos("center", "center"), Size("30%", "2/4"), styles=Styles(color="white", stroke=1)
)

counter_text = Text(
    f"Count is {current_value[0]}", 23, Pos(0, 0), parent=container
).center_at()  # This method centers the objects inside it's parent

# Let's make buttons to modify the count
increase_button = Rect(
    pos=Pos("right-center", "center"),
    size=Size(50, 50),
    styles=Styles(border_radius=[5], color="green"),
)


# Lets add an event listerner to the button
@add_event(event="click", object=increase_button)
def increase_count():
    # This method will only be called when `increase_button` is clicked
    current_value[0] += 1

    # We also need to update the text in the counter
    counter_text.update(text=f"Count is {current_value[0]}")


decrease_button = Rect(
    pos=Pos("left-center", "center"),
    size=Size(50, 50),
    styles=Styles(border_radius=[5], color="red"),
)


@add_event(event="click", object=decrease_button)
def decrease_count():
    # This method will only be called when `decrease_button` is clicked
    current_value[0] -= 1

    # We also need to update the text in the counter
    counter_text.update(text=f"Count is {current_value[0]}")


# Group everthing so you don't have to call draw method one-by-one
counter = Group(container, counter_text, decrease_button, increase_button)


while True:
    window.check_events()
    window.fill("black")

    # Draw the counter
    counter.draw()

    window.update()
```