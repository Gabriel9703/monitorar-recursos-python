from dotenv import load_dotenv
import os

# Carrega o .env local para variáveis de ambiente
load_dotenv(dotenv_path=".env.local")
from time import sleep

from psutil import swap_memory

from scripts.utils.logger import setup_logger
from scripts.utils.format_out import format_bytes
from database.save_logs_db import save_log_swap

logger = setup_logger()

class CriticalSwapDetector:
    def __init__(self, threshold=80):
        self.threshold = threshold

    def get_critical_data_swap(self):
        mem = swap_memory()
        return {"total": mem.total, "used": mem.used, "percent": mem.percent}

    def is_critical_swap(self):
        return swap_memory().percent > self.threshold


class SwapMonitorController:
    def __init__(self, interval=2):
        self.detector = CriticalSwapDetector()
        self.interval = interval

    def run(self):
        try:
            while True:
                data = self.detector.get_critical_data_swap()
                logger.info(f"Swap total: {format_bytes(data['total'])}")
                logger.info(
                    f"Swap usada: {format_bytes(data['used'])}, uso: {data['percent']}%"
                )

                if self.detector.is_critical_swap():
                    logger.warning(f" Uso critico de Swap: {data['percent']}%")
                    save_log_swap(data["total"], data["used"], data["percent"])

                sleep(self.interval)

        except KeyboardInterrupt:
            logger.warning("Monitoramento interrompido pelo usuário.")
        except Exception as e:
            logger.exception(f"Erro inesperado: {e}")
