from ezsgame.all import *

screen = Screen(show_fps=True)


class MyComponent:
    activation_method = ComponentTemplate.activation_methods.on_click
    
    def init(self, **kwargs):
        pass
    
    def activate(self):
        self.object.color = "red"
        
    def desactivate(self):
        self.object.color = "white"

my_component = ComponentTemplate.create(MyComponent, True)

rect = Rect(["center", "center"], [100, 100], components=[my_component])

while True:
    screen.check_events()
    screen.fill()

    rect.draw()

    screen.update()