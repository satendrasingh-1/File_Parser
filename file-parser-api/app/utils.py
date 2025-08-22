import json
import os
import logging
from datetime import datetime
from sqlalchemy.orm import Session
from . import crud
from .websocket import manager
from typing import Dict, Any, Optional
import openpyxl
from PyPDF2 import PdfReader
import time
import asyncio
import threading

logger = logging.getLogger(__name__)

def parse_csv_file(file_path: str) -> Dict[str, Any]:
    try:
        import pandas as pd
        df = pd.read_csv(file_path)
        
        data = {
            "rows": df.to_dict('records'),
            "row_count": len(df),
            "column_count": len(df.columns),
            "columns": df.columns.tolist(),
            "data_types": df.dtypes.astype(str).to_dict()
        }
        
        return {"success": True, "data": data}
    except Exception as e:
        return {"success": False, "error": str(e)}

def parse_excel_file(file_path: str) -> Dict[str, Any]:
    try:
        import pandas as pd
        df = pd.read_excel(file_path)
        
        data = {
            "rows": df.to_dict('records'),
            "row_count": len(df),
            "column_count": len(df.columns),
            "columns": df.columns.tolist(),
            "data_types": df.dtypes.astype(str).to_dict()
        }
        
        return {"success": True, "data": data}
    except Exception as e:
        return {"success": False, "error": str(e)}

def parse_pdf_file(file_path: str) -> Dict[str, Any]:
    try:
        reader = PdfReader(file_path)
        text_content = ""
        
        for page in reader.pages:
            text_content += page.extract_text()
        
        data = {
            "text": text_content,
            "page_count": len(reader.pages),
            "word_count": len(text_content.split()),
            "character_count": len(text_content)
        }
        
        return {"success": True, "data": data}
    except Exception as e:
        return {"success": False, "error": str(e)}

def parse_json_file(file_path: str) -> Dict[str, Any]:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        if isinstance(json_data, list):
            data = {
                "type": "array",
                "items": json_data,
                "item_count": len(json_data)
            }
        elif isinstance(json_data, dict):
            data = {
                "type": "object",
                "keys": list(json_data.keys()),
                "key_count": len(json_data),
                "content": json_data
            }
        else:
            data = {
                "type": "primitive",
                "value": json_data
            }
        
        return {"success": True, "data": data}
    except Exception as e:
        return {"success": False, "error": str(e)}

def parse_file_by_type(file_path: str, file_type: str) -> Dict[str, Any]:
    if file_type == "csv":
        return parse_csv_file(file_path)
    elif file_type == "excel":
        return parse_excel_file(file_path)
    elif file_type == "pdf":
        return parse_pdf_file(file_path)
    elif file_type == "json":
        return parse_json_file(file_path)
    else:
        return {"success": False, "error": f"Unsupported file type: {file_type}"}

def validate_file_type(file_type: str) -> bool:
    supported_types = ["csv", "excel", "pdf", "json"]
    return file_type in supported_types

def get_file_type(filename: str) -> str:
    if not filename:
        return "unknown"
    
    extension = filename.lower().split('.')[-1]
    
    if extension in ['csv']:
        return "csv"
    elif extension in ['xlsx', 'xls']:
        return "excel"
    elif extension in ['pdf']:
        return "pdf"
    elif extension in ['json']:
        return "json"
    else:
        return "unknown"

def get_file_metadata(file_path: str, file_type: str) -> Dict[str, Any]:
    try:
        file_stat = os.stat(file_path)
        metadata = {
            "file_size": file_stat.st_size,
            "created_time": datetime.fromtimestamp(file_stat.st_ctime).isoformat(),
            "modified_time": datetime.fromtimestamp(file_stat.st_mtime).isoformat(),
            "file_type": file_type
        }
        return metadata
    except Exception as e:
        logger.error(f"Error getting file metadata: {e}")
        return {}

def simulate_file_processing(db: Session, file_id: str, file_path: str, file_type: str):
    start_time = time.time()
    
    def run_async_operations():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(manager.broadcast_file_status(file_id, {
                "status": "processing",
                "message": "File processing started"
            }))
            
            crud.update_file_progress(db, file_id, 0, "processing")
            
            progress_steps = [20, 40, 60, 80]
            for progress in progress_steps:
                time.sleep(1)
                crud.update_file_progress(db, file_id, progress, processing_time=int(time.time() - start_time))
                loop.run_until_complete(manager.broadcast_progress(file_id, {
                    "status": "processing",
                    "progress": progress,
                    "processing_time": int(time.time() - start_time)
                }))
            
            result = parse_file_by_type(file_path, file_type)
            
            if result["success"]:
                content_json = json.dumps(result["data"])
                file_metadata_json = json.dumps({
                    "file_type": file_type,
                    "processing_time": result["data"].get("processing_time", 0),
                    "row_count": result["data"].get("row_count", 0),
                    "column_count": result["data"].get("column_count", 0)
                })
                
                crud.update_file_content(
                    db, file_id, content_json, file_metadata_json, 
                    "ready", int(time.time() - start_time)
                )
                
                loop.run_until_complete(manager.broadcast_file_status(file_id, {
                    "status": "ready",
                    "message": "File processed successfully",
                    "processing_time": int(time.time() - start_time)
                }))
                
                logger.info(f"File {file_id} processed successfully in {time.time() - start_time:.2f}s")
            else:
                crud.update_file_error(db, file_id, f"Parsing failed: {result['error']}")
                loop.run_until_complete(manager.broadcast_file_status(file_id, {
                    "status": "failed",
                    "error_message": f"Parsing failed: {result['error']}"
                }))
                logger.error(f"File {file_id} processing failed: {result['error']}")
                
        except Exception as e:
            error_msg = f"Processing failed: {str(e)}"
            crud.update_file_error(db, file_id, error_msg)
            try:
                loop.run_until_complete(manager.broadcast_file_status(file_id, {
                    "status": "failed",
                    "error_message": error_msg
                }))
            except:
                pass
            logger.error(f"File {file_id} processing failed: {e}")
        finally:
            loop.close()
    
    thread = threading.Thread(target=run_async_operations)
    thread.start()
    thread.join()
    
    if os.path.exists(file_path):
        os.remove(file_path)
        logger.info(f"Temporary file {file_path} cleaned up")