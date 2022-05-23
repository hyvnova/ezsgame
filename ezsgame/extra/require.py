import os, sys
from pathlib import Path

def Require(*modules):
    r"""
    #### Imports modules passed as arguments.
   
    #### Parameters
    * `*modules`: list of modules to import. `args` 

    #### Example:
    - Require("all") -> imports all modules 
    - Require("base", "objects") -> imports main and objects modules
    
    #### Note: use the "module_list" function to get a list of all modules.
    """
    
    basics =  [f for f in os.listdir("ezsgame") if f.endswith(".py")]
    extras = [f for f in os.listdir("ezsgame/extra") if f.endswith(".py")]
    
    if modules[0] == "all":
        modules = basics + extras
    elif modules[0] == "basic":
        modules = basics
    elif modules[0] == "extra":
        modules = extras        

    globals_ = sys._getframe(1).f_globals
    
    for part in modules:
        part = part.replace(".py", "")    
        if part + ".py" in basics:
            mod = __import__(f"ezsgame.{part}")
        
        elif part + ".py" in extras:
            mod = __import__(f"ezsgame.extra.{part}")
            part = "extra." + part
            
        else:
            raise FileNotFoundError(f"{part} not found in {Path('ezsgame')}")
        
        
        if part.startswith("extra."):
            mod = getattr(mod, part.split(".")[0])
            mod = getattr(mod, part.split(".")[1])
        else:
            mod = getattr(mod, part)
            
        for attr in dir(mod):
            if attr not in globals_:
                globals_[attr] = getattr(mod, attr)
     
def module_list(_print=True) -> tuple:
    """
    #### Returns a tuple with basic and extra modules.  
    
    #### Parameters
    * `_print`: if True, prints the modules.
    
    """
    basics =  [f for f in os.listdir("ezsgame") if f.endswith(".py")]
    extras = [f for f in os.listdir("ezsgame/extra") if f.endswith(".py")]
    
    if _print:
        print(f"\nBasic modules: ")
        [print(f"\t{f[:-3]} ") for f in basics]
        print()
        
        print(f"\nExtra modules: ")
        [print(f"\t{f[:-3]} ") for f in extras]
        
    return basics, extras



    

