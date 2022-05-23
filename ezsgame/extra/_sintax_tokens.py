

# ----------------------------------------------------------------------------

# TOKENS FOR STRUCTURED OBJECTS MODULE

# ----------------------------------------------------------------------------

# ALL TOKENS MUST BE UNIQUE OR IT CAN CAUSE ERRORS, RUN THIS FILE TO SEE IF ANY TOKEN IS DUPLICATE
# DO NOT REMOVE ANY TOKEN


STYLES_CLASS_TOKEN = "::" # used to denife a set of styles that will be applied to the object with same class 
# Example:   ::items : {...}

FUNCTION_TOKEN = "on:" # used to define a function
# Example:   on:click : {...}


# check if any duplicate token
if __name__ == "__main__":
    tokens = {}
    _globals = {**globals()}
    
    for k,v in _globals.items():
        
        if k.startswith("__"):continue
        if not k or not v:continue
        
        if v in tokens.values():
            key = [k for k,v in tokens.items() if v == v][0]
            raise SyntaxError(f"Duplicate token: {k} == {key},  Token : {v}")
        else:
            tokens[k] = v
            