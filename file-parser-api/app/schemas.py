from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List, Dict, Any

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: bool = True

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100)

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    token_type: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class FileBase(BaseModel):
    id: str
    filename: str
    original_filename: str
    file_type: str
    file_size: Optional[int] = None
    status: str
    progress: int
    error_message: Optional[str] = None
    file_metadata: Optional[str] = None
    processing_time: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    processed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class FileUploadResponse(BaseModel):
    file_id: str
    filename: str
    message: str

class FileProgress(BaseModel):
    file_id: str
    status: str
    progress: int
    error_message: Optional[str] = None

class FileContent(BaseModel):
    file_id: str
    filename: str
    status: str
    content: Optional[List[Dict[str, Any]]] = None
    file_metadata: Optional[Dict[str, Any]] = None
    message: Optional[str] = None
    error_message: Optional[str] = None
    processing_time: Optional[int] = None

class FileList(BaseModel):
    files: List[FileBase]
    total: int

class DeleteResponse(BaseModel):
    success: bool
    message: str

class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    timestamp: Optional[datetime] = None

class ErrorResponse(BaseModel):
    success: bool
    message: str
    error: Optional[str] = None

class WebSocketMessage(BaseModel):
    type: str
    data: Dict[str, Any]

class ProgressUpdate(BaseModel):
    status: str
    progress: int
    processing_time: Optional[int] = None

class StatusUpdate(BaseModel):
    status: str
    message: Optional[str] = None
    error_message: Optional[str] = None

class FileMetadata(BaseModel):
    file_type: str
    processing_time: int
    row_count: Optional[int] = None
    column_count: Optional[int] = None

class ProcessingOptions(BaseModel):
    include_headers: bool = True
    max_rows: Optional[int] = None
    skip_empty_rows: bool = True