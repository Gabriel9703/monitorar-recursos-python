from filelock import FileLock
import orjson
from pathlib import Path
from dashboard.utils import setup_logger
from pathlib import Path
import os

logger = setup_logger()

def read_metric_safely(filename):
    PATH = Path(os.getenv("METRICS_PATH", "/app/database/json/shared_metrics"))
    filepath = Path(PATH) / filename
    lockfile = str(filepath) + ".lock"

    try:
        with FileLock(lockfile, timeout=1): 
            if filepath.exists():
                data = filepath.read_bytes()
                return orjson.loads(data)
            else:
                return None
    except FileNotFoundError:
        logger.warning(f"Arquivo {filename} nao encontrado.")
        return None
    except orjson.JSONDecodeError:
        logger.warning(f"Arquivo {filename} nao pode ser lido.")
        return None        
    except Exception as e:
        logger.error(f"Erro ao ler {filename}: {e}")
        return None