from time import monotonic_ns
from threading import Thread

class Multilock:
    def __init__(self, size):
        self.last_to_enter = [-1] * size
        self.level = [-1] * size
        self.num_locks = size
        
  
    def acquire(self, process_id):    
        for i in range(0, self.num_locks):
            self.level[process_id] = i
            self.last_to_enter[i] = process_id
            while self.last_to_enter[i] == process_id \
                and max(self.level[:process_id] + self.level[process_id+1:]) >= i:
                continue
    
    def release(self, process_id):
        self.level[process_id] = -1 
    
    def get_queue(self):
        return self.level


class MultilockWithTimeout:
    def __init__(self, size):
        self._last_to_enter = [-1] * size
        self._level = [-1] * size
        self._num_locks = size
        self.timeout_threads = [None] * size
        self.stop_threads = [False] * size
        self.timeout_grant_in_nsecs = 8000000000 
  
    def acquire(self, process_id):   
        for i in range(0, self._num_locks):
            self._level[process_id] = i
            self._last_to_enter[i] = process_id
            while self._last_to_enter[i] == process_id and max(self._level[:process_id] + self._level[process_id+1:]) >= i:
                continue

        self.stop_threads[process_id] = False
        self.timeout_threads[process_id] = Thread(target=self._verify_timeout, args=(process_id, lambda: self.stop_threads[process_id]))
        self.timeout_threads[process_id].start()

    def _verify_timeout(self, process_id, stop):
        start_time = monotonic_ns()
        while (monotonic_ns() - start_time) <  self.timeout_grant_in_nsecs and not stop():
            continue

        if not stop():
            self.release(process_id)
    
    def release(self, process_id):        
        self.stop_threads[process_id] = True
        self._level[process_id] = -1
