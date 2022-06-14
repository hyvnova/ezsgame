import json

class Styles:
    r"""
    ####  Manages styles in a JSON file.
    #### Parameters:
    - **file**: The path to the JSON file.
    
    
    #### Note: adds a property for each style in the JSON file.
    #### Example:
    ```python
    styles = Styles("styles.json")
    Rect(pos=[0,0], size=[50,50], styles=styles.rect)    
    ```
    """

    def __init__(self, file:str):
        self.file = file
        self.styles = {}
        
        with open(self.file, 'r') as f:
            data = json.load(f)

        for name, styles_set in data.items():
            self.styles[name] = styles_set
            setattr(self, name, styles_set)
            
    def __getitem__(self, key):
        return self.styles[key]
    
    def __setitem__(self, key, value):
        self.styles[key] = value
        
    def __delitem__(self, key):
        del self.styles[key]
        
    def __iter__(self):
        return iter(self.styles)
    
    def __len__(self):
        return len(self.styles)
    
    def __next__(self):
        return next(self.styles)

    def __str__(self):
        return "<Styles>"

            
