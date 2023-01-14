from ..objects import Rect
from .iobjects import IObject
from ..global_data import get_screen, get_id

class Scroll:
	def __init__(self, scroll_speed=10):
		self.id = get_id()
		self.screen = get_screen()
		self.objects = []
		self.scroll_speed = scroll_speed

		self.biggest_y = self.screen.size.height
		self.lowest_y = 0

		# visual objects
		self.bar = Rect(pos=[ self.screen.size.width - 15, 0  ], size=[ 15, self.screen.size.height ], color="white", stroke=2,
						border_radius=[10])
	
		self.thumb = Rect(pos=[ (self.bar.pos.x + self.bar.size.width / 4) - 2 , self.bar.pos.y], size=[ 15, self.bar.size.height ], 
                    border_radius=[10])

		self.last_y = 0

		# extends IObject to manage events over the object easily
		self.bar.extends(IObject)
		self.thumb.extends(IObject)

		self._evname_moving = f"Scroll.on.mousedown._moving.{self.id}"

		# thumb interactions
		@self.thumb.click
		def on_thumb_click():
			self.screen.time.add(30, self._move, self._evname_moving)

		@self.thumb.unclick
		def on_thumb_unclick():
			self.screen.remove_interval(self._evname_moving)
			
	def __thumb_size(self):
		# calculates thumb size
		size =  (self.biggest_y - self.lowest_y) // len(self.objects)
		if size < 30:
			size = 30
   
		elif size > self.bar.size.height:
			size = self.bar.size.height
   
		return size

	def draw(self):
		self.bar.draw()
		self.thumb.draw()
  
	def add_objects(self, *objects):
		
		for obj in objects:
			if obj.pos.y > self.biggest_y:
				self.biggest_y = obj.pos.y
    
			if obj.pos.y < self.lowest_y:
				self.lowest_y = obj.pos.y
      
			self.objects.append(obj)
   
		self.thumb.size.height = self.__thumb_size()
		
	def _move(self):
		pos = self.screen.mouse_pos()
  
		# if thumb is at top but theres still content to scroll
		if self.thumb.pos.y == self.bar.pos.y and self.thumb.pos.y > self.lowest_y:
			# scroll up

			for obj in self.objects:
				if obj.behavior["pos"] == "static":
					continue
 
				obj.pos.y += self.scroll_speed
			
		# if thumb is at bottom but theres still content to scroll
		elif self.thumb.pos.y == self.bar.pos.y and self.thumb.pos.y < self.biggest_y:
			# scroll down
   
			for obj in self.objects:
				if obj.behavior["pos"] == "static":
					continue
 
				obj.pos[1] -= self.scroll_speed

   
		self.thumb.pos[1] = pos[1] - self.thumb.size[1] // 2 

		# if overflows
		if self.thumb.pos[1] < self.bar.pos[1]:
			self.thumb.pos[1] = self.bar.pos[1]

		if self.thumb.pos[1] + self.thumb.size[1] > self.bar.pos[1] + self.bar.size[1]:
			self.thumb.pos[1] = self.bar.pos[1] + self.bar.size[1] - self.thumb.size[1]

		# update objects position
		for obj in self.objects:
			if obj.behavior["pos"] == "static":
				continue
      
			obj.pos[1] -= (self.thumb.pos[1] - self.last_y) 
   
			if obj.pos[1] > self.biggest_y:
				obj.pos[1] = self.biggest_y
			
			if obj.pos[1] < self.lowest_y:
				obj.pos[1] = self.lowest_y

		self.last_y = self.thumb.pos[1]
		self.thumb.size.height = self.__thumb_size()
		
  
				