import time

class Timer:
    def __init__(self):
        self.start_time = None
        self.elapsed_time = 0
        self.is_running = False

    def start(self):
        if not self.is_running:
            self.start_time = time.time()
            self.is_running = True

    def stop(self):
        if self.is_running:
            self.elapsed_time += time.time() - self.start_time
            self.is_running = False

    def reset(self):
        self.elapsed_time = 0
        if self.is_running:
            self.start_time = time.time()

    def get_elapsed_time(self):
        if self.is_running:
            return self.elapsed_time + (time.time() - self.start_time)
        else:
            return self.elapsed_time

    def is_timer_running(self):
        return self.is_running
