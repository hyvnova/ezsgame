class Scene:
    def __init__(self, file):
        self.file = file
        self._globals = {**globals()}
        self._locals = {**locals()}
        
        with open (file, "r") as f:
            try:
                declarations, self.code = f.read().split("::main")            
            except:
                raise SyntaxError(f"No code division found at: {file}")
            
            # get func names declared in the file
            func_names = [line.split(" ")[1] for line in declarations.split("\n") if line.startswith("def")]
            func_names = list(map(lambda x: x.split("(")[0], func_names))
            
            self._globals.update(self._locals)
            self._locals.update(self._globals)
            
            exec (declarations, self._globals, self._locals)
        
            # assing functions to the scene
            for key, value in self._locals.items():
                if key in func_names:
                    setattr(self, key, value)
                
    def play(self):
        self._globals.update(self._locals)
        self._locals.update(self._globals)
        exec(self.code, self._globals, self._locals)

