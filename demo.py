from ezsgame import *

class pg_scene(Scene):
    def init(self):
        # define tile size
        self.tile_size = 32

        # Create a tile map (8, 8)
        self.tile_map = Group()
        for y in range(8):
            for x in range(8):
                self.tile_map.add(Sprite("./sprites/sample_tile.png", Pos(x, y) * self.tile_size, Size(self.tile_size)))

    def update(self):
        # if w is pressed, switch to main scene
        if went_down("w"):
            self.switch_to("main")

    def draw(self):
        # draw tile map onto screen
        self.tile_map.draw()



class main_scene(Scene):
    def init(self):
        self.sprite = AnimatedSprite("./sprites/tex.gif", Pos(0), Size(500))

    def update(self):
        # if w is pressed, switch to pg scene
        if went_down("e"):
            self.switch_to("pg")

    def draw(self):
        self.sprite.draw()

    def exit(self):
        pass


Window(Size(500), show_fps=True ).run_scenes(
    SceneManager(
        main_scene(),
        pg_scene(),
    )
)