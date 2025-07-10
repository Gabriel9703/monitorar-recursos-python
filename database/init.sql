CREATE TABLE IF NOT EXISTS cpu_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usage_percent FLOAT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS cpu_core_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    core_number INT NOT NULL,
    usage_percent FLOAT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS ram_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    percent FLOAT NOT NULL,
    total BIGINT NOT NULL,
    used BIGINT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);



CREATE TABLE IF NOT EXISTS disk_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    percent FLOAT NOT NULL,
    total BIGINT NOT NULL,
    used BIGINT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS swap_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    percent FLOAT NOT NULL,
    total BIGINT NOT NULL,
    used BIGINT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS network_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bytes_sent BIGINT,
    bytes_recv BIGINT,
    packets_sent BIGINT,
    packets_recv BIGINT,
    errors_sent INT,
    errors_received INT,
    drops_in INT,
    drops_out INT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS processes_log(
    id INT AUTO_INCREMENT PRIMARY KEY,
    pid INT NOT NULL,
    name_proc VARCHAR(50) NOT NULL,
    username VARCHAR(20) NOT NULL,
    cpu_percent FLOAT NOT NULL,
    memory_percent FLOAT NOT NULL,
    status_proc VARCHAR(20) NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);