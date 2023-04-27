from ezsgame import *
from ezsgame.scenes import SceneManager, Scene

class main_scene(Scene):
    def init(self):
        self.sprite = AnimatedSprite("./sprites/tex.gif", Pos(0), Size(500))

    def update(self):
        pass

    def draw(self):
        self.sprite.draw()

    def exit(self):
        pass

    def switch_to(self):
        pass

Window(Size(500), show_fps=True ).run_scenes(
    SceneManager(
        main_scene("main")
    )
)