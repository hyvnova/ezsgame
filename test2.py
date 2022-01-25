from ezsgame.main import *

s = IScreen(size=[480, 400], title="Test", fps=120, show_fps=True,
    objects=[Rect(size=[100,100], pos=[1,1], color=Color.white())]
).run(fill_color=Color.black())