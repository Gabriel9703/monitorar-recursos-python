from psutil import  virtual_memory
from time import sleep
from scripts.utils.logger import setup_logger
from scripts.utils.format_out import format_bytes
from database.logs_repository import save_log_ram

logger = setup_logger()



class RamStats:
    def __init__(self):
        pass

    def get_available_memory(self):
        return virtual_memory().available
    
    def get_total_memory(self):
        return virtual_memory().total
    
    def get_free_memory(self):
        return virtual_memory().free
    
    def get_used_memory(self):
        return virtual_memory().used
    
    def get_percent_memory(self):
        return virtual_memory().percent
    

class CriticalRamDetector:
    def __init__(self, threshold=80):
        self.threshold = threshold

    def detect_critical_total(self, usage):
        return usage > self.threshold
    
class RamMonitorController:
    def __init__(self, interval=1.5):
        self.stats = RamStats()
        self.detector = CriticalRamDetector()
        self.interval = interval

    def run(self):
        try:
            while True:
                total = self.stats.get_total_memory()
                available = self.stats.get_available_memory()
                used = self.stats.get_used_memory()
                percent = self.stats.get_percent_memory()

                logger.info(f"Total RAM: {format_bytes(total)}")
                logger.info(f"Available RAM: {format_bytes(available)}")
                logger.info(f"Used RAM: {format_bytes(used)}")
                logger.info(f"Percent RAM usage: {percent}%")

                if self.detector.detect_critical_total(self.stats.get_percent_memory()):
                    logger.warning(f" Total RAM usage is high: {self.stats.get_percent_memory()}%")
                    save_log_ram(total, used, percent)
                sleep(self.interval)
        except KeyboardInterrupt:
            logger.warning("Monitoramento interrompido pelo usuário.")
        except Exception as e:
            logger.exception(f"Erro inesperado: {e}")        

