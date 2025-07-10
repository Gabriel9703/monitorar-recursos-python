import asyncio

from dotenv import load_dotenv
load_dotenv(dotenv_path=".env.local")

from psutil import net_io_counters

from scripts.utils.logger import setup_logger
from database.writer_logs_db import save_log_network


logger = setup_logger()


class NetworkStats:
    def __init__(self):
        self._last = net_io_counters()

    def get_stats(self):
        current = net_io_counters()
        delta = {
            "bytes_sent": current.bytes_sent - self._last.bytes_sent,
            "bytes_recv": current.bytes_recv - self._last.bytes_recv,
            "packets_sent": current.packets_sent - self._last.packets_sent,
            "packets_recv": current.packets_recv - self._last.packets_recv,
            "errors_sent": current.errout - self._last.errout,
            "errors_recv": current.errin - self._last.errin,
            "drops_in": current.dropin - self._last.dropin,
            "drops_out": current.dropout - self._last.dropout,
        }
        self._last = current
        return delta
    
class CriticalNetworkDetector:
    def detect(self, stats):
        critical = {}
        if stats["errors_sent"] > 0:
            critical["errors_sent"] = stats["errors_sent"]
        if stats["errors_recv"] > 0:
            critical["errors_recv"] = stats["errors_recv"]
        if stats["drops_in"] > 0:
            critical["drops_in"] = stats["drops_in"]
        if stats["drops_out"] > 0:
            critical["drops_out"] = stats["drops_out"]
        return critical

class NetworkMonitorController:
    def __init__(self, interval=2, restart_script=1):
        self.stats = NetworkStats()
        self.detector = CriticalNetworkDetector()
        self.interval = interval
        self.restart_script = restart_script


    async def run(self):
        try:
            while True:
                stats = self.stats.get_stats()
                logger.info(f"Rede: {stats}")
                save_log_network(stats)

                critical = self.detector.detect(stats)
                for k, v in critical.items():
                    logger.warning(f"Anomalia detectada: {k} = {v}")

                await asyncio.sleep(self.interval)
    
        except Exception as e:
            logger.exception(f"Erro inesperado: {e}")
            await asyncio.sleep(self.restart_script)      