from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env.local")

from psutil import cpu_percent
from scripts.utils.logger import setup_logger
from time import sleep
from database.save_logs_db import save_log_cpu, save_log_cpu_core

logger = setup_logger()

   
class CriticalCpuDetector:
    def __init__(self, threshold=80):
        self.threshold = threshold

    def get_total_usage(self):
        return cpu_percent(interval=0.1, percpu=False)
    
    def get_each_usage(self):
        return cpu_percent(interval=0.2, percpu=True)

    def get_critical_cores(self, each):
        return [(i, usage) for i, usage in enumerate(each, start=1) if usage > self.threshold]


class CpuMonitorController:
    def __init__(self, interval=1):
        self.detector = CriticalCpuDetector()
        self.interval = interval 

    def run(self):
        try:
            while True:
                total = self.detector.get_total_usage()
                each = self.detector.get_each_usage()

                logger.info(f"Total CPU Usage: {total}%")
                if total > self.detector.threshold:
                    logger.warning(f"Total CPU usage is critical: {total}%")
                    save_log_cpu(total) 

                for i, usage in enumerate(each, start=1):
                    logger.info(f"CPU {i} Usage: {usage}%")
                    
                critical_cores = self.detector.get_critical_cores(each)
                for i, usage in critical_cores:
                    logger.warning(f"CPU {i} usage is critical: {usage}%")
                    save_log_cpu_core(i, usage)  

                sleep(self.interval)
        except KeyboardInterrupt:
            logger.warning("Monitoramento interrompido pelo usuário.")
        except Exception as e:
            logger.exception(f"Erro inesperado: {e}")
 
   