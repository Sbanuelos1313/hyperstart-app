from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Float, Text, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./hyperstart.db")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ── MODELS ──

class User(Base):
    __tablename__ = "hs_users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="student")  # student, admin, teacher
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    # Profile
    full_name = Column(String)
    grade = Column(Integer)
    school = Column(String)
    zip_code = Column(String)
    race_ethnicity = Column(String)
    gender = Column(String)
    # Progress
    xp = Column(Integer, default=0)
    cluster = Column(String)
    # Relations
    progress = relationship("StudentProgress", back_populates="user", uselist=False)
    sessions = relationship("SessionLog", back_populates="user")

class StudentProgress(Base):
    __tablename__ = "hs_progress"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("hs_users.id"), unique=True)
    # Pre/Post Assessment
    pre_conf = Column(Integer, default=0)
    pre_aware = Column(Integer, default=0)
    pre_money = Column(Integer, default=0)
    pre_why = Column(Integer, default=0)
    post_conf = Column(Integer, default=0)
    post_aware = Column(Integer, default=0)
    post_money = Column(Integer, default=0)
    post_why = Column(Integer, default=0)
    pre_done = Column(Boolean, default=False)
    post_done = Column(Boolean, default=False)
    # Module completion
    career_sparks_done = Column(Boolean, default=False)
    career_sparks_cluster = Column(String)
    money_mod = Column(Integer, default=0)
    think_q = Column(Integer, default=0)
    story_done = Column(Boolean, default=False)
    ai_mod = Column(Integer, default=0)
    eng_done = Column(Boolean, default=False)
    # Reflections stored as JSON
    reflections = Column(JSON, default={})
    # Timestamps
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user = relationship("User", back_populates="progress")

class SessionLog(Base):
    __tablename__ = "hs_sessions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("hs_users.id"))
    school = Column(String)
    zip_code = Column(String)
    action = Column(String)
    module = Column(String)
    xp_earned = Column(Integer, default=0)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="sessions")

class Program(Base):
    __tablename__ = "hs_programs"
    id = Column(Integer, primary_key=True)
    name = Column(String)  # e.g. "OKC Innovation District 2026-27"
    schools = Column(JSON, default=[])
    zip_codes = Column(JSON, default=[])
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    grant_amount = Column(Float)
    is_active = Column(Boolean, default=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
