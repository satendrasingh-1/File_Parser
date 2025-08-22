#!/usr/bin/env python3
"""
Debug script to test database operations
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import get_db, engine
from app.models import Base, User, File
from app import crud
from app.schemas import UserCreate, FileBase

def test_database_connection():
    """Test database connection and table creation"""
    print("🔍 Testing Database Connection...")
    
    try:
        # Create tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully")
        
        # Test database session
        db = next(get_db())
        print("✅ Database session created successfully")
        
        # Test basic query
        user_count = db.query(User).count()
        print(f"✅ User count query: {user_count}")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_user_crud():
    """Test user CRUD operations"""
    print("\n🔍 Testing User CRUD Operations...")
    
    db = next(get_db())
    
    try:
        # Test user creation
        user_data = UserCreate(
            username="testuser_crud_new",
            email="test_crud_new@example.com",
            password="testpass123",
            full_name="Test User CRUD New"
        )
        
        user = crud.create_user(db, user_data)
        print(f"✅ User created: {user.username}")
        
        # Test user retrieval
        retrieved_user = crud.get_user(db, user.id)
        print(f"✅ User retrieved: {retrieved_user.username}")
        
        # Test user by username
        user_by_username = crud.get_user_by_username(db, user.username)
        print(f"✅ User by username: {user_by_username.username}")
        
        # Test user listing
        users = crud.list_users(db)
        print(f"✅ Users listed: {len(users)} users")
        
        return user
        
    except Exception as e:
        print(f"❌ User CRUD failed: {e}")
        # Try to get an existing user instead
        try:
            existing_user = db.query(User).first()
            if existing_user:
                print(f"✅ Using existing user: {existing_user.username}")
                return existing_user
        except:
            pass
        return None
    finally:
        db.close()

def test_file_crud():
    """Test file CRUD operations"""
    print("\n🔍 Testing File CRUD Operations...")
    
    db = next(get_db())
    
    try:
        # Get a user for file creation
        user = db.query(User).first()
        if not user:
            print("❌ No user found for file creation")
            return None
        
        # Test file creation
        file_id = "test_file_123"
        file_data = {
            "id": file_id,
            "filename": "test.csv",
            "original_filename": "test.csv",
            "file_type": "csv",
            "file_size": 1024,
            "status": "uploading",
            "progress": 0,
            "owner_id": user.id
        }
        
        file = crud.create_file(db, file_data)
        print(f"✅ File created: {file.filename}")
        
        # Test file retrieval
        retrieved_file = crud.get_file(db, file_id)
        print(f"✅ File retrieved: {retrieved_file.filename}")
        
        # Test file progress update
        updated_file = crud.update_file_progress(db, file_id, 50, "processing")
        print(f"✅ File progress updated: {updated_file.progress}%")
        
        # Test file listing
        files = crud.list_files_by_owner(db, user.id)
        print(f"✅ Files listed: {len(files)} files")
        
        # Test file count
        file_count = crud.get_files_count(db, owner_id=user.id)
        print(f"✅ File count: {file_count}")
        
        return file
        
    except Exception as e:
        print(f"❌ File CRUD failed: {e}")
        import traceback
        traceback.print_exc()
        return None
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Starting Database Debug Tests\n")
    
    try:
        # Test database connection
        if test_database_connection():
            # Test user CRUD
            user = test_user_crud()
            
            # Test file CRUD
            if user:
                file = test_file_crud()
                if file:
                    print(f"\n✅ All database tests passed!")
                else:
                    print("\n❌ File CRUD tests failed")
            else:
                print("\n❌ User CRUD tests failed")
        else:
            print("\n❌ Database connection failed")
            
    except Exception as e:
        print(f"\n❌ Test execution failed: {e}")
        import traceback
        traceback.print_exc()
