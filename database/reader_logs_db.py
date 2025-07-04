from database.conexao import get_connection



def get_last_cpu_logs(limit=10):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM cpu_logs ORDER BY timestamp DESC LIMIT %s"
    cursor.execute(query, (limit,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result



def get_last_cpu_core_logs(limit=10):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM cpu_core_logs ORDER BY timestamp DESC LIMIT %s"
    cursor.execute(query, (limit,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result


def get_last_network_logs(limit=10):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM network_logs ORDER BY timestamp DESC LIMIT %s"
    cursor.execute(query, (limit,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result


def get_last_ram_logs(limit=10):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM ram_logs ORDER BY timestamp DESC LIMIT %s"
    cursor.execute(query, (limit,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result


def get_last_disk_logs(limit=10):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM disk_logs ORDER BY timestamp DESC LIMIT %s"
    cursor.execute(query, (limit,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result


def get_last_swap_logs(limit=10):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM swap_logs ORDER BY timestamp DESC LIMIT %s"
    cursor.execute(query, (limit,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result
