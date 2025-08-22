#!/usr/bin/env python3
"""
Debug script to test authentication logic
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import get_db
from app.auth import auth_manager, get_current_user, get_current_active_user
from app.models import User
from app.schemas import UserCreate

def test_auth_manager():
    """Test basic auth manager functionality"""
    print("🔍 Testing AuthManager...")
    
    # Test password hashing
    password = "testpass123"
    hashed = auth_manager.get_password_hash(password)
    print(f"✅ Password hashing: {len(hashed)} chars")
    
    # Test password verification
    is_valid = auth_manager.verify_password(password, hashed)
    print(f"✅ Password verification: {is_valid}")
    
    # Test invalid password
    is_invalid = auth_manager.verify_password("wrongpass", hashed)
    print(f"✅ Invalid password check: {not is_invalid}")
    
    # Test token creation
    token_data = {"sub": "testuser"}
    access_token = auth_manager.create_access_token(token_data)
    print(f"✅ Access token creation: {len(access_token)} chars")
    
    # Test token verification
    try:
        token_info = auth_manager.verify_token(access_token)
        print(f"✅ Token verification: {token_info.username}")
    except Exception as e:
        print(f"❌ Token verification failed: {e}")

def test_user_creation():
    """Test user creation and retrieval"""
    print("\n🔍 Testing User Creation...")
    
    # Get database session
    db = next(get_db())
    
    try:
        # Create test user
        user_data = UserCreate(
            username="debuguser",
            email="debug@example.com",
            password="debugpass123",
            full_name="Debug User"
        )
        
        # Check if user exists
        existing_user = db.query(User).filter(User.username == user_data.username).first()
        if existing_user:
            print(f"✅ User already exists: {existing_user.username}")
            user = existing_user
        else:
            # Create new user
            user = auth_manager.create_user(db, user_data)
            print(f"✅ User created: {user.username}")
        
        # Test user retrieval
        retrieved_user = db.query(User).filter(User.username == user.username).first()
        print(f"✅ User retrieval: {retrieved_user.username}")
        
        return user
        
    except Exception as e:
        print(f"❌ User creation failed: {e}")
        return None
    finally:
        db.close()

def test_authentication_flow():
    """Test complete authentication flow"""
    print("\n🔍 Testing Authentication Flow...")
    
    # Get database session
    db = next(get_db())
    
    try:
        # Test user login
        username = "debuguser"
        password = "debugpass123"
        
        user = auth_manager.authenticate_user(db, username, password)
        if user:
            print(f"✅ User authentication: {user.username}")
            
            # Create access token
            token_data = {"sub": user.username}
            access_token = auth_manager.create_access_token(token_data)
            print(f"✅ Access token created: {len(access_token)} chars")
            
            # Verify token
            token_info = auth_manager.verify_token(access_token)
            print(f"✅ Token verified: {token_info.username}")
            
            return access_token
        else:
            print("❌ User authentication failed")
            return None
            
    except Exception as e:
        print(f"❌ Authentication flow failed: {e}")
        return None
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Starting Authentication Debug Tests\n")
    
    try:
        # Test basic auth manager
        test_auth_manager()
        
        # Test user creation
        user = test_user_creation()
        
        # Test authentication flow
        if user:
            token = test_authentication_flow()
            if token:
                print(f"\n✅ All tests passed! Token: {token[:20]}...")
            else:
                print("\n❌ Authentication flow failed")
        else:
            print("\n❌ User creation failed")
            
    except Exception as e:
        print(f"\n❌ Test execution failed: {e}")
        import traceback
        traceback.print_exc()
