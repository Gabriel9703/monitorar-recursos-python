import psutil
from datetime import datetime
from pathlib import Path
import time
from filelock import FileLock
import asyncio



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
        