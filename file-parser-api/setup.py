#!/usr/bin/env python3
"""
Setup script for File Parser CRUD API
Automates the installation and setup process
"""

import os
import sys
import subprocess
import platform

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"   Output: {e.stdout}")
        if e.stderr:
            print(f"   Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    print("🔍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required, found {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def create_virtual_environment():
    """Create and activate virtual environment"""
    print("🔧 Setting up virtual environment...")
    
    # Check if virtual environment already exists
    if os.path.exists(".venv"):
        print("✅ Virtual environment already exists")
        return True
    
    # Create virtual environment
    if not run_command("python -m venv .venv", "Creating virtual environment"):
        return False
    
    print("✅ Virtual environment created successfully")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    
    # Determine activation command based on OS
    if platform.system() == "Windows":
        activate_cmd = ".venv\\Scripts\\activate"
        pip_cmd = ".venv\\Scripts\\pip"
    else:
        activate_cmd = "source .venv/bin/activate"
        pip_cmd = ".venv/bin/pip"
    
    # Install dependencies
    if not run_command(f"{pip_cmd} install -r requirements.txt", "Installing dependencies"):
        return False
    
    print("✅ Dependencies installed successfully")
    return True

def create_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    
    directories = ["data", "uploads"]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}")
        else:
            print(f"✅ Directory already exists: {directory}")
    
    return True

def test_installation():
    """Test if the installation is working"""
    print("🧪 Testing installation...")
    
    try:
        # Test import
        import app.main
        print("✅ Application imports successfully")
        
        # Test database connection
        from app.database import engine
        from app.models import Base
        Base.metadata.create_all(bind=engine)
        print("✅ Database connection successful")
        
        return True
    except Exception as e:
        print(f"❌ Installation test failed: {e}")
        return False

def print_next_steps():
    """Print next steps for the user"""
    print("\n" + "="*60)
    print("🎉 SETUP COMPLETED SUCCESSFULLY!")
    print("="*60)
    print("\n📋 Next Steps:")
    print("1. Activate virtual environment:")
    if platform.system() == "Windows":
        print("   .venv\\Scripts\\activate")
    else:
        print("   source .venv/bin/activate")
    
    print("\n2. Start the server:")
    print("   uvicorn app.main:app --reload --host 127.0.0.1 --port 8000")
    
    print("\n3. Access the API:")
    print("   - API Base URL: http://127.0.0.1:8000")
    print("   - Interactive Docs: http://127.0.0.1:8000/docs")
    print("   - Health Check: http://127.0.0.1:8000/")
    
    print("\n4. Test the API:")
    print("   python test_api.py")
    
    print("\n5. Import Postman collection:")
    print("   File: File_Parser_API.postman_collection.json")
    
    print("\n📚 Documentation:")
    print("   - README.md: Complete setup and usage guide")
    print("   - Interactive API docs: http://127.0.0.1:8000/docs")
    
    print("\n🚀 Happy coding!")

def main():
    """Main setup function"""
    print("🚀 File Parser CRUD API Setup")
    print("="*40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment
    if not create_virtual_environment():
        print("❌ Failed to create virtual environment")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Create directories
    if not create_directories():
        print("❌ Failed to create directories")
        sys.exit(1)
    
    # Test installation
    if not test_installation():
        print("❌ Installation test failed")
        sys.exit(1)
    
    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    main()
