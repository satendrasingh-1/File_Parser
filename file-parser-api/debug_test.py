#!/usr/bin/env python3
"""
Debug script to test file upload and identify issues
"""

import requests
import json

def test_file_upload():
    """Test file upload to identify the issue"""
    
    # 1. Login to get token
    print("🔐 Logging in...")
    login_response = requests.post(
        'http://127.0.0.1:8000/auth/login',
        json={'username': 'testuser', 'password': 'testpass123'}
    )
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        print(f"Response: {login_response.text}")
        return
    
    token = login_response.json()['access_token']
    print(f"✅ Login successful, token: {token[:20]}...")
    
    # 2. Test file upload
    print("\n📤 Testing file upload...")
    headers = {'Authorization': f'Bearer {token}'}
    
    try:
        with open('test.csv', 'rb') as f:
            files = {'file': ('test.csv', f, 'text/csv')}
            response = requests.post(
                'http://127.0.0.1:8000/files',
                files=files,
                headers=headers
            )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ File upload successful!")
        else:
            print("❌ File upload failed!")
            
    except Exception as e:
        print(f"❌ Error during file upload: {e}")

if __name__ == "__main__":
    test_file_upload()
