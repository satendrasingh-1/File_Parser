#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    print("🔍 Testing imports...")
    
    try:
        from app.database import engine, get_db
        print("✅ Database imports successful")
    except Exception as e:
        print(f"❌ Database import failed: {e}")
        return False
    
    try:
        from app.models import Base, User, File
        print("✅ Models import successful")
    except Exception as e:
        print(f"❌ Models import failed: {e}")
        return False
    
    try:
        from app.auth import auth_manager, get_current_user, get_current_active_user
        print("✅ Auth import successful")
    except Exception as e:
        print(f"❌ Auth import failed: {e}")
        return False
    
    try:
        from app.crud import create_user, get_user, create_file
        print("✅ CRUD import successful")
    except Exception as e:
        print(f"❌ CRUD import failed: {e}")
        return False
    
    try:
        from app.utils import simulate_file_processing, parse_file_by_type
        print("✅ Utils import successful")
    except Exception as e:
        print(f"❌ Utils import failed: {e}")
        return False
    
    try:
        from app.websocket import manager
        print("✅ WebSocket import successful")
    except Exception as e:
        print(f"❌ WebSocket import failed: {e}")
        return False
    
    try:
        from app.schemas import UserCreate, FileBase, Token
        print("✅ Schemas import successful")
    except Exception as e:
        print(f"❌ Schemas import failed: {e}")
        return False
    
    return True

def test_database_operations():
    print("\n🔍 Testing database operations...")
    
    try:
        from app.database import engine, get_db
        from app.models import Base, User
        from app.schemas import UserCreate
        
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created")
        
        db = next(get_db())
        print("✅ Database session created")
        
        user_data = UserCreate(
            username="debuguser",
            email="debug@example.com",
            password="debugpass123",
            full_name="Debug User"
        )
        
        from app.auth import auth_manager
        user = auth_manager.create_user(db, user_data)
        print(f"✅ User created: {user.username}")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Database operations failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_app_creation():
    print("\n🔍 Testing FastAPI app creation...")
    
    try:
        from app.main import app
        print("✅ FastAPI app created successfully")
        print(f"✅ App title: {app.title}")
        print(f"✅ App version: {app.version}")
        print(f"✅ Routes count: {len(app.routes)}")
        return True
        
    except Exception as e:
        print(f"❌ FastAPI app creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Starting Server Debug Tests\n")
    
    try:
        if test_imports():
            if test_database_operations():
                if test_app_creation():
                    print("\n✅ All tests passed! Server should start successfully.")
                else:
                    print("\n❌ App creation failed")
            else:
                print("\n❌ Database operations failed")
        else:
            print("\n❌ Import tests failed")
            
    except Exception as e:
        print(f"\n❌ Test execution failed: {e}")
        import traceback
        traceback.print_exc()
