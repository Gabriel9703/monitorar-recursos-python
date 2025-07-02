from psutil import cpu_percent, cpu_count
from scripts.utils.logger import setup_logger
from time import sleep
from database.logs_repository import save_log_cpu
logger = setup_logger()


class CpuStats:
    def __init__(self):
        pass

    def get_total_usage(self):
        return cpu_percent(interval=1, percpu=False)

    def get_each_core_usage(self):
        return cpu_percent(interval=1, percpu=True)

    def get_phisical_cores(self):
        return cpu_count(logical=False) 

    def get_logical_cores(self):
        return cpu_count(logical=True) 
    
class CriticalCpuDetector:
    def __init__(self, threshold=80):
        self.threshold = threshold

    def detect_critical_total(self, usage):
        return usage > self.threshold

    def detect_critical_each(self, usage_list):
        return [(i, usage) for i, usage in enumerate(usage_list, start=1) if usage > self.threshold]


class CpuMonitorController:
    def __init__(self, interval=2):
        self.stats = CpuStats()
        self.detector = CriticalCpuDetector()
        self.interval = interval 
    def run(self):
        try:
            while True:
                total = self.stats.get_total_usage() 
                each = self.stats.get_each_core_usage()

                logger.info(f"Total CPU Usage: {total}%")
                if self.detector.detect_critical_total(total):
                    logger.warning(f"Total CPU usage is critical: {total}%")
                    save_log_cpu(total) 

                for i, usage in enumerate(each, start=1):
                    logger.info(f"CPU {i} Usage: {usage}%")
                    
                critical_cores = self.detector.detect_critical_each(each)
                for i, usage in critical_cores:
                    logger.warning(f"CPU {i} usage is critical: {usage}%")
                    save_log_cpu(usage)  

                sleep(self.interval)

        except KeyboardInterrupt:
            logger.warning("Monitoramento interrompido pelo usuário.")
        except Exception as e:
            logger.exception(f"Erro inesperado: {e}")


 
   