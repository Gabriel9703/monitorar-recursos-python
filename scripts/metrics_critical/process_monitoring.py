from time import sleep
from psutil import process_iter, AccessDenied, ZombieProcess, NoSuchProcess
from scripts.utils.logger import setup_logger
from scripts.utils.format_out import format_bytes

logger = setup_logger()
MAX_MEMORY_RSS = 2 * 1024**3  

class ProcessNormal:
    def __init__(self):
        pass

    def get_process_system(self):
        process = []
        for proc in process_iter(['pid', 'name', 'username','cpu_percent', 
                                  'memory_info', 'memory_percent', 'status',
                                  'num_threads','cmdline']):
            try:
                process_system = {
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'username': proc.info['username'],
                    'cpu': proc.cpu_percent(interval=0.1),
                    'mem_rss': proc.info['memory_info'].rss,
                    'mem_vms': proc.info['memory_info'].vms,
                    'mem_percent': proc.info['memory_percent'],
                    'cmdline': proc.info['cmdline'],
                    'num_threads': proc.info['num_threads'],
                    'status': proc.info['status']
                }
                process.append(process_system)
            except (AccessDenied, ZombieProcess, NoSuchProcess):
                continue
       
        return process

class CriticalProcess:
    def __init__(self, threshold_mem=MAX_MEMORY_RSS, threshold_cpu=70):
        self.threshold_mem_rss = threshold_mem
        self.threshold_cpu = threshold_cpu  

    def is_critical_mem(self, processes):
        for proc in processes:
            if proc['mem_rss'] > self.threshold_mem_rss:
                logger.warning(f"PID: {proc['pid']} - NAME: {proc['name']} - MEM_RSS: {format_bytes(proc['mem_rss'])} - STATUS: {proc['status']}")

    def is_critical_cpu(self, processes):
        for proc in processes:
            if proc['cpu'] > self.threshold_cpu:
                logger.warning(f"PID: {proc['pid']} - NAME: {proc['name']} - CPU: {proc['cpu']}% - STATUS: {proc['status']}")

class MonitorProcess:
    def __init__(self):
        self.metrics_normal = ProcessNormal()
        self.critical = CriticalProcess()

    def views_metrics_process(self, processes):
        for proc in processes:
            logger.info(f"PID: {proc['pid']} - NAME: {proc['name']} - USERNAME: {proc['username']}")
            logger.info(f"MEM_RSS: {format_bytes(proc['mem_rss'])} - MEM_VMS: {format_bytes(proc['mem_vms'])} - MEM(%): {proc['mem_percent']}")
            logger.info(f"CPU: {proc['cpu']}% - NUM_THREADS: {proc['num_threads']} - STATUS: {proc['status']}")
            logger.info(f"CMDLINE: {proc['cmdline']}")
            print('-' * 30, '\n')

    def run(self):
        while True:
            try:
                processes = self.metrics_normal.get_process_system()    
                self.views_metrics_process(processes)
                self.critical.is_critical_mem(processes)
                self.critical.is_critical_cpu(processes)
                sleep(10)
            except (AccessDenied, ZombieProcess, NoSuchProcess):
                continue

if __name__ == '__main__':
    control_process = MonitorProcess()
    control_process.run()
