import asyncio
from dotenv import load_dotenv
load_dotenv(dotenv_path=".env.local")

from psutil import  virtual_memory


from scripts.utils.logger import setup_logger
from scripts.utils.format_out import format_bytes
from database.writer_logs_db import save_log_ram


logger = setup_logger()


class CriticalRamDetector:
    def __init__(self, threshold=80):
        self.threshold = threshold

    def get_critical_data(self):
        mem = virtual_memory()
        return {
            "total": mem.total,
            "used": mem.used,
            "percent": mem.percent
        }
        
    def is_critical(self):
        return virtual_memory().percent > self.threshold


class RamMonitorController:
    def __init__(self, interval=1.5, restart_script=1):
        self.detector = CriticalRamDetector()
        self.interval = interval
        self.restart_script =  restart_script

    async def run(self):
        try:
            while True:
                data = self.detector.get_critical_data()
                logger.info(f"RAM total: {format_bytes(data['total'])}")
                logger.info(f"RAM usada: {format_bytes(data['used'])}, uso: {data['percent']}%")

                if self.detector.is_critical():
                    logger.warning(f"Uso critico de RAM: {data['percent']}%")
                    save_log_ram(data['total'], data['used'], data['percent'])

                await asyncio.sleep(self.interval)

        except Exception as e:
            logger.exception(f"Erro inesperado: {e}")        
            await asyncio.sleep(self.restart_script)
