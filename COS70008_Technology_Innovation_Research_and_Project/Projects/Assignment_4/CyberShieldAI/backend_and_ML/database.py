from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Database Configuration
DB_USER = 'root'
DB_PASSWORD = 'Ragav%40220899'
DB_HOST = 'localhost'
DB_PORT = '3306'
DB_NAME = 'malware_detection_db'

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False)
    email = Column(String(255), unique=True , nullable = False)
    password = Column(String(100), nullable=False)
    user_type = Column(String(10), default='regular')

class ScanHistory(Base):
    __tablename__ = 'scan_history'
    scan_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)

    result_1 = Column(String(20), default='--')
    malware_type_1 = Column(String(50), default='--')
    anomaly_score_1 = Column(String(10), default='--')
    accuracy_1 = Column(String(10), default='--')
    risk_1 = Column(String(10), default='--')

    result_2 = Column(String(20), default='--')
    malware_type_2 = Column(String(50), default='--')
    anomaly_score_2 = Column(String(10), default='--')
    accuracy_2 = Column(String(10), default='--')
    risk_2 = Column(String(10), default='--')

    result_3 = Column(String(20), default='--')
    malware_type_3 = Column(String(50), default='--')
    anomaly_score_3 = Column(String(10), default='--')
    accuracy_3 = Column(String(10), default='--')
    risk_3 = Column(String(10), default='--')

    historical_avg_error = Column(Float, default=0.0)
    scan_timestamp = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)
