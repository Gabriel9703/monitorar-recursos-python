CREATE TABLE IF NOT EXISTS cpu_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
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
