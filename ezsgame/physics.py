class Gravity:
    def __init__(self, objects, screen, gravity=[0,-2]):
        if isinstance(objects, list):
            self.objects = objects
        else:
            self.objects = [objects]
        
        self.screen = screen
        self.gravity = gravity

        @self.screen.add_interval(self.screen.fps * screen.delta_time() * 60)
        def gravity_update():
            self.update()
    
    def update(self):
        for obj in self.objects:
            if obj.is_out(self.screen)[0]:
                continue
            
            obj.move(*self.gravity)
            
                    


        
        

    
            
