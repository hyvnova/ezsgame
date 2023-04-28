"""
This module is used to provide an easy way to create threads and processes to improve performance.
"""

import threading
import multiprocessing

def add_thread(target, args=()):
    """
    Add a function to be executed in a new thread.

    Args:
        target: a function to be executed in a new thread
        args: a tuple of arguments to pass to the function (default: ())

    Returns:
        A Thread object representing the new thread.
    """
    thread = threading.Thread(target=target, args=args)
    thread.start()
    return thread


def add_process(target, args=()):
    """
    Add a function to be executed in a new process.

    Args:
        target: a function to be executed in a new process
        args: a tuple of arguments to pass to the function (default: ())

    Returns:
        A Process object representing the new process.
    """
    process = multiprocessing.Process(target=target, args=args)
    process.start()
    return process
