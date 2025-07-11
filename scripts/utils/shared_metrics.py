import psutil
import json
from datetime import datetime
from pathlib import Path
import time

class SharedMetricsWriter:
    def __init__(self, shared_dir="/app/shared_metrics"):
        self.shared_dir = Path(shared_dir)
        self.shared_dir.mkdir(exist_ok=True)

    def _save_metric(self, filename, data):
        (self.shared_dir / filename).write_text(json.dumps(data))

    def _write_cpu_metrics(self):
        data = {
            'percent': psutil.cpu_percent(interval=0.1, percpu=False),
            'cores': psutil.cpu_percent(interval=0.2, percpu=True),
            'cpu_physical': psutil.cpu_count(logical=False),
            'cpu_logical': psutil.cpu_count(logical=True),
            'timestamp': datetime.now().isoformat()
        }   
        self._save_metric("cpu.json", data)


    
    def _write_ram_metrics(self):
        mem = psutil.virtual_memory()
        data = {
            'total': mem.total,
            'available': mem.available,
            'used': mem.used,
            'percent': mem.percent,
            'timestamp': datetime.now().isoformat()
        }    
        self._save_metric("ram.json", data) 


    def _write_swap_metrics(self):
        swap = psutil.swap_memory()
        data = {
            'total': swap.total,
            'free': swap.free,
            'used': swap.used,
            'percent': swap.percent,
            'timestamp': datetime.now().isoformat()
        }    
        self._save_metric("swap.json", data) 


    def _write_disk_metrics(self):
        disk = psutil.disk_usage('/')
        data = {
            'total': disk.total,
            'free': disk.free,
            'used': disk.used,
            'percent': disk.percent
        }
        self._save_metric("disk.json", data) 
        

    def _write_net_metrics(self):
        network = psutil.net_io_counters()
        data = {
            'bytes_sent': network.bytes_sent,
            'bytes_recv': network.bytes_recv,
            'packets_sent': network.packets_sent,
            'packets_recv': network.packets_recv,
            'drops_in': network.dropin,
            'drops_out': network.dropout
        }    
        self._save_metric("net.json", data) 


    def _write_process_metrics(self):
        process_data = []
        summary = {'total': 0, 'running': 0, 'sleeping': 0, 'zombie': 0}
        
        # Pré-aquece o cálculo de CPU
        for proc in psutil.process_iter():
            try:
                proc.cpu_percent(interval=None)
            except:
                continue
        
        # Espera para cálculo preciso
        time.sleep(0.1)
        
        # Coleta dados dos processos
        for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'status']):
            try:
                info = proc.info
                summary['total'] += 1
                summary[info['status'].lower()] += 1
                process_data.append(info)
            except:
                continue
        
        # Ordena e limita
        top_cpu = sorted(process_data, key=lambda x: x['cpu_percent'], reverse=True)[:10]
        
        # Prepara os dados para JSON
        data = {
            'summary': summary,
            'top_processes': top_cpu,
            'timestamp': datetime.now().isoformat()
        }
        
        self._save_metric("processes.json", data)
        
    def write_all_metrics(self):
        self._write_cpu_metrics()
        self._write_disk_metrics()
        self._write_net_metrics()
        self._write_ram_metrics()
        self._write_swap_metrics()
        self._write_process_metrics()    
