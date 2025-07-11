from dotenv import load_dotenv
load_dotenv(dotenv_path=".env.local")

from psutil import disk_usage
import asyncio
from scripts.utils.logger import setup_logger
from database.writer_logs_db import save_log_disk


logger = setup_logger()


class CriticalDiskDetector:
    def __init__(self, threshold=60):
        self.threshold = threshold

    def get_critical_data_disk(self):
        disk = disk_usage("/")
        return {
            "total": disk.total,
            "used": disk.used,
            "percent": disk.percent
        }
    
    def is_critical_disk(self):
        return disk_usage("/").percent > self.threshold
    
class DiskMonitorController:
    def __init__(self, interval=3, restart_script=1):
        self.stats = CriticalDiskDetector()
        self.interval = interval
        self.restart_script = restart_script

    async def run(self):
        try:
            while True:
                data = self.stats.get_critical_data_disk()
                if self.stats.is_critical_disk():
                    logger.warning(f"Uso critico de disco: {data['percent']}%")
                    save_log_disk(data['total'], data['used'], data['percent'])

                await asyncio.sleep(self.interval)

        except Exception as e:
            logger.exception(f"Erro inesperado: {e} restartando em 1s..")
            await asyncio.sleep(self.restart_script)    

