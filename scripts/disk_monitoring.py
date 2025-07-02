from time import sleep

from psutil import disk_usage, disk_io_counters

from scripts.utils.logger import setup_logger
from scripts.utils.format_out import format_bytes
from database.logs_repository import save_log_disk


logger = setup_logger()


class DiskStats:
    def __init__(self):
        pass

    def get_total_disk(self):
        return disk_usage('/').total

    def get_free_disk(self):
        return disk_usage('/').free
    
    def get_used_disk(self):
        return disk_usage('/').used
    
    def get_percent_disk(self):
        return disk_usage('/').percent
    
    def get_read_bytes(self):
        return disk_io_counters().read_bytes

    def get_write_bytes(self):
        return disk_io_counters().write_bytes

    def get_read_time(self):
        return disk_io_counters().read_time

    def get_write_time(self):
        return disk_io_counters().write_time    


class CriticalDiskDetector:
    def __init__(self, threshold=80):
        self.threshold = threshold

    def detect_critical_total(self, percent):
        return percent > self.threshold
    
    def detect_critical_io(self, read_time, write_time):
        return read_time > write_time

    def detect_critical_io_bytes(self, read_bytes, write_bytes):
        return read_bytes > write_bytes

class DiskMonitorController:
    def __init__(self, interval=2):
        self.stats = DiskStats()
        self.interval = interval

    def run(self):
        try:
            while True:
                total = self.stats.get_total_disk()
                free = self.stats.get_free_disk()
                used = self.stats.get_used_disk()
                percent = self.stats.get_percent_disk() 
                read_time = self.stats.get_read_time()
                write_time = self.stats.get_write_time()
                write_bytes = self.stats.get_write_bytes()
                read_bytes = self.stats.get_read_bytes()

                logger.info(f"Total Disk: {format_bytes(total)}")
                logger.info(f"Free Disk: {format_bytes(free)}")
                logger.info(f"Used Disk: {format_bytes(used)}") 
                logger.info(f"Percent Disk usage: {percent}%")
                logger.info("--" * 20)
                logger.info(f"Read time: {read_time}")  
                logger.info(f"Write time: {write_time}")
                logger.info(f"Read bytes: {format_bytes(read_bytes)}")
                logger.info(f"Write bytes: {format_bytes(write_bytes)}")
                logger.info("--" * 20)
                

                if self.stats.get_percent_disk() > 80:
                    logger.warning(f" Total Disk usage is high: {self.stats.get_percent_disk()}%")
                    save_log_disk(total, used, percent)

                sleep(self.interval)
        except KeyboardInterrupt:
            logger.warning("Monitoramento interrompido pelo usuário.")
        except Exception as e:
            logger.exception(f"Erro inesperado: {e}")    

