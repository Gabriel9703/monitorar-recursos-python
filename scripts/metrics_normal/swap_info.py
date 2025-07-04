from psutil import swap_memory


class SwapInfo:
    def __init__(self):
        self.mem = swap_memory()

    def get_total_swap(self):
        return self.mem.total

    def get_used_swap(self):
        return self.mem.used

    def get_free_swap(self):
        return self.mem.free

    def get_percent_swap(self):
        return self.mem.percent

    def get_available_swap(self):
        return self.mem.available
    