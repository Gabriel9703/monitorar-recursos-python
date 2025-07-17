import asyncio
import psutil as ps
from collections import deque
from database.core.crud import create_cpu_log
from sqlalchemy.orm import Session
from utils.logger import setup_logger


logger = setup_logger()

   
class CpuCriticalDetector():
    def __init__(self, threshold=80, window_size=5):
        self.threshold = threshold
        self.window_size = window_size
        self._recent_percentages = deque(maxlen=self.window_size)
        ps.cpu_percent(interval=None)

        
    def _get_current_percentage(self) -> float:
        return ps.cpu_percent(interval=None)

    def evaluate_critical_state_and_get_data(self) -> tuple[bool, dict]:
        current_percentage = self._get_current_percentage()
        self._recent_percentages.append(current_percentage)
        
        if len(self._recent_percentages) < self.window_size:
            return False, {"type":"overall_cpu", "percent": current_percentage}
        
        moving_average = sum(self._recent_percentages) / len(self._recent_percentages)
        logger.info(f"[CPU Overall] Média móvel: {moving_average:.2f}% | Leituras: {list(self._recent_percentages)}")


        is_persist_critical = moving_average > self.threshold
        return is_persist_critical, {"type": "overall_cpu",
                                     "percent": current_percentage,
                                       "avg": moving_average} 


class MonitorCpuOverall:
    def __init__(self, interval=1, restart_script=0.9, db: Session= None):
        self.detector = CpuCriticalDetector()
        self.interval = interval
        self.restart_script = restart_script
        self.db = db

    async def run(self):
        try:
            while True:
                is_critical, data = await asyncio.to_thread(self.detector.evaluate_critical_state_and_get_data)
                if is_critical:
                    logger.warning(f"Uso de CPU critico: {data['percent']}%")
                    create_cpu_log(self.db, data['percent'])
                await asyncio.sleep(self.interval)

        except Exception as e:
            logger.exception(f"Erro inesperado: {e}")
            await asyncio.sleep(self.restart_script)