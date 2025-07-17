from dotenv import load_dotenv
load_dotenv(dotenv_path=".env.local")
import psutil
from core.database import SessionLocal
import asyncio
from core.crud import create_process_log
from scripts.metrics_normal.logger import setup_logger


logger = setup_logger()

class CriticalProcessesDetector:
    def __init__(self, threshold_cpu=70.0, top_n=10):
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
                db = SessionLocal()
                top = self.detector.get_top_processes()
                critical = self.detector.get_critical_processes(top)
                for proc in critical:
                    logger.warning(f"Processo: {proc['pid']} - Name: {proc['name']} |  CPU: {proc['cpu_percent']}%")
                    create_process_log(db, proc['pid'], proc['name'], proc['username'], proc['cpu_percent'], proc['memory_percent'], proc['status'])

                await asyncio.sleep(self.restart_script)
        
        except Exception as e:
            logger.exception(f"Erro inesperado: {e}")       
            await asyncio.sleep(self.restart_script)


