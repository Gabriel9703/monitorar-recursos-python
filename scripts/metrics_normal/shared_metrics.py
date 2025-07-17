import psutil
from datetime import datetime
from pathlib import Path
from filelock import FileLock
import asyncio
import orjson
from utils.logger import setup_logger

logger = setup_logger()

class SharedMetricsWriter:
    def __init__(self, shared_dir="/home/gabriel/git/monitoring-system/database/json/shared_metrics"):
        self.shared_dir = Path(shared_dir)
        self.shared_dir.mkdir(exist_ok=True)
 

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


    async def _write_cpu_metrics(self):
        percent = await asyncio.to_thread(psutil.cpu_percent, interval=None, percpu=False)
        cores = await asyncio.to_thread(psutil.cpu_percent, interval=None, percpu=True)
        cpu_physical = await asyncio.to_thread(psutil.cpu_count, logical=False)
        cpu_logical = await asyncio.to_thread(psutil.cpu_count, logical=True)
        data = {
            'percent': percent,
            'cores': cores,
            'physical': cpu_physical,
            'logical': cpu_logical,
            'timestamp': datetime.now().isoformat()
        }   
        await self._save_metric("cpu.json", data)
    
    async def _write_ram_metrics(self):
        mem = await asyncio.to_thread(psutil.virtual_memory)
        data = {
            'total': mem.total,
            'available': mem.available,
            'used': mem.used,
            'percent': mem.percent,
            'timestamp': datetime.now().isoformat()
        }    
        await self._save_metric("ram.json", data) 


    async def _write_swap_metrics(self):
        swap = await asyncio.to_thread(psutil.swap_memory)
        data = {
            'total': swap.total,
            'free': swap.free,
            'used': swap.used,
            'percent': swap.percent,
            'timestamp': datetime.now().isoformat()
        }    
        await self._save_metric("swap.json", data) 


    async def _write_disk_metrics(self):
        disk = await asyncio.to_thread(psutil.disk_usage, "/")
        data = {
            'total': disk.total,
            'free': disk.free,
            'used': disk.used,
            'percent': disk.percent,
            'timestamp': datetime.now().isoformat()
        }
        await self._save_metric("disk.json", data) 
        

    async def _write_net_metrics(self):
        network = await asyncio.to_thread(psutil.net_io_counters)
        data = {
            'bytes_sent': network.bytes_sent,
            'bytes_recv': network.bytes_recv,
            'packets_sent': network.packets_sent,
            'packets_recv': network.packets_recv,
            'drops_in': network.dropin,
            'drops_out': network.dropout,
            'timestamp': datetime.now().isoformat()

        }    
        await self._save_metric("net.json", data) 


    async def write_all_metrics(self):
        await asyncio.gather(
        self._write_cpu_metrics(),
        self._write_disk_metrics(),
        self._write_net_metrics(),
        self._write_ram_metrics(),
        self._write_swap_metrics(), 
        self._write_temp_metrics()
        )

    async def run(self):
        try:
            while True:
                await self.write_all_metrics()
                await asyncio.sleep(1.3)
        
        except Exception as e:
            logger.exception(f"Erro inesperado: {e}")
           