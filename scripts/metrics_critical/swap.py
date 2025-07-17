import asyncio
import psutil as ps
from utils.logger import setup_logger
from collections import deque
from database.core.crud import create_swap_log
from sqlalchemy.orm import Session



logger = setup_logger()

class SwapCriticalDetector():
    def __init__(self, threshold=60, window_size=5):
        self.threshold = threshold
        self.window_size = window_size
        self._recent_percentages = deque(maxlen=self.window_size)
        self.was_critical = False
    def _get_current_percentage(self) -> float:
        return ps.swap_memory().percent

    def evaluate_critical_state_and_get_data(self) -> tuple[bool, dict]:
        current_percentage = self._get_current_percentage()
        self._recent_percentages.append(current_percentage)

        if len(self._recent_percentages) < self.window_size:
            self.was_critical = False
            mem_data = ps.swap_memory()
            return False, {"total": mem_data.total, "used": mem_data.used, "percent": current_percentage}
        
        moving_average = sum(self._recent_percentages) / len(self._recent_percentages)
        logger.info(f"[SWAP] Media móvel: {moving_average:.2f}%  |  leituras: {list(self._recent_percentages)}%")

        is_persist_critical = moving_average > self.threshold
        mem_data = ps.swap_memory()
        return is_persist_critical,{"total": mem_data.total, 
                                    "used": mem_data.used, 
                                    "percent": current_percentage}

class MonitorSwap:
    def __init__(self, interval=0.5, restart_script=1, db: Session = None):
        self.detector = SwapCriticalDetector()
        self.interval = interval
        self.restart_script = restart_script
        self.db = db

    async def run(self):
        try:
            while True:
                is_critical, data = await asyncio.to_thread(self.detector.evaluate_critical_state_and_get_data)
                if is_critical:
                    logger.warning(f"Uso de Swap critico: {data['percent']}%")
                    create_swap_log(self.db, data['total'], data['used'], data['percent'])
                await asyncio.sleep(self.interval)

        except Exception as e:
            logger.exception(f"Erro inesperado: {e}")
            await asyncio.sleep(self.restart_script)    

