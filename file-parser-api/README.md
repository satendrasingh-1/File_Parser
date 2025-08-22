# 🚀 File Parser CRUD API with Authentication & Production Features

A **production-ready** FastAPI-based file parsing service with JWT authentication, WebSocket real-time updates, multiple file format support, and comprehensive CRUD operations.

## ✨ **Production Features**

- **🔐 JWT Authentication**: Secure user management with access/refresh tokens
- **🔌 WebSocket Support**: Real-time progress updates and file status notifications
- **📁 Multiple File Formats**: CSV, Excel, PDF, and JSON file processing
- **👥 User Management**: User registration, login, and profile management
- **🛡️ Security**: Password hashing, token validation, and authorization
- **📊 Enhanced Tracking**: Processing time, metadata extraction, and statistics
- **🧪 Comprehensive Testing**: Unit tests and integration tests for all features
- **📝 Production Logging**: Structured logging with error handling
- **🚀 Scalable Architecture**: Background processing with async support

## 🏗️ **Enhanced Architecture**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Client App    │───▶│   FastAPI       │───▶│   SQLite DB     │
│                 │    │   Server        │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │
         ▼                       ▼
┌─────────────────┐    ┌─────────────────┐
│   WebSocket     │    │   Background    │
│   Real-time     │    │   Tasks        │
│   Updates       │    └─────────────────┘
└─────────────────┘
```

## 📋 **Requirements Checklist - Production Ready**

- [x] **JWT Authentication** - Complete user management system
- [x] **WebSocket Support** - Real-time progress updates
- [x] **Multiple File Formats** - CSV, Excel, PDF, JSON support
- [x] **Enhanced Security** - Password hashing, token validation
- [x] **User Management** - Registration, login, profiles, admin roles
- [x] **File Upload API** - Authenticated file uploads
- [x] **Progress Tracking** - Real-time WebSocket updates
- [x] **File Parsing** - Intelligent format detection and processing
- [x] **CRUD Operations** - Complete file lifecycle management
- [x] **File Retrieval** - Authenticated content access
- [x] **File Listing** - User-specific file management
- [x] **File Deletion** - Secure file removal
- [x] **Database Integration** - SQLite with user relationships
- [x] **Error Handling** - Comprehensive error responses
- [x] **Input Validation** - File type and size validation
- [x] **Background Processing** - Asynchronous file processing
- [x] **Progress Simulation** - Realistic progress updates
- [x] **Auto-cleanup** - Temporary file management
- [x] **API Documentation** - Interactive Swagger UI
- [x] **Health Check** - Enhanced API status endpoint
- [x] **Unit Tests** - Comprehensive test coverage
- [x] **Production Logging** - Structured logging system
- [x] **CORS Support** - Cross-origin resource sharing
- [x] **Rate Limiting Ready** - Infrastructure for throttling
- [x] **Environment Configuration** - Configurable settings

## 🚀 **Quick Start**

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd file-parser-api
   ```

2. **Create virtual environment**
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate
   
   # Linux/Mac
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables** (optional)
   ```bash
   # Windows
   set SECRET_KEY=your-super-secret-key-here
   set ACCESS_TOKEN_EXPIRE_MINUTES=30
   
   # Linux/Mac
   export SECRET_KEY=your-super-secret-key-here
   export ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. **Run the server**
   ```bash
   uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   ```

6. **Access the API**
   - **API Base URL**: `http://127.0.0.1:8000`
   - **Interactive Docs**: `http://127.0.0.1:8000/docs`
   - **Health Check**: `http://127.0.0.1:8000/`

## 📚 **Enhanced API Documentation**

### **Authentication Endpoints**

#### 1. **User Registration**
```http
POST /auth/register
Content-Type: application/json

{
  "username": "newuser",
  "email": "user@example.com",
  "full_name": "New User",
  "password": "securepassword123"
}
```

#### 2. **User Login**
```http
POST /auth/login
Content-Type: application/json

{
  "username": "newuser",
  "password": "securepassword123"
}
```

**Response**:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

#### 3. **Token Refresh**
```http
POST /auth/refresh
Content-Type: application/json

{
  "refresh_token": "your-refresh-token-here"
}
```

### **Protected File Endpoints**

**Note**: All file endpoints now require authentication. Include the access token in the Authorization header:

```http
Authorization: Bearer your-access-token-here
```

#### 4. **File Upload (Authenticated)**
```http
POST /files
Authorization: Bearer your-access-token-here
Content-Type: multipart/form-data

file: [your-file]
```

**Supported Formats**:
- CSV files (`.csv`, `.txt`)
- Excel files (`.xlsx`, `.xls`)
- PDF files (`.pdf`)
- JSON files (`.json`)

#### 5. **Progress Tracking (Authenticated)**
```http
GET /files/{file_id}/progress
Authorization: Bearer your-access-token-here
```

#### 6. **File Content (Authenticated)**
```http
GET /files/{file_id}
Authorization: Bearer your-access-token-here
```

#### 7. **List User Files (Authenticated)**
```http
GET /files?limit=10&offset=0&file_type=csv&status=ready
Authorization: Bearer your-access-token-here
```

#### 8. **Search Files (Authenticated)**
```http
GET /files/search?q=filename&limit=10&offset=0
Authorization: Bearer your-access-token-here
```

#### 9. **File Statistics (Authenticated)**
```http
GET /files/stats
Authorization: Bearer your-access-token-here
```

#### 10. **Delete File (Authenticated)**
```http
DELETE /files/{file_id}
Authorization: Bearer your-access-token-here
```

### **User Management Endpoints**

#### 11. **Get Current User Profile**
```http
GET /users/me
Authorization: Bearer your-access-token-here
```

#### 12. **List All Users (Admin Only)**
```http
GET /users?limit=100&offset=0
Authorization: Bearer admin-access-token-here
```

### **WebSocket Endpoint**

#### 13. **Real-time Progress Updates**
```javascript
// Connect to WebSocket for real-time updates
const ws = new WebSocket(`ws://127.0.0.1:8000/ws/${file_id}`);

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    
    if (data.type === 'progress_update') {
        console.log(`Progress: ${data.data.progress}%`);
        console.log(`Status: ${data.data.status}`);
    } else if (data.type === 'status_update') {
        console.log(`Status changed to: ${data.data.status}`);
    }
};

// Send ping to keep connection alive
setInterval(() => {
    ws.send(JSON.stringify({type: 'ping'}));
}, 30000);
```

## 📝 **Sample Requests & Responses**

### **cURL Examples with Authentication**

#### 1. **Register User**
```bash
curl -X POST "http://127.0.0.1:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "full_name": "Test User",
    "password": "testpass123"
  }'
```

#### 2. **Login and Get Token**
```bash
curl -X POST "http://127.0.0.1:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'
```

#### 3. **Upload File with Authentication**
```bash
curl -X POST "http://127.0.0.1:8000/files" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "file=@test.csv"
```

#### 4. **Check Progress with Authentication**
```bash
curl "http://127.0.0.1:8000/files/FILE_ID/progress" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### 5. **Get File Content with Authentication**
```bash
curl "http://127.0.0.1:8000/files/FILE_ID" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### **PowerShell Examples with Authentication**

#### 1. **Register User**
```powershell
$userData = @{
    username = "testuser"
    email = "test@example.com"
    full_name = "Test User"
    password = "testpass123"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/auth/register" -Method Post -Body $userData -ContentType "application/json"
```

#### 2. **Login and Get Token**
```powershell
$loginData = @{
    username = "testuser"
    password = "testpass123"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/auth/login" -Method Post -Body $loginData -ContentType "application/json"
$token = $response.access_token
```

#### 3. **Upload File with Authentication**
```powershell
$headers = @{
    Authorization = "Bearer $token"
}

$file = Get-Item "test.csv"
$form = @{file = $file}
Invoke-RestMethod -Uri "http://127.0.0.1:8000/files" -Method Post -Form $form -Headers $headers
```

## 🧪 **Enhanced Testing**

### **Automated Production Tests**

Run the comprehensive production test suite:

```bash
python test_production_api.py
```

This tests:
- ✅ JWT Authentication (registration, login, refresh)
- ✅ Protected endpoints
- ✅ Multiple file formats
- ✅ WebSocket connectivity
- ✅ User management
- ✅ File operations with authentication
- ✅ Error handling and security

### **Unit Tests**

Run unit tests for critical components:

```bash
# Install pytest
pip install pytest

# Run authentication tests
pytest tests/test_auth.py -v

# Run all tests
pytest tests/ -v
```

### **Manual Testing**

1. **Start the server**:
   ```bash
   uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   ```

2. **Open the interactive documentation**:
   - Navigate to `http://127.0.0.1:8000/docs`
   - Use the Swagger UI to test endpoints interactively
   - Test authentication flow first

3. **Test with sample files**:
   - Use the provided test files
   - Test different file formats
   - Verify WebSocket connections

## 📊 **Enhanced Postman Collection**

### **Import Instructions**

1. Open Postman
2. Click "Import" button
3. Copy and paste the collection JSON below
4. Set the base URL variable to `http://127.0.0.1:8000`
5. Create an environment with these variables:
   - `base_url`: `http://127.0.0.1:8000`
   - `access_token`: `your-access-token-here`
   - `refresh_token`: `your-refresh-token-here`

### **Collection JSON**

```json
{
  "info": {
    "name": "File Parser CRUD API with Authentication",
    "description": "Production-ready API collection with JWT auth, WebSocket, and multiple file formats",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
    "version": "2.0.0"
  },
  "variable": [
    {
      "key": "base_url",
      "value": "http://127.0.0.1:8000",
      "type": "string"
    },
    {
      "key": "access_token",
      "value": "your-access-token-here",
      "type": "string"
    },
    {
      "key": "refresh_token",
      "value": "your-refresh-token-here",
      "type": "string"
    }
  ],
  "item": [
    {
      "name": "Authentication",
      "item": [
        {
          "name": "Register User",
          "request": {
            "method": "POST",
            "header": [
              {
                "key": "Content-Type",
                "value": "application/json"
              }
            ],
            "body": {
              "mode": "raw",
              "raw": "{\n  \"username\": \"testuser\",\n  \"email\": \"test@example.com\",\n  \"full_name\": \"Test User\",\n  \"password\": \"testpass123\"\n}"
            },
            "url": {
              "raw": "{{base_url}}/auth/register",
              "host": ["{{base_url}}"],
              "path": ["auth", "register"]
            }
          }
        },
        {
          "name": "Login User",
          "request": {
            "method": "POST",
            "header": [
              {
                "key": "Content-Type",
                "value": "application/json"
              }
            ],
            "body": {
              "mode": "raw",
              "raw": "{\n  \"username\": \"testuser\",\n  \"password\": \"testpass123\"\n}"
            },
            "url": {
              "raw": "{{base_url}}/auth/login",
              "host": ["{{base_url}}"],
              "path": ["auth", "login"]
            }
          }
        },
        {
          "name": "Refresh Token",
          "request": {
            "method": "POST",
            "header": [
              {
                "key": "Content-Type",
                "value": "application/json"
              }
            ],
            "body": {
              "mode": "raw",
              "raw": "{\n  \"refresh_token\": \"{{refresh_token}}\"\n}"
            },
            "url": {
              "raw": "{{base_url}}/auth/refresh",
              "host": ["{{base_url}}"],
              "path": ["auth", "refresh"]
            }
          }
        }
      ]
    },
    {
      "name": "File Operations (Authenticated)",
      "item": [
        {
          "name": "Upload File",
          "request": {
            "method": "POST",
            "header": [
              {
                "key": "Authorization",
                "value": "Bearer {{access_token}}"
              }
            ],
            "body": {
              "mode": "formdata",
              "formdata": [
                {
                  "key": "file",
                  "type": "file",
                  "src": []
                }
              ]
            },
            "url": {
              "raw": "{{base_url}}/files",
              "host": ["{{base_url}}"],
              "path": ["files"]
            }
          }
        },
        {
          "name": "Get Progress",
          "request": {
            "method": "GET",
            "header": [
              {
                "key": "Authorization",
                "value": "Bearer {{access_token}}"
              }
            ],
            "url": {
              "raw": "{{base_url}}/files/{{file_id}}/progress",
              "host": ["{{base_url}}"],
              "path": ["files", "{{file_id}}", "progress"]
            }
          }
        },
        {
          "name": "Get File Content",
          "request": {
            "method": "GET",
            "header": [
              {
                "key": "Authorization",
                "value": "Bearer {{access_token}}"
              }
            ],
            "url": {
              "raw": "{{base_url}}/files/{{file_id}}",
              "host": ["{{base_url}}"],
              "path": ["files", "{{file_id}}"]
            }
          }
        },
        {
          "name": "List Files",
          "request": {
            "method": "GET",
            "header": [
              {
                "key": "Authorization",
                "value": "Bearer {{access_token}}"
              }
            ],
            "url": {
              "raw": "{{base_url}}/files?limit=10&offset=0",
              "host": ["{{base_url}}"],
              "path": ["files"],
              "query": [
                {
                  "key": "limit",
                  "value": "10"
                },
                {
                  "key": "offset",
                  "value": "0"
                }
              ]
            }
          }
        },
        {
          "name": "Search Files",
          "request": {
            "method": "GET",
            "header": [
              {
                "key": "Authorization",
                "value": "Bearer {{access_token}}"
              }
            ],
            "url": {
              "raw": "{{base_url}}/files/search?q=test&limit=10&offset=0",
              "host": ["{{base_url}}"],
              "path": ["files", "search"],
              "query": [
                {
                  "key": "q",
                  "value": "test"
                },
                {
                  "key": "limit",
                  "value": "10"
                },
                {
                  "key": "offset",
                  "value": "0"
                }
              ]
            }
          }
        },
        {
          "name": "Get File Statistics",
          "request": {
            "method": "GET",
            "header": [
              {
                "key": "Authorization",
                "value": "Bearer {{access_token}}"
              }
            ],
            "url": {
              "raw": "{{base_url}}/files/stats",
              "host": ["{{base_url}}"],
              "path": ["files", "stats"]
            }
          }
        },
        {
          "name": "Delete File",
          "request": {
            "method": "DELETE",
            "header": [
              {
                "key": "Authorization",
                "value": "Bearer {{access_token}}"
              }
            ],
            "url": {
              "raw": "{{base_url}}/files/{{file_id}}",
              "host": ["{{base_url}}"],
              "path": ["files", "{{file_id}}"]
            }
          }
        }
      ]
    },
    {
      "name": "User Management",
      "item": [
        {
          "name": "Get Current User Profile",
          "request": {
            "method": "GET",
            "header": [
              {
                "key": "Authorization",
                "value": "Bearer {{access_token}}"
              }
            ],
            "url": {
              "raw": "{{base_url}}/users/me",
              "host": ["{{base_url}}"],
              "path": ["users", "me"]
            }
          }
        }
      ]
    }
  ]
}
```

## 🔧 **Configuration**

### **Environment Variables**

```bash
# Security
SECRET_KEY=your-super-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Database
DATABASE_URL=sqlite:///./data/files.db

# Server
HOST=127.0.0.1
PORT=8000

# File Processing
MAX_FILE_SIZE=10485760  # 10MB
SUPPORTED_FORMATS=csv,xlsx,xls,pdf,json
```

### **Production Settings**

For production deployment, consider:

1. **Strong Secret Key**: Generate a cryptographically secure secret key
2. **Token Expiry**: Adjust token expiration times based on security requirements
3. **Database**: Use PostgreSQL or MySQL for production
4. **HTTPS**: Always use HTTPS in production
5. **Rate Limiting**: Implement rate limiting for production use
6. **Monitoring**: Add application monitoring and logging

## 🚀 **Production Deployment**

### **Using Gunicorn**

```bash
# Install production dependencies
pip install gunicorn uvicorn[standard]

# Run with Gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### **Docker Deployment**

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### **Environment Setup**

```bash
# Production environment
export SECRET_KEY="your-production-secret-key"
export ACCESS_TOKEN_EXPIRE_MINUTES="15"
export REFRESH_TOKEN_EXPIRE_DAYS="30"
export DATABASE_URL="postgresql://user:pass@localhost/dbname"
export HOST="0.0.0.0"
export PORT="8000"
```

## 🐛 **Troubleshooting**

### **Common Issues**

1. **Authentication Errors**:
   - Ensure you're including the `Authorization: Bearer <token>` header
   - Check if your access token has expired
   - Use the refresh token endpoint to get a new access token

2. **File Upload Issues**:
   - Verify file format is supported
   - Check file size limits
   - Ensure you're authenticated

3. **WebSocket Connection Issues**:
   - Check if the WebSocket endpoint is accessible
   - Verify the file_id in the WebSocket URL
   - Ensure proper WebSocket client implementation

4. **Database Issues**:
   - Check database file permissions
   - Verify SQLite installation
   - Check for database corruption

### **Debug Mode**

Enable debug logging:

```bash
uvicorn app.main:app --reload --log-level debug
```

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Ensure all tests pass
6. Submit a pull request

## 📄 **License**

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 **Support**

- **Issues**: Create an issue on GitHub
- **Documentation**: Check the interactive docs at `/docs`
- **Testing**: Use the provided test suites
- **Authentication**: Follow the JWT flow in the examples above

## 🔮 **Future Enhancements**

- [ ] Rate limiting and throttling
- [ ] File compression and archiving
- [ ] Advanced data validation rules
- [ ] Celery + Redis for distributed processing
- [ ] Kubernetes deployment manifests
- [ ] Monitoring and metrics dashboard
- [ ] API versioning system
- [ ] Multi-tenant support
- [ ] File encryption at rest
- [ ] Audit logging

---

**Happy Coding! 🚀**

This production-ready API provides enterprise-grade features with security, scalability, and comprehensive testing. Perfect for production deployments and real-world applications.
