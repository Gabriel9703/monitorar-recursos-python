import psutil as ps
from utils.logger import setup_logger
import asyncio
from collections import deque
from database.core.crud import create_disk_log
from sqlalchemy.orm import Session


logger = setup_logger()


class DiskCriticalDetector:
    def __init__(self, threshold=60, window_size=5):
        self.threshold = threshold
        self.window_size = window_size
        self._recent_percentages = deque(maxlen=self.window_size)
        self._data_disk = None

    def _get_current_percentage(self) -> float:
        self._data_disk = ps.disk_usage("/")
        self.disk_percent = self._data_disk.percent
        return self.disk_percent
    
    def evaluate_critical_state_and_get_data(self) -> tuple[bool, dict]:
        current_percentage = self._get_current_percentage()
        self._recent_percentages.append(current_percentage)

        if len(self._recent_percentages) < self.window_size:
            return False, {"total": self._data_disk.total, "used": self._data_disk.used, "percent": current_percentage}
        
        moving_average = sum(self._recent_percentages) / len(self._recent_percentages)
        logger.info(f"[DISK] Media móvel: {moving_average:.2f}%  | leituras: {list(self._recent_percentages)}")

        is_persist_critical = moving_average > self.threshold
        return is_persist_critical,  {"total": self._data_disk.total, "used": self._data_disk.used, "percent": current_percentage}
    
class MonitorDisk:
    def __init__(self, interval=10, restart_script=5, db: Session = None):
        self.detector = DiskCriticalDetector()
        self.interval = interval
        self.restart_script = restart_script
        self.db = db


    async def run(self):
        try:
            while True:
                is_critical, data = await asyncio.to_thread(self.detector.evaluate_critical_state_and_get_data)
                if is_critical:
                    logger.warning(f"Uso de Disco critico: {data['percent']}%")
                    create_disk_log(self.db, data['total'], data['used'], data['percent'])    
                await asyncio.sleep(self.interval)

        except Exception as e:
            logger.exception(f"Erro inesperado: {e}")
            await asyncio.sleep(self.restart_script)    

