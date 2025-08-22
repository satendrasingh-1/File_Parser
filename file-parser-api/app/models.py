from sqlalchemy import Column, String, Integer, DateTime, Text, Boolean, ForeignKey, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    files = relationship("File", back_populates="owner", cascade="all, delete-orphan")

class File(Base):
    __tablename__ = "files"

    id = Column(String, primary_key=True, index=True)
    filename = Column(String, index=True, nullable=False)
    original_filename = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_size = Column(Integer, nullable=True)
    status = Column(String, default="uploading", nullable=False)
    progress = Column(Integer, default=0, nullable=False)
    content = Column(Text, nullable=True)
    error_message = Column(String, nullable=True)
    file_metadata = Column(Text, nullable=True)
    processing_time = Column(Integer, nullable=True)
    
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="files")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    processed_at = Column(DateTime(timezone=True), nullable=True)

Index("idx_files_owner_status", File.owner_id, File.status)
Index("idx_files_created_at", File.created_at)
Index("idx_files_file_type", File.file_type)
Index("idx_users_username", User.username)
Index("idx_users_email", User.email)