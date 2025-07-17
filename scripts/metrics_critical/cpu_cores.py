import psutil as ps
from utils.logger import setup_logger
import asyncio
from collections import deque
from database.core.crud import create_cpu_core_log
from sqlalchemy.orm import Session
logger = setup_logger()


class CpuCoresDetectorCritical():
    def __init__(self, threshold=80, window_size=5):
        self.threshold = threshold
        self.window_size = window_size
        self._recent_cores_percentages: dict[int, deque[float]] = {} 
        ps.cpu_percent(percpu=True, interval=None) 
    def _get_current_percentage(self) -> list[float]:
        current_percent = ps.cpu_percent(interval=None, percpu=True)
        for i in range(len(current_percent)):
            if i not in self._recent_cores_percentages:
                self._recent_cores_percentages[i] = deque(maxlen=self.window_size)  
        return current_percent
    
    def evaluate_critical_state_and_get_data(self) -> tuple[bool, dict]:
        current_percentage = self._get_current_percentage()
        critical_core_info = []
        is_any_core_critical = False

        for i, percent in enumerate(current_percentage):
            self._recent_cores_percentages[i].append(percent)

            if len(self._recent_cores_percentages[i]) < self.window_size:
                continue

            moving_average = sum(self._recent_cores_percentages[i]) / len(self._recent_cores_percentages[i])
            logger.info(f"[CORE {i}] Media móvel: {moving_average:.2f}%  | Leituras: {list(self._recent_cores_percentages[i])}%")
            if moving_average > self.threshold:
                is_any_core_critical = True
                critical_core_info.append({"core": i, "percent": percent, "avg": moving_average})
       
        return is_any_core_critical, {
    "type": "per_cpu",
    "critical_cores": critical_core_info,
    "all_cores_percent": current_percentage,
}
    
class MonitorCpuCores():
    def __init__(self, interval=1, restart_script=0.9, db: Session = None):
        self.detector = CpuCoresDetectorCritical()
        self.interval = interval
        self.restart_script = restart_script
        self.db = db
    async def run(self):
        try:
            while True:
                is_critical, data = await asyncio.to_thread(self.detector.evaluate_critical_state_and_get_data)
                if is_critical:
                    logger.warning(f"Núcleos críticos detectados: {data['critical_cores']}")
                    for core_info in data["critical_cores"]:
                        create_cpu_core_log(
                            db=self.db,
                            core_number=core_info["core"],
                            usage_percent=core_info["percent"]
                        )   

                await asyncio.sleep(self.interval)    

        except Exception as e:
            logger.exception(f"Erro inesperado: {e}")        
    