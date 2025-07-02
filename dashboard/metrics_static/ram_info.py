from psutil import virtual_memory

class RamInfo:
    def __init__(self):
        self.mem = virtual_memory()

    def get_total_memory(self):
        return self.mem.total

    def get_used_memory(self):
        return self.mem.used

    def get_free_memory(self):
        return self.mem.free

    def get_percent_memory(self):
        return self.mem.percent

    def get_available_memory(self):
        return self.mem.available    