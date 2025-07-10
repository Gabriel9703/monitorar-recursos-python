import psutil
import pandas as pd
import time

def get_process_summary_and_top(limit=10):
    total = 0
    running = 0
    sleeping = 0
    zombie = 0
    process_data = []

    for proc in psutil.process_iter():
        try:
            proc.cpu_percent(interval=None)
        except:
            continue

    psutil.cpu_percent(interval=0.1)

    for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'status']):
        try:
            info = proc.info
            total += 1
            if info['status'] == psutil.STATUS_RUNNING:
                running += 1
            elif info['status'] == psutil.STATUS_SLEEPING:
                sleeping += 1
            elif info['status'] == psutil.STATUS_ZOMBIE:
                zombie += 1

            process_data.append(info)
        except:
            continue

    top_cpu = sorted(process_data, key=lambda x: x['cpu_percent'], reverse=True)[:limit]
    df_top = pd.DataFrame(top_cpu)

    summary = {
        'total': total,
        'running': running,
        'sleeping': sleeping,
        'zombie': zombie
    }

    return summary, df_top[['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'status']]



