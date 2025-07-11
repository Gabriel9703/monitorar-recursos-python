import psutil as ps
from scripts.utils.logger import setup_logger

logger = setup_logger()


def check_suspicious_connectios():
    """ Verifica conexões suspeitas """
    suspicious = []

    for proc in ps.process_iter(['pid', 'name', 'net_connections']):
        try:
            connections = proc.info['net_connections']
            if connections:  # Se o processo tem conexões
                for conn in connections:
                    # Consideramos suspeito se for conexão remota e status não estabelecido
                    if conn.raddr and conn.status != 'ESTABLISHED':
                        info = {
                            'pid': proc.info['pid'],
                            'name': proc.info['name'],
                            'local_address': f"{conn.laddr.ip}:{conn.laddr.port}",
                            'remote_address': f"{conn.raddr.ip}:{conn.raddr.port}",
                            'status': conn.status
                        }
                        logger.warning(f"Conexão suspeita: {info}")
                        suspicious.append(info)
        except(ps.AccessDenied, ps.NoSuchProcess):
            continue

    return suspicious


def get_top_n_processes(n=5):
    processes = []
    for proc in ps.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            processes.append({
                'pid': proc.info['pid'],
                'name': proc.info['name'],
                'cpu': proc.info['cpu_percent'],
                'ram': proc.info['memory_percent']
            })
        except (ps.NoSuchProcess, ps.AccessDenied):
            continue
    processes.sort(key=lambda x: x['cpu'] + x['ram'], reverse=True)
    logger.info(f"Top {n} processos: {processes[:n]}")
    return processes[:n]    

if __name__ == "__main__":
    check_suspicious_connectios()
    get_top_n_processes()