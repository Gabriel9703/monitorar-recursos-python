def format_bytes(bytes):
    if bytes < 1024:
        return f"{bytes} bytes"
    elif bytes < 1024**2:
        return f"{bytes / 1024:.2f} KB"
    elif bytes < 1024**3:
        return f"{bytes / 1024**2:.2f} MB"
    else:
        return f"{bytes / 1024**3:.2f} GB"