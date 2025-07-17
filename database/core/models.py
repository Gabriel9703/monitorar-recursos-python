from sqlalchemy import Column, Integer, String, DateTime, Float, BigInteger
from sqlalchemy.sql import func
from database.core.conexao import Base


class CPULog(Base):
    __tablename__ = 'cpu_logs'

    id = Column(Integer, primary_key=True, index=True)
    usage_percent = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class CPUCoreLog(Base):
    __tablename__ = 'cpu_core_logs'

    id = Column(Integer, primary_key=True, index=True)
    core_number = Column(Integer, nullable=False)
    usage_percent = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())


class RAMLog(Base):
    __tablename__ = 'ram_logs'

    id = Column(Integer, primary_key=True, index=True)
    percent = Column(Float, nullable=False)
    total = Column(BigInteger, nullable=False)
    used = Column(BigInteger, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class DiskLog(Base):
    __tablename__ = 'disk_logs'

    id = Column(Integer, primary_key=True, index=True)
    percent = Column(Float, nullable=False)
    total = Column(BigInteger, nullable=False)
    used = Column(BigInteger, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class SwapLog(Base):
    __tablename__ = 'swap_logs'

    id = Column(Integer, primary_key=True, index=True)
    percent = Column(Float, nullable=False)
    total = Column(BigInteger, nullable=False)
    used = Column(BigInteger, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class NetworkLog(Base):
    __tablename__ = 'network_logs'

    id = Column(Integer, primary_key=True, index=True)
    bytes_sent = Column(BigInteger, nullable=False)
    bytes_recv = Column(BigInteger, nullable=False)
    packets_sent = Column(BigInteger, nullable=False)
    packets_recv = Column(BigInteger, nullable=False)
    errors_sent = Column(Integer, nullable=False)
    errors_received = Column(Integer, nullable=False)
    drops_in = Column(Integer, nullable=False)
    drops_out = Column(Integer, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class ProcessLog(Base):
    __tablename__ = 'processes_log'

    id = Column(Integer, primary_key=True, index=True)
    pid = Column(Integer, nullable=False)
    name_proc = Column(String(50), nullable=False)
    username = Column(String(20), nullable=False)
    cpu_percent = Column(Float, nullable=False)
    memory_percent = Column(Float, nullable=False)
    status_proc = Column(String(20), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

