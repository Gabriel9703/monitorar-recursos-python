from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from database.core import models


def get_db_entity(db: Session, model, entity_id: int):
    return db.query(model).filter(model.id == entity_id).first()

def get_all_db_entities(db: Session, model, skip: int = 0, limit: int = 100):
    return db.query(model).offset(skip).limit(limit).all()

# ========== CPU LOG CRUD ==========
def create_cpu_log(db: Session, usage_percent: float) -> models.CPULog:
    db_cpu = models.CPULog(usage_percent=usage_percent)
    db.add(db_cpu)
    db.commit()
    db.refresh(db_cpu)
    return db_cpu

def get_cpu_logs(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    time_range: Optional[timedelta] = None
) -> List[models.CPULog]:
    query = db.query(models.CPULog).order_by(models.CPULog.timestamp.desc())
    
    if time_range:
        min_time = datetime.now() - time_range
        query = query.filter(models.CPULog.timestamp >= min_time)
    
    return query.offset(skip).limit(limit).all()

def get_cpu_stats(db: Session, time_range: timedelta = timedelta(minutes=30)):
    min_time = datetime.now() - time_range
    stats = db.query(
        func.avg(models.CPULog.usage_percent).label('avg_usage'),
        func.max(models.CPULog.usage_percent).label('max_usage'),
        func.min(models.CPULog.usage_percent).label('min_usage')
    ).filter(models.CPULog.timestamp >= min_time).first()
    
    return {
        'avg_usage': stats.avg_usage,
        'max_usage': stats.max_usage,
        'min_usage': stats.min_usage
    }

# ========== CPU CORE LOG CRUD ==========
def create_cpu_core_log(db: Session, core_number: int, usage_percent: float) -> models.CPUCoreLog:
    db_core = models.CPUCoreLog(
        core_number=core_number,
        usage_percent=usage_percent
    )
    db.add(db_core)
    db.commit()
    db.refresh(db_core)
    return db_core

def get_cpu_core_logs(
    db: Session, 
    core_number: Optional[int] = None,
    skip: int = 0, 
    limit: int = 100
) -> List[models.CPUCoreLog]:
    query = db.query(models.CPUCoreLog).order_by(models.CPUCoreLog.timestamp.desc())
    
    if core_number is not None:
        query = query.filter(models.CPUCoreLog.core_number == core_number)
    
    return query.offset(skip).limit(limit).all()

# ========== RAM LOG CRUD ==========
def create_ram_log(db: Session, total: int, used: int, percent: float) -> models.RAMLog:
    db_ram = models.RAMLog(
        total=total,
        used=used,
        percent=percent
    )
    db.add(db_ram)
    db.commit()
    db.refresh(db_ram)
    return db_ram

def get_ram_logs(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    min_usage: Optional[float] = None
) -> List[models.RAMLog]:
    query = db.query(models.RAMLog).order_by(models.RAMLog.timestamp.desc())
    
    if min_usage:
        query = query.filter(models.RAMLog.percent >= min_usage)
    
    return query.offset(skip).limit(limit).all()

# ========== DISK LOG CRUD ==========
def create_disk_log(db: Session, total: int, used: int, percent: float) -> models.DiskLog:
    db_disk = models.DiskLog(
        total=total,
        used=used,
        percent=percent
    )
    db.add(db_disk)
    db.commit()
    db.refresh(db_disk)
    return db_disk

def get_disk_logs(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    critical_level: Optional[float] = None
) -> List[models.DiskLog]:
    query = db.query(models.DiskLog).order_by(models.DiskLog.timestamp.desc())
    
    if critical_level:
        query = query.filter(models.DiskLog.percent >= critical_level)
    
    return query.offset(skip).limit(limit).all()

# ========== SWAP LOG CRUD ==========
def create_swap_log(db: Session, total: int, used: int, percent: float) -> models.SwapLog:
    db_swap = models.SwapLog(
        total=total,
        used=used,
        percent=percent
    )
    db.add(db_swap)
    db.commit()
    db.refresh(db_swap)
    return db_swap

def get_swap_logs(
    db: Session, 
    skip: int = 0, 
    limit: int = 100
) -> List[models.SwapLog]:
    return db.query(models.SwapLog)\
             .order_by(models.SwapLog.timestamp.desc())\
             .offset(skip).limit(limit).all()

# ========== NETWORK LOG CRUD ==========
def create_network_log(
    db: Session,
    bytes_sent: int,
    bytes_recv: int,
    packets_sent: int,
    packets_recv: int,
    errors_sent: int,
    errors_received: int,
    drops_in: int,
    drops_out: int
) -> models.NetworkLog:
    db_network = models.NetworkLog(
        bytes_sent=bytes_sent,
        bytes_recv=bytes_recv,
        packets_sent=packets_sent,
        packets_recv=packets_recv,
        errors_sent=errors_sent,
        errors_received=errors_received,
        drops_in=drops_in,
        drops_out=drops_out
    )
    db.add(db_network)
    db.commit()
    db.refresh(db_network)
    return db_network

def get_network_logs(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    min_errors: Optional[int] = None
) -> List[models.NetworkLog]:
    query = db.query(models.NetworkLog).order_by(models.NetworkLog.timestamp.desc())
    
    if min_errors:
        query = query.filter(
            (models.NetworkLog.errors_sent >= min_errors) |
            (models.NetworkLog.errors_received >= min_errors)
        )
    
    return query.offset(skip).limit(limit).all()

# ========== PROCESS LOG CRUD ==========
def create_process_log(
    db: Session,
    pid: int,
    name_proc: str,
    username: str,
    cpu_percent: float,
    memory_percent: float,
    status_proc: str
) -> models.ProcessLog:
    db_process = models.ProcessLog(
        pid=pid,
        name_proc=name_proc,
        username=username,
        cpu_percent=cpu_percent,
        memory_percent=memory_percent,
        status_proc=status_proc
    )
    db.add(db_process)
    db.commit()
    db.refresh(db_process)
    return db_process

def get_process_logs(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    min_cpu: Optional[float] = None,
    min_memory: Optional[float] = None,
    status_filter: Optional[str] = None
) -> List[models.ProcessLog]:
    query = db.query(models.ProcessLog).order_by(models.ProcessLog.timestamp.desc())
    
    if min_cpu:
        query = query.filter(models.ProcessLog.cpu_percent >= min_cpu)
    
    if min_memory:
        query = query.filter(models.ProcessLog.memory_percent >= min_memory)
    
    if status_filter:
        query = query.filter(models.ProcessLog.status_proc == status_filter)
    
    return query.offset(skip).limit(limit).all()

def get_critical_processes(
    db: Session,
    cpu_threshold: float = 80.0,
    memory_threshold: float = 80.0,
    limit: int = 20
) -> List[models.ProcessLog]:
    return db.query(models.ProcessLog)\
             .filter(
                 (models.ProcessLog.cpu_percent >= cpu_threshold) |
                 (models.ProcessLog.memory_percent >= memory_threshold)
             )\
             .order_by(models.ProcessLog.timestamp.desc())\
             .limit(limit)\
             .all()