from functools import wraps
import time

def every_seconds(seconds: float):
    """
    Decorator to run a function every x seconds
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            time.sleep(seconds)
            
        return wrapper
    
    return decorator
    