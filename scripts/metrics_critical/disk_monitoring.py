from time import sleep

from dotenv import load_dotenv
load_dotenv(dotenv_path=".env.local")

from psutil import disk_usage

from scripts.utils.logger import setup_logger
from scripts.utils.format_out import format_bytes
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
    def __init__(self, interval=2):
        self.stats = CriticalDiskDetector()
        self.interval = interval

    def run(self):
        try:
            while True:
                data = self.stats.get_critical_data_disk()
                logger.info(f"Disk total: {format_bytes(data['total'])}")
                logger.info(f"Disk usada: {format_bytes(data['used'])}, uso: {data['percent']}%")

                if self.is_critical_disk():
                    logger.warning(f"Uso critico de disco: {data['percent']}%")
                    save_log_disk(data['total'], data['used'], data['percent'])

                sleep(self.interval)

        except KeyboardInterrupt:
            logger.warning("Monitoramento interrompido pelo usuário.")
        except Exception as e:
            logger.exception(f"Erro inesperado: {e}")    

