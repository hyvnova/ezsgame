from ..objects import *
from .iobjects import IObject
from .components import Draggable
from ..global_data import get_screen, get_id

class Scroll:
	def __init__(self):
		self.id = get_id()
		self.screen = get_screen()
		self.objects = []

		# visual objects
		self.bar = Rect(pos=[ self.screen.size.width - 15, 0  ], size=[ 15, self.screen.size.height ], color="white", stroke=2,
						border_radius=[10])
	
		self.thumb = Rect(pos=[ self.bar.pos.x + self.bar.size.width / 4 , self.bar.pos.y], size=[ 15, self.screen.size.height//4 ], 
						  border_radius=[10],
                          
						  components=[
                              Draggable(freeze_x=True, freeze_y=True, outline=False)
						  ])

		# extends IObject to manage events over the object easily
		self.bar.extends(IObject)
		self.thumb.extends(IObject)

		# thumb interactions
		@self.thumb.click
		def on_thumb_click():
			print("Clicked")
			self.thumb.components[Draggable].freeze_y = False

		@self.thumb.unclick
		def on_thumb_unclick():
			print("Unclicked")
			self.thumb.components[Draggable].freeze_y = True
			
	def draw(self):
		self.bar.draw()
		self.thumb.draw()


		