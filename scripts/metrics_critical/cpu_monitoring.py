from dotenv import load_dotenv
load_dotenv(dotenv_path=".env.local")

import asyncio
from psutil import cpu_percent

from scripts.utils.logger import setup_logger
from database.writer_logs_db import save_log_cpu, save_log_cpu_core


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
    def __init__(self, interval=0.5, restart_script=0.5):
        self.detector = CriticalCpuDetector()
        self.interval = interval 
        self.restart_script = restart_script


    async def run(self):
        try:
            while True:
                total = self.detector.get_total_usage()
                each = self.detector.get_each_usage()

                if total > self.detector.threshold:
                    logger.warning(f"Total CPU usage is critical: {total}%")
                    save_log_cpu(total) 
                
                critical_cores = self.detector.get_critical_cores(each)
                for i, usage in critical_cores:
                    logger.warning(f"CPU {i} usage is critical: {usage}%")
                    save_log_cpu_core(i, usage)  

                await asyncio.sleep(self.interval)
        
        except Exception as e:
            logger.exception(f"Erro inesperado: {e}, restartando em 1s..")
            await asyncio.sleep(self.restart_script)
 
   