"""
Unit tests for authentication system
Tests JWT token creation, validation, and user management
"""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.auth import AuthManager, get_current_user, get_current_active_user, require_admin
from app.models import User
from app.schemas import UserCreate, TokenData

@pytest.fixture
def mock_db():
    """Mock database session"""
    return Mock(spec=Session)

@pytest.fixture
def sample_user():
    """Sample user for testing"""
    return User(
        id=1,
        username="testuser",
        email="test@example.com",
        full_name="Test User",
        hashed_password="hashed_password",
        is_active=True,
        is_admin=False,
        created_at=datetime.utcnow()
    )

@pytest.fixture
def admin_user():
    """Admin user for testing"""
    return User(
        id=2,
        username="admin",
        email="admin@example.com",
        full_name="Admin User",
        hashed_password="hashed_password",
        is_active=True,
        is_admin=True,
        created_at=datetime.utcnow()
    )

class TestAuthManager:
    """Test cases for AuthManager class"""
    
    def test_verify_password(self):
        """Test password verification"""
        auth_manager = AuthManager()
        plain_password = "testpassword123"
        hashed_password = auth_manager.get_password_hash(plain_password)
        
        # Should verify correctly
        assert auth_manager.verify_password(plain_password, hashed_password) is True
        
        # Should fail with wrong password
        assert auth_manager.verify_password("wrongpassword", hashed_password) is False
    
    def test_get_password_hash(self):
        """Test password hashing"""
        auth_manager = AuthManager()
        password = "testpassword123"
        hashed = auth_manager.get_password_hash(password)
        
        # Should not be the same as plain text
        assert hashed != password
        # Should be a string
        assert isinstance(hashed, str)
        # Should be different each time (due to salt)
        hashed2 = auth_manager.get_password_hash(password)
        assert hashed != hashed2
    
    def test_create_access_token(self):
        """Test access token creation"""
        auth_manager = AuthManager()
        data = {"sub": "testuser"}
        token = auth_manager.create_access_token(data)
        
        # Should be a string
        assert isinstance(token, str)
        # Should be decodable
        decoded = auth_manager.verify_token(token)
        assert decoded.username == "testuser"
        assert decoded.token_type == "access"
    
    def test_create_refresh_token(self):
        """Test refresh token creation"""
        auth_manager = AuthManager()
        data = {"sub": "testuser"}
        token = auth_manager.create_refresh_token(data)
        
        # Should be a string
        assert isinstance(token, str)
        # Should be decodable
        decoded = auth_manager.verify_token(token)
        assert decoded.username == "testuser"
        assert decoded.token_type == "refresh"
    
    def test_verify_token_valid(self):
        """Test valid token verification"""
        auth_manager = AuthManager()
        data = {"sub": "testuser"}
        token = auth_manager.create_access_token(data)
        
        result = auth_manager.verify_token(token)
        assert result is not None
        assert result.username == "testuser"
        assert result.token_type == "access"
    
    def test_verify_token_invalid(self):
        """Test invalid token verification"""
        auth_manager = AuthManager()
        
        # Invalid token
        result = auth_manager.verify_token("invalid_token")
        assert result is None
    
    def test_verify_token_expired(self):
        """Test expired token verification"""
        auth_manager = AuthManager()
        data = {"sub": "testuser"}
        
        # Create token with very short expiry
        with patch('app.auth.ACCESS_TOKEN_EXPIRE_MINUTES', 0):
            token = auth_manager.create_access_token(data)
        
        # Wait a bit for token to expire
        import time
        time.sleep(0.1)
        
        # Should raise HTTPException for expired token
        with pytest.raises(HTTPException) as exc_info:
            auth_manager.verify_token(token)
        
        assert exc_info.value.status_code == 401
        assert "expired" in str(exc_info.value.detail)
    
    def test_authenticate_user_valid(self, mock_db, sample_user):
        """Test valid user authentication"""
        auth_manager = AuthManager()
        
        # Mock database query
        mock_db.query.return_value.filter.return_value.first.return_value = sample_user
        
        # Mock password verification
        with patch.object(auth_manager, 'verify_password', return_value=True):
            result = auth_manager.authenticate_user(mock_db, "testuser", "password")
        
        assert result == sample_user
    
    def test_authenticate_user_invalid_username(self, mock_db):
        """Test authentication with invalid username"""
        auth_manager = AuthManager()
        
        # Mock database query returning None
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        result = auth_manager.authenticate_user(mock_db, "nonexistent", "password")
        assert result is None
    
    def test_authenticate_user_invalid_password(self, mock_db, sample_user):
        """Test authentication with invalid password"""
        auth_manager = AuthManager()
        
        # Mock database query
        mock_db.query.return_value.filter.return_value.first.return_value = sample_user
        
        # Mock password verification failing
        with patch.object(auth_manager, 'verify_password', return_value=False):
            result = auth_manager.authenticate_user(mock_db, "testuser", "wrongpassword")
        
        assert result is None

class TestAuthDependencies:
    """Test cases for authentication dependencies"""
    
    @patch('app.auth.security')
    def test_get_current_user_valid(self, mock_security, mock_db, sample_user):
        """Test getting current user with valid token"""
        # Mock security dependency
        mock_credentials = Mock()
        mock_credentials.credentials = "valid_token"
        mock_security.return_value = mock_credentials
        
        # Mock token verification
        with patch('app.auth.auth_manager.verify_token') as mock_verify:
            mock_verify.return_value = TokenData(username="testuser", token_type="access")
            
            # Mock database query
            mock_db.query.return_value.filter.return_value.first.return_value = sample_user
            
            # Test dependency
            result = get_current_user(mock_credentials, mock_db)
            assert result == sample_user
    
    @patch('app.auth.security')
    def test_get_current_user_invalid_token(self, mock_security, mock_db):
        """Test getting current user with invalid token"""
        # Mock security dependency
        mock_credentials = Mock()
        mock_credentials.credentials = "invalid_token"
        mock_security.return_value = mock_credentials
        
        # Mock token verification failing
        with patch('app.auth.auth_manager.verify_token') as mock_verify:
            mock_verify.return_value = None
            
            # Should raise HTTPException
            with pytest.raises(HTTPException) as exc_info:
                get_current_user(mock_credentials, mock_db)
            
            assert exc_info.value.status_code == 401
    
    @patch('app.auth.security')
    def test_get_current_user_not_found(self, mock_security, mock_db):
        """Test getting current user when user not found in database"""
        # Mock security dependency
        mock_credentials = Mock()
        mock_credentials.credentials = "valid_token"
        mock_security.return_value = mock_credentials
        
        # Mock token verification
        with patch('app.auth.auth_manager.verify_token') as mock_verify:
            mock_verify.return_value = TokenData(username="testuser", token_type="access")
            
            # Mock database query returning None
            mock_db.query.return_value.filter.return_value.first.return_value = None
            
            # Should raise HTTPException
            with pytest.raises(HTTPException) as exc_info:
                get_current_user(mock_credentials, mock_db)
            
            assert exc_info.value.status_code == 401
    
    def test_get_current_active_user_active(self, sample_user):
        """Test getting current active user"""
        result = get_current_active_user(sample_user)
        assert result == sample_user
    
    def test_get_current_active_user_inactive(self):
        """Test getting current inactive user"""
        inactive_user = User(
            id=1,
            username="inactive",
            email="inactive@example.com",
            hashed_password="hash",
            is_active=False
        )
        
        # Should raise HTTPException
        with pytest.raises(HTTPException) as exc_info:
            get_current_active_user(inactive_user)
        
        assert exc_info.value.status_code == 400
        assert "inactive" in str(exc_info.value.detail)
    
    def test_require_admin_admin(self, admin_user):
        """Test admin requirement with admin user"""
        result = require_admin(admin_user)
        assert result == admin_user
    
    def test_require_admin_non_admin(self, sample_user):
        """Test admin requirement with non-admin user"""
        # Should raise HTTPException
        with pytest.raises(HTTPException) as exc_info:
            require_admin(sample_user)
        
        assert exc_info.value.status_code == 403
        assert "Admin privileges required" in str(exc_info.value.detail)

class TestUserCreation:
    """Test cases for user creation"""
    
    def test_create_user_success(self, mock_db):
        """Test successful user creation"""
        auth_manager = AuthManager()
        user_data = UserCreate(
            username="newuser",
            email="new@example.com",
            full_name="New User",
            password="password123"
        )
        
        # Mock password hashing
        with patch.object(auth_manager, 'get_password_hash', return_value="hashed_password"):
            # Mock database operations
            mock_db.add.return_value = None
            mock_db.commit.return_value = None
            mock_db.refresh.return_value = None
            
            result = auth_manager.create_user(mock_db, user_data)
            
            # Should create user with correct data
            assert result.username == "newuser"
            assert result.email == "new@example.com"
            assert result.full_name == "New User"
            assert result.hashed_password == "hashed_password"
            assert result.is_active is True
    
    def test_create_user_duplicate_username(self, mock_db):
        """Test user creation with duplicate username"""
        auth_manager = AuthManager()
        user_data = UserCreate(
            username="existinguser",
            email="new@example.com",
            password="password123"
        )
        
        # Mock existing user found
        existing_user = User(username="existinguser")
        mock_db.query.return_value.filter.return_value.first.return_value = existing_user
        
        # Should raise HTTPException
        with pytest.raises(HTTPException) as exc_info:
            auth_manager.create_user(mock_db, user_data)
        
        assert exc_info.value.status_code == 400
        assert "Username already registered" in str(exc_info.value.detail)
    
    def test_create_user_duplicate_email(self, mock_db):
        """Test user creation with duplicate email"""
        auth_manager = AuthManager()
        user_data = UserCreate(
            username="newuser",
            email="existing@example.com",
            password="password123"
        )
        
        # Mock no existing username but existing email
        mock_db.query.return_value.filter.return_value.first.side_effect = [None, User(email="existing@example.com")]
        
        # Should raise HTTPException
        with pytest.raises(HTTPException) as exc_info:
            auth_manager.create_user(mock_db, user_data)
        
        assert exc_info.value.status_code == 400
        assert "Email already registered" in str(exc_info.value.detail)
