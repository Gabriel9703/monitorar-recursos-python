import asyncio

from dotenv import load_dotenv
load_dotenv(dotenv_path=".env.local")

from psutil import swap_memory

from scripts.utils.logger import setup_logger
from scripts.utils.format_out import format_bytes
from database.writer_logs_db import save_log_swap


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
    def __init__(self, interval=2, restart_script=1):
        self.detector = CriticalSwapDetector()
        self.interval = interval
        self.restart_script = restart_script


    async def run(self):
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

                await asyncio.sleep(self.interval)

        except Exception as e:
            logger.exception(f"Erro inesperado: {e}")
            await asyncio.sleep(self.restart_script)   