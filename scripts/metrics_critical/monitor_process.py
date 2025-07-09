from dotenv import load_dotenv
load_dotenv(dotenv_path=".env.local")
import psutil
import pandas as pd
from time import sleep



def get_process_summary_and_top(limit=10):
    total = 0
    running = 0
    sleeping = 0
    zombie = 0
    process_data = []

    # Primeira coleta para CPU
    for proc in psutil.process_iter():
        try:
            proc.cpu_percent(interval=None)
        except:
            continue

    # Pequena pausa
    psutil.cpu_percent(interval=0.1)

    for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'status']):
        try:
            info = proc.info
            status = info['status']
            total += 1
            if status == psutil.STATUS_RUNNING:
                running += 1
            elif status == psutil.STATUS_SLEEPING:
                sleeping += 1
            elif status == psutil.STATUS_ZOMBIE:
                zombie += 1

            process_data.append(info)
        except:
            continue

    top_cpu = sorted(process_data, key=lambda x: x['cpu_percent'], reverse=True)[:limit]

    df_top = pd.DataFrame(top_cpu)
    df_top = df_top[['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'status']]

    summary = {
        'total': total,
        'running': running,
        'sleeping': sleeping,
        'zombie': zombie
    }

    return summary, df_top


while True:
    resume = get_process_summary_and_top()[0]
    print(resume)
    print(get_process_summary_and_top()[1])
    sleep(3)