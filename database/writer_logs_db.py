from database.conexao import get_connection

def save_log_cpu(usage_percent):
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO cpu_logs (usage_percent) VALUES (%s)"
    cursor.execute(query, (usage_percent,))
    conn.commit()
    cursor.close()
    conn.close()


def save_log_cpu_core(core_number, usage):
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO cpu_core_logs (core_number, usage_percent) VALUES (%s, %s)"
    cursor.execute(query, (core_number, usage))
    conn.commit()
    cursor.close()
    conn.close()


def save_log_network(stats):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO network_logs (
            bytes_sent, bytes_recv, packets_sent, packets_recv,
            errors_sent, errors_received, drops_in, drops_out
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (
        stats["bytes_sent"],
        stats["bytes_recv"],
        stats["packets_sent"],
        stats["packets_recv"],
        stats["errors_sent"],
        stats["errors_recv"],
        stats["drops_in"],
        stats["drops_out"]
    ))
    conn.commit()
    cursor.close()
    conn.close()


def save_log_ram(total, used, percent):
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO ram_logs (total, used, percent) VALUES (%s, %s, %s)"
    cursor.execute(query, (total, used, percent))
    conn.commit()
    cursor.close()
    conn.close()


def save_log_swap(total, used, percent):
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO swap_logs (total, used, percent) VALUES (%s, %s, %s)"
    cursor.execute(query, (total, used, percent))
    conn.commit()
    cursor.close()
    conn.close()


def save_log_disk(total, used, percent):
    conn = get_connection()
    cursor = conn.cursor()  
    query = "INSERT INTO disk_logs (total, used, percent) VALUES (%s, %s, %s)"
    cursor.execute(query, (total, used, percent))
    conn.commit()
    cursor.close()
    conn.close()    


def save_log_process(pid, name_proc, username, cpu_percent, memory_percent, status_proc):
    conn = get_connection()
    cursor = conn.cursor()  
    query = "INSERT INTO processes_log (pid, name_proc, username, cpu_percent, memory_percent, status_proc) VALUES (%s, %s, %s, %s, %s, %s,)"
    cursor.execute(query, (pid, name_proc, username, cpu_percent, memory_percent, status_proc))
    conn.commit()
    cursor.close()
    conn.close()     


