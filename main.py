import asyncio
from scripts.metrics_normal.shared_metrics import SharedMetricsWriter
from scripts.metrics_critical.cpu_overall import MonitorCpuOverall
from scripts.metrics_critical.ram import MonitorRam
from scripts.metrics_critical.swap import MonitorSwap
from scripts.metrics_critical.disk import MonitorDisk
from scripts.metrics_critical.cpu_cores import MonitorCpuCores
from utils.logger import setup_logger
from database.core.conexao import Base, engine
import database.core.models 
from database.core.conexao import SessionLocal


Base.metadata.create_all(bind=engine)


logger = setup_logger()



async def main():
    logger.info("Iniciando monitoramento...")
    db = SessionLocal()
    metrics_normals = SharedMetricsWriter()
    disk_detector = MonitorDisk(db=db)
    ram_detector = MonitorRam(db=db)
    swap_detector = MonitorSwap(db=db)
    cpu_overall_detector = MonitorCpuOverall(db=db)
    cpu_cores = MonitorCpuCores(db=db)
   
    await asyncio.gather(
           metrics_normals.run(),
           disk_detector.run(),
           ram_detector.run(),
           swap_detector.run(),
           cpu_overall_detector.run(),
           cpu_cores.run()
                   )
if __name__ == "__main__":  
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Monitoramento interrompido pelo usuário.")
    except Exception as e:
            logger.exception(f"Erro inesperado: {e}", exc_info=True)    
