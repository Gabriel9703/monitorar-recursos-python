from psutil import disk_usage, disk_io_counters


class DiskInfo:
    def __init__(self):
        self.disk = disk_usage("/")
        self.disk_io = disk_io_counters()

    def get_total_disk(self):
        return self.disk.total

    def get_used_disk(self):
        return self.disk.used

    def get_free_disk(self):    
        return self.disk.free

    def get_percent_disk(self):
        return self.disk.percent

    def get_read_bytes(self):
        return self.disk_io.read_bytes

    def get_write_bytes(self):
        return self.disk_io.write_bytes

    def get_read_time(self):
        return self.disk_io.read_time

    def get_write_time(self):
        return self.disk_io.write_time    