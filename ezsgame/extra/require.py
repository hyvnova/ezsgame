import os, sys
from pathlib import Path

def Require(*parts):
    """
    Imports modules passed as arguments.
    @param parts: list of strings

    Example:
    Require("all") -> imports all modules
    Require("main", "objects") -> imports main and objects modules
    
    Note: use the "module_list" function to get a list of all modules.
    """
    
    parts_in_dir = [f for f in os.listdir("ezsgame") if f.endswith(".py")]

    if parts[0] == "all":
        parts = parts_in_dir

    globals_ = sys._getframe(1).f_globals
    
    for part in parts:
        part = part.replace(".py", "")    
        if part + ".py" in parts_in_dir:
            mod = __import__(f"ezsgame.{part}")
            mod = getattr(mod, part)
            
            for attr in dir(mod):
                if attr not in globals_:
                    globals_[attr] = getattr(mod, attr)
        else:
            raise FileNotFoundError(f"{part} not found in {Path('ezsgame')}")
     
def module_list():
    """
    Returns a list of all modules in ezsgame directory.
    """
    return [f for f in os.listdir("ezsgame") if f.endswith(".py")]       

