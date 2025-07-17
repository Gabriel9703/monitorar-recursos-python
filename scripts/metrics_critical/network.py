import psutil as ps
import time
import asyncio
from utils.logger import setup_logger

logger = setup_logger()


class NetworkStats:
    def __init__(self):
        self._last = ps.net_io_counters()
        self._last_time = time.time()

    def get_stats(self):
        current = ps.net_io_counters()
        now = time.time()
        interval = now - self._last_time

        delta = {
            "bytes_sent": current.bytes_sent - self._last.bytes_sent,
            "bytes_recv": current.bytes_recv - self._last.bytes_recv,
            "packets_sent": current.packets_sent - self._last.packets_sent,
            "packets_recv": current.packets_recv - self._last.packets_recv,
            "errors_sent": current.errout - self._last.errout,
            "errors_recv": current.errin - self._last.errin,
            "drops_in": current.dropin - self._last.dropin,
            "drops_out": current.dropout - self._last.dropout,
            "bytes_sent_per_sec": (current.bytes_sent - self._last.bytes_sent) / interval,
            "bytes_recv_per_sec": (current.bytes_recv - self._last.bytes_recv) / interval,
        }

        self._last = current
        self._last_time = now
        return delta


class CriticalNetworkDetector:
    def __init__(self, threshold=10):
        self.threshold = threshold

    def detect(self, stats):
        critical = {}
        for key in ["errors_sent", "errors_recv", "drops_in", "drops_out"]:
            if stats[key] > self.threshold:
                critical[key] = stats[key]
        return critical


class MonitorNetwork:
    def __init__(self, interval=1, restart_script=1):
        self.stats = NetworkStats()
        self.detector = CriticalNetworkDetector()
        self.interval = interval
        self.restart_script = restart_script

    def get_stats_and_check(self):
        stats = self.stats.get_stats()
        critical = self.detector.detect(stats)
        return stats, critical

    async def run(self):
        try:
            while True:
                stats, critical = await asyncio.to_thread(self.get_stats_and_check)
                logger.info(
                    f"Rede: ↑ {stats['bytes_sent_per_sec']:.2f} B/s ↓ {stats['bytes_recv_per_sec']:.2f} B/s"
                )

                if critical:
                    for k, v in critical.items():
                        logger.warning(f"🚨 Anomalia detectada: {k} = {v}")

                await asyncio.sleep(self.interval)

        except Exception as e:
            logger.exception(f"Erro inesperado: {e}")
            await asyncio.sleep(self.restart_script)
