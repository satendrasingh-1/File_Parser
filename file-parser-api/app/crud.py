from sqlalchemy.orm import Session
from sqlalchemy import desc, and_, or_
from . import models
from .schemas import UserCreate, UserUpdate
from typing import Optional, List, Dict, Any
import json

def create_user(db: Session, user_data: UserCreate) -> models.User:
    hashed_password = models.User.get_password_hash(user_data.password)
    db_user = models.User(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()

def update_user(db: Session, user_id: int, user_data: UserUpdate) -> Optional[models.User]:
    db_user = get_user(db, user_id)
    if db_user:
        for field, value in user_data.dict(exclude_unset=True).items():
            setattr(db_user, field, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int) -> bool:
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False

def list_users(db: Session, limit: int = 100, offset: int = 0) -> List[models.User]:
    return db.query(models.User).offset(offset).limit(limit).all()

def create_file(db: Session, file_data: dict) -> models.File:
    db_file = models.File(**file_data)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file

def get_file(db: Session, file_id: str) -> Optional[models.File]:
    return db.query(models.File).filter(models.File.id == file_id).first()

def get_file_by_owner(db: Session, file_id: str, owner_id: int) -> Optional[models.File]:
    return db.query(models.File).filter(
        and_(models.File.id == file_id, models.File.owner_id == owner_id)
    ).first()

def update_file_progress(db: Session, file_id: str, progress: int, status: str = None, processing_time: int = None) -> Optional[models.File]:
    db_file = get_file(db, file_id)
    if db_file:
        db_file.progress = progress
        if status:
            db_file.status = status
        if processing_time is not None:
            db_file.processing_time = processing_time
        db.commit()
        db.refresh(db_file)
    return db_file

def update_file_content(db: Session, file_id: str, content: str, file_metadata: str = None, 
                         status: str = "ready", processing_time: int = None) -> Optional[models.File]:
    db_file = get_file(db, file_id)
    if db_file:
        db_file.content = content
        db_file.status = status
        db_file.progress = 100
        if file_metadata:
            db_file.file_metadata = file_metadata
        if processing_time is not None:
            db_file.processing_time = processing_time
        db.commit()
        db.refresh(db_file)
    return db_file

def update_file_error(db: Session, file_id: str, error_message: str) -> Optional[models.File]:
    db_file = get_file(db, file_id)
    if db_file:
        db_file.status = "failed"
        db_file.error_message = error_message
        db.commit()
        db.refresh(db_file)
    return db_file

def list_files_by_owner(db: Session, owner_id: int, limit: int = 100, offset: int = 0) -> List[models.File]:
    return (
        db.query(models.File)
        .filter(models.File.owner_id == owner_id)
        .order_by(desc(models.File.created_at))
        .offset(offset)
        .limit(limit)
        .all()
    )

def delete_file(db: Session, file_id: str) -> bool:
    db_file = get_file(db, file_id)
    if db_file:
        db.delete(db_file)
        db.commit()
        return True
    return False

def search_files(db: Session, owner_id: int, query: str) -> List[models.File]:
    return (
        db.query(models.File)
        .filter(
            and_(
                models.File.owner_id == owner_id,
                or_(
                    models.File.original_filename.contains(query),
                    models.File.content.contains(query)
                )
            )
        )
        .order_by(desc(models.File.created_at))
        .all()
    )

def get_file_statistics(db: Session, owner_id: int) -> Dict[str, Any]:
    files = db.query(models.File).filter(models.File.owner_id == owner_id).all()
    
    total_files = len(files)
    file_types = {}
    status_counts = {}
    total_size = 0
    total_processing_time = 0
    
    for file in files:
        file_types[file.file_type] = file_types.get(file.file_type, 0) + 1
        status_counts[file.status] = status_counts.get(file.status, 0) + 1
        
        if file.file_size:
            total_size += file.file_size
        if file.processing_time:
            total_processing_time += file.processing_time
    
    return {
        "total_files": total_files,
        "file_types": file_types,
        "status_counts": status_counts,
        "total_size": total_size,
        "total_processing_time": total_processing_time,
        "average_processing_time": total_processing_time / total_files if total_files > 0 else 0
    }