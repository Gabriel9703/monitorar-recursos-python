import asyncio
import psutil
from datetime import datetime
from filelock import FileLock
import orjson

class MonitorTemperaturas:
    def __init__(self, shared_dir):
        self.shared_dir = shared_dir

    async def _save_metric(self, filename, data):
        filepath = self.shared_dir / filename
        lockfile = str(filepath) + ".lock"

        def write_file():
            with FileLock(lockfile, timeout=1):
                filepath.write_bytes(orjson.dumps(data))

        return await asyncio.to_thread(write_file)

    async def _write_temp_metrics(self):
        temps = await asyncio.to_thread(psutil.sensors_temperatures)
        output = {}

        for fonte, sensores in temps.items():
            output[fonte] = []
            for s in sensores:
                output[fonte].append({
                    'label': s.label,
                    'current': s.current,
                    'high': s.high,
                    'critical': s.critical,
                })

        data = {
            'temperatures': output,
            'timestamp': datetime.now().isoformat()
        }

        await self._save_metric("temp.json", data)
