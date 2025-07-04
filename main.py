from threading import Thread
from scripts.metrics_critical.cpu_monitoring import CpuMonitorController
from scripts.metrics_critical.network_monitoring import NetworkMonitorController
from scripts.metrics_critical.ram_monitoring import RamMonitorController
from scripts.metrics_critical.swap_monitoring import SwapMonitorController

if __name__ == "__main__":
    cpu_monitor = CpuMonitorController()
    network_monitor = NetworkMonitorController(interval=2)
    ram_monitor = RamMonitorController(interval=1.5) 
    swap_monitor = SwapMonitorController(interval=2) 

    Thread(target=ram_monitor.run).start()
    Thread(target=cpu_monitor.run).start()
    Thread(target=network_monitor.run).start()
    Thread(target=swap_monitor.run).start()