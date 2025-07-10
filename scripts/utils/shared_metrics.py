import psutil
import json
from datetime import datetime
from pathlib import Path


class SharedMetricsWriter:
    def __init__(self, shared_dir="/app/shared_metrics"):
        self.shared_dir = Path(shared_dir)
        self.shared_dir.mkdir(exist_ok=True)

    def write_cpu_metrics(self):
        data = {
            'percent': psutil.cpu_percent(interval=1),
            'cores': psutil.cpu_percent(interval=1, percpu=True),
            'cpu_physical': psutil.cpu_count(logical=False),
            'cpu_logical': psutil.cpu_count(logical=True),
            'timestamp': datetime.now().isoformat()
        }   
        (self.shared_dir / 'cpu.json').write_text(json.dumps(data)) 

    
    def write_ram_metrics(self):
        mem = psutil.virtual_memory()
        data = {
            'total': mem.total,
            'available': mem.available,
            'used': mem.used,
            'percent': mem.percent,
            'timestamp': datetime.now().isoformat()
    
        }    
        (self.shared_dir / 'ram.json').write_text(json.dumps(data)) 


    def write_swap_metrics(self):
        swap = psutil.swap_memory()
        data = {
            'total': swap.total,
            'free': swap.free,
            'used': swap.used,
            'percent': swap.percent,
            'timestamp': datetime.now().isoformat()
        }    
        (self.shared_dir / 'swap.json').write_text(json.dumps(data)) 


    def write_disk_metrics(self):
        disk = psutil.disk_usage('/')
        data = {
            'total': disk.total,
            'free': disk.free,
            'used': disk.used,
            'percent': disk.percent
        }
        (self.shared_dir / 'disk.json').write_text(json.dumps(data)) 
        
    def write_net_metrics(self):
        network = psutil.net_io_counters()
        data = {
            'bytes_sent': network.bytes_sent,
            'bytes_recv': network.bytes_recv,
            'packets_sent': network.packets_sent,
            'packets_recv': network.packets_recv,
            'drops_in': network.dropin,
            'drops_out': network.dropout
        }    
        (self.shared_dir / 'net.json').write_text(json.dumps(data)) 

    def write_all_metrics(self):
        self.write_cpu_metrics()
        self.write_disk_metrics()
        self.write_net_metrics()
        self.write_ram_metrics()
        self.write_swap_metrics()    
