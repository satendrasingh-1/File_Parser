# 🚀 Quick Start Guide

Get your File Parser CRUD API running in **5 minutes**!

## ⚡ Super Quick Setup

### Option 1: Automated Setup (Recommended)
```bash
# Run the setup script
python setup.py
```

### Option 2: Manual Setup
```bash
# 1. Create virtual environment
python -m venv .venv

# 2. Activate it (Windows)
.venv\Scripts\activate
# OR (Linux/Mac)
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start server
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## 🧪 Test It Works

### 1. Health Check
```bash
curl http://127.0.0.1:8000/
```

### 2. Run Full Test Suite
```bash
python test_api.py
```

### 3. Interactive Testing
- Open: http://127.0.0.1:8000/docs
- Test endpoints directly in your browser

## 📱 Postman Collection

1. Import: `File_Parser_API.postman_collection.json`
2. Set base URL: `http://127.0.0.1:8000`
3. Start testing!

## 🎯 What You Get

- ✅ **File Upload**: POST `/files`
- ✅ **Progress Tracking**: GET `/files/{id}/progress`
- ✅ **Content Retrieval**: GET `/files/{id}`
- ✅ **File Management**: GET `/files`, DELETE `/files/{id}`
- ✅ **Real-time Processing**: Background CSV parsing
- ✅ **Database**: SQLite with automatic setup
- ✅ **API Docs**: Interactive Swagger UI

## 🚨 Common Issues

- **Port 8000 busy**: Change port with `--port 8001`
- **Import errors**: Activate virtual environment first
- **File upload fails**: Ensure CSV format is valid

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check out the [API endpoints](README.md#api-endpoints) section
- Explore [sample requests](README.md#sample-requests--responses)

---

**Need help?** Check the troubleshooting section in the main README or run `python test_api.py` to verify everything is working!
