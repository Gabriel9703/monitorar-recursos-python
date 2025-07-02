from time import sleep

from psutil import  virtual_memory

from scripts.utils.logger import setup_logger
from scripts.utils.format_out import format_bytes
from database.logs_repository import save_log_ram

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
    def __init__(self, interval=1.5):
        self.detector = CriticalRamDetector()
        self.interval = interval

    def run(self):
        try:
            while True:
                data = self.detector.get_critical_data()
                logger.info(f"RAM total: {format_bytes(data['total'])}")
                logger.info(f"RAM usada: {format_bytes(data['used'])}, uso: {data['percent']}%")

                if self.detector.is_critical():
                    logger.warning(f"Uso critico de RAM: {data['percent']}%")
                    save_log_ram(data['total'], data['used'], data['percent'])

                sleep(self.interval)

        except KeyboardInterrupt:
            logger.warning("Monitoramento interrompido pelo usuário.")
        except Exception as e:
            logger.exception(f"Erro inesperado: {e}")        

if __name__ == "__main__":
    RamMonitorController().run()