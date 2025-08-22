from fastapi import FastAPI, UploadFile, File, Depends, BackgroundTasks, HTTPException, Query, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import uuid
import shutil
import os
import json
import logging
from typing import List, Optional
from datetime import datetime

from . import models, database, crud, utils, auth
from .schemas import (
    FileUploadResponse, FileProgress, FileContent, 
    FileList, FileBase, DeleteResponse, UserCreate, UserResponse,
    Token, LoginRequest, RefreshTokenRequest, APIResponse, ErrorResponse
)
from .websocket import manager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="File Parser CRUD API with Authentication",
    description="A production-ready FastAPI application for parsing and managing files with JWT authentication, real-time updates, and multiple file format support",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_model=APIResponse)
async def root():
    return APIResponse(
        success=True,
        message="File Parser CRUD API with Authentication is running!",
        data={
            "version": "2.0.0",
            "docs": "/docs",
            "features": [
                "JWT Authentication",
                "Multiple File Formats (CSV, Excel, PDF, JSON)",
                "WebSocket Real-time Updates",
                "User Management",
                "File Processing with Progress Tracking"
            ]
        }
    )

@app.post("/auth/register", response_model=UserResponse)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        existing_user = crud.get_user_by_username(db, user.username)
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already registered")
        
        if user.email:
            existing_email = crud.get_user_by_email(db, user.email)
            if existing_email:
                raise HTTPException(status_code=400, detail="Email already registered")
        
        db_user = auth.auth_manager.create_user(db, user)
        logger.info(f"New user registered: {db_user.username}")
        return db_user
    except Exception as e:
        logger.error(f"User registration failed: {e}")
        raise HTTPException(status_code=500, detail="Registration failed")

@app.post("/auth/login", response_model=Token)
async def login_user(login_data: LoginRequest, db: Session = Depends(get_db)):
    try:
        user = auth.auth_manager.authenticate_user(db, login_data.username, login_data.password)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        access_token = auth.auth_manager.create_access_token(data={"sub": user.username})
        refresh_token = auth.auth_manager.create_refresh_token(data={"sub": user.username})
        
        logger.info(f"User logged in: {user.username}")
        return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")
    except Exception as e:
        logger.error(f"Login failed: {e}")
        raise HTTPException(status_code=500, detail="Login failed")

@app.post("/auth/refresh", response_model=Token)
async def refresh_token(refresh_data: RefreshTokenRequest, db: Session = Depends(get_db)):
    try:
        token_data = auth.auth_manager.verify_token(refresh_data.refresh_token)
        if not token_data or token_data.token_type != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        
        user = crud.get_user_by_username(db, token_data.username)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        access_token = auth.auth_manager.create_access_token(data={"sub": user.username})
        new_refresh_token = auth.auth_manager.create_refresh_token(data={"sub": user.username})
        
        logger.info(f"Token refreshed for user: {user.username}")
        return Token(access_token=access_token, refresh_token=new_refresh_token, token_type="bearer")
    except Exception as e:
        logger.error(f"Token refresh failed: {e}")
        raise HTTPException(status_code=500, detail="Token refresh failed")

@app.websocket("/ws/{file_id}")
async def websocket_endpoint(websocket: WebSocket, file_id: str):
    try:
        await manager.connect(websocket, file_id)
        logger.info(f"WebSocket connected for file: {file_id}")
        
        try:
            while True:
                data = await websocket.receive_text()
                await manager.send_personal_message(f"Message: {data}", websocket)
        except WebSocketDisconnect:
            manager.disconnect(websocket, file_id)
            logger.info(f"WebSocket disconnected for file: {file_id}")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket, file_id)

@app.post("/files", response_model=FileUploadResponse)
async def upload_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    try:
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        file_type = utils.get_file_type(file.filename)
        if not utils.validate_file_type(file_type):
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {file_type}")
        
        file_id = str(uuid.uuid4())
        file_path = f"uploads/{file_id}_{file.filename}"
        
        os.makedirs("uploads", exist_ok=True)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        file_data = {
            "id": file_id,
            "filename": f"{file_id}_{file.filename}",
            "original_filename": file.filename,
            "file_type": file_type,
            "file_size": os.path.getsize(file_path),
            "status": "uploading",
            "progress": 0,
            "owner_id": current_user.id
        }
        
        db_file = crud.create_file(db, file_data)
        
        background_tasks.add_task(
            utils.simulate_file_processing, db, file_id, file_path, file_type
        )
        
        logger.info(f"File uploaded: {file_id} by user: {current_user.username}")
        
        return FileUploadResponse(
            file_id=file_id,
            filename=file.filename,
            message="File uploaded successfully and processing started"
        )
        
    except Exception as e:
        logger.error(f"File upload failed: {e}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.get("/files/{file_id}/progress", response_model=FileProgress)
async def get_file_progress(
    file_id: str, 
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    try:
        db_file = crud.get_file_by_owner(db, file_id, current_user.id)
        if not db_file:
            raise HTTPException(status_code=404, detail="File not found")
        
        return FileProgress(
            file_id=file_id,
            status=db_file.status,
            progress=db_file.progress,
            error_message=db_file.error_message
        )
    except Exception as e:
        logger.error(f"Progress retrieval failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to get progress")

@app.get("/files/{file_id}", response_model=FileContent)
async def get_file_content(
    file_id: str, 
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    try:
        db_file = crud.get_file_by_owner(db, file_id, current_user.id)
        if not db_file:
            raise HTTPException(status_code=404, detail="File not found")
        
        if db_file.status != "ready":
            return FileContent(
                file_id=file_id,
                filename=db_file.original_filename,
                status=db_file.status,
                message="File is still being processed"
            )
        
        try:
            content = json.loads(db_file.content) if db_file.content else None
            file_metadata = json.loads(db_file.file_metadata) if db_file.file_metadata else None
        except json.JSONDecodeError:
            content = None
            file_metadata = None
        
        return FileContent(
            file_id=file_id,
            filename=db_file.original_filename,
            status=db_file.status,
            content=content,
            file_metadata=file_metadata,
            processing_time=db_file.processing_time
        )
    except Exception as e:
        logger.error(f"Content retrieval failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to get content")

@app.get("/files", response_model=FileList)
async def list_user_files(
    limit: int = Query(default=50, ge=1, le=100, description="Maximum number of files to return"),
    offset: int = Query(default=0, ge=0, description="Number of files to skip"),
    file_type: Optional[str] = Query(None, description="Filter by file type"),
    status: Optional[str] = Query(None, description="Filter by status"),
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    try:
        files = crud.list_files_by_owner(db, current_user.id, limit, offset)
        
        if file_type:
            files = [f for f in files if f.file_type == file_type]
        if status:
            files = [f for f in files if f.status == status]
        
        file_list = []
        for f in files:
            file_list.append(FileBase(
                id=f.id,
                filename=f.filename,
                original_filename=f.original_filename,
                file_type=f.file_type,
                file_size=f.file_size,
                status=f.status,
                progress=f.progress,
                error_message=f.error_message,
                file_metadata=f.file_metadata,
                processing_time=f.processing_time,
                created_at=f.created_at,
                updated_at=f.updated_at,
                processed_at=f.processed_at
            ))
        
        return FileList(files=file_list, total=len(file_list))
    except Exception as e:
        logger.error(f"File listing failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to list files")

@app.get("/files/search", response_model=FileList)
async def search_files(
    query: str = Query(..., description="Search query for filename or content"),
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    try:
        files = crud.search_files(db, current_user.id, query)
        
        file_list = []
        for f in files:
            file_list.append(FileBase(
                id=f.id,
                filename=f.filename,
                original_filename=f.original_filename,
                file_type=f.file_type,
                file_size=f.file_size,
                status=f.status,
                progress=f.progress,
                error_message=f.error_message,
                file_metadata=f.file_metadata,
                processing_time=f.processing_time,
                created_at=f.created_at,
                updated_at=f.updated_at,
                processed_at=f.processed_at
            ))
        
        return FileList(files=file_list, total=len(file_list))
    except Exception as e:
        logger.error(f"File search failed: {e}")
        raise HTTPException(status_code=500, detail="Search failed")

@app.get("/files/stats", response_model=dict)
async def get_file_statistics(
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    try:
        stats = crud.get_file_statistics(db, current_user.id)
        return stats
    except Exception as e:
        logger.error(f"Statistics retrieval failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to get statistics")

@app.delete("/files/{file_id}", response_model=DeleteResponse)
async def delete_file(
    file_id: str, 
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    try:
        db_file = crud.get_file_by_owner(db, file_id, current_user.id)
        if not db_file:
            raise HTTPException(status_code=404, detail="File not found")
        
        if db_file.filename and os.path.exists(f"uploads/{db_file.filename}"):
            os.remove(f"uploads/{db_file.filename}")
        
        crud.delete_file(db, file_id)
        
        logger.info(f"File deleted: {file_id} by user: {current_user.username}")
        
        return DeleteResponse(
            success=True,
            message=f"File {file_id} deleted successfully"
        )
    except Exception as e:
        logger.error(f"File deletion failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete file")

@app.get("/users/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: models.User = Depends(auth.get_current_active_user)
):
    return current_user

@app.get("/users", response_model=List[UserResponse])
async def list_users(
    current_user: models.User = Depends(auth.require_admin)
):
    try:
        from .database import SessionLocal
        db = SessionLocal()
        users = crud.list_users(db)
        db.close()
        return users
    except Exception as e:
        logger.error(f"User listing failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to list users")

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            success=False,
            message="Internal server error",
            error=str(exc)
        ).dict()
    )