from psutil import swap_memory
from scripts.utils.logger import setup_logger
from scripts.utils.format_out import format_bytes
from database.logs_repository import save_log_swap
from time import sleep

logger = setup_logger()


class SwapStats:
    def __init__(self):
        pass

    def get_total_swap(self):
        return swap_memory().total
    
    def get_free_swap(self):
        return swap_memory().free
    
    def get_used_swap(self):
        return swap_memory().used
    
    def get_percent_swap(self):
        return swap_memory().percent


class CriticalSwapDetector:
    def __init__(self, threshold=80):
        self.threshold = threshold

    def detect_critical_total(self, usage):
        return usage > self.threshold   

class SwapMonitorController:
    def __init__(self, interval=2):
        self.stats = SwapStats()
        self.detector = CriticalSwapDetector()
        self.interval = interval    

    def run(self):
        try:
            while True:
                total = self.stats.get_total_swap()
                free = self.stats.get_free_swap()
                used = self.stats.get_used_swap()
                percent = self.stats.get_percent_swap()

                logger.info(f"Total Swap: {format_bytes(total)}")
                logger.info(f"Free Swap: {format_bytes(free)}")
                logger.info(f"Used Swap: {format_bytes(used)}")
                logger.info(f"Percent Swap usage: {percent}%")

                if self.detector.detect_critical_total(self.stats.get_percent_swap()):
                    logger.warning(f" Total Swap usage is high: {self.stats.get_percent_swap()}%")
                    save_log_swap(total, used, percent)

                sleep(self.interval)
        except KeyboardInterrupt:
            logger.warning("Monitoramento interrompido pelo usuário.")
        except Exception as e:
            logger.exception(f"Erro inesperado: {e}")
