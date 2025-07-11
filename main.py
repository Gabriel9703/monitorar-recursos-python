import asyncio
from scripts.metrics_critical.cpu_monitoring import CpuMonitorController
from scripts.metrics_critical.network_monitoring import NetworkMonitorController
from scripts.metrics_critical.ram_monitoring import RamMonitorController
from scripts.metrics_critical.swap_monitoring import SwapMonitorController
from scripts.metrics_critical.monitor_process import ProcessMonitorController
from scripts.metrics_critical.disk_monitoring import DiskMonitorController
from scripts.utils.logger import setup_logger

logger = setup_logger()


async def main():
    disk_monitor = DiskMonitorController()
    processes = ProcessMonitorController()
    cpu_monitor = CpuMonitorController()
    network_monitor = NetworkMonitorController()
    ram_monitor = RamMonitorController() 
    swap_monitor = SwapMonitorController() 

    from scripts.utils.shared_metrics import SharedMetricsWriter
    metrics_write = SharedMetricsWriter()
    async def write_normal_metrics():
        while True:
            metrics_write.write_all_metrics()
            await asyncio.sleep(1)

    try:
        await asyncio.gather(
            cpu_monitor.run(),
            network_monitor.run(),
            ram_monitor.run(),
            swap_monitor.run(),
            processes.run(),
            disk_monitor.run(),
            write_normal_metrics(),

        )
    except KeyboardInterrupt:
        logger.exception("Pausado pelo usuario")
    except Exception as e:
        logger.error(f"Erro {e} inesperado")    


if __name__ == "__main__":
    asyncio.run(main())