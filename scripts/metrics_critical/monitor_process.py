from dotenv import load_dotenv
load_dotenv(dotenv_path=".env.local")
import psutil
import pandas as pd

import asyncio
from database.writer_logs_db import save_log_process
from scripts.utils.logger import setup_logger


logger = setup_logger()

class CriticalProcessesDetector:
    def __init__(self, threshold_cpu=200.0, top_n=10):
        self.threshold_cpu = threshold_cpu
        self.top_n = top_n

    
    def get_top_processes(self):
        # Pré carrega CPU para medição correta
        for proc in psutil.process_iter():
            try:
                proc.cpu_percent(interval=None)
            except:
                continue

        # Pequena pausa
        psutil.cpu_percent(interval=0.1)

        processes_data =[]
        for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'status']):
            try:
                processes_data.append(proc.info)
            except:
                continue

        return sorted(processes_data, key=lambda x: x['cpu_percent'], reverse=True)[:self.top_n]

    def get_critical_processes(self, processes):
        return[ p for p in processes if p['cpu_percent'] > self.threshold_cpu]
    
class ProcessMonitorController:
    def __init__(self, interval=5, restart_script=1):
        self.detector = CriticalProcessesDetector()
        self.interval = interval
        self.restart_script = restart_script

    async def run(self):
        try:
            while True:
                top = self.detector.get_top_processes(limit=10)
                critical = self.detector.get_critical_processes(top)
                for proc in critical:
                    logger.warning(f"Processo: {proc['pid']} - Name: {proc['name']} |  CPU: {proc['cpu_percent']}%")
                    save_log_process(proc)

                await asyncio.sleep(self.restart_script)
        
        except Exception as e:
            logger.exception(f"Erro inesperado: {e}")       
            await asyncio.sleep(self.restart_script)


