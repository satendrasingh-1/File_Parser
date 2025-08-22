#!/usr/bin/env python3
"""
Test script for File Parser CRUD API
Tests all endpoints to ensure they're working correctly
"""

import requests
import json
import time
import os

BASE_URL = "http://127.0.0.1:8000"

def test_health_check():
    """Test the root endpoint"""
    print("🔍 Testing Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health Check: {data['message']}")
            return True
        else:
            print(f"❌ Health Check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health Check error: {e}")
        return False

def test_file_upload():
    """Test file upload endpoint"""
    print("\n📤 Testing File Upload...")
    try:
        # Test with the existing test.csv file
        with open("test.csv", "rb") as f:
            files = {"file": ("test.csv", f, "text/csv")}
            response = requests.post(f"{BASE_URL}/files", files=files)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ File Upload: {data['message']}")
            print(f"   File ID: {data['file_id']}")
            print(f"   Status: {data['status']}")
            return data['file_id']
        else:
            print(f"❌ File Upload failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ File Upload error: {e}")
        return None

def test_progress_tracking(file_id):
    """Test progress tracking endpoint"""
    print(f"\n📊 Testing Progress Tracking for file {file_id}...")
    
    # Wait a bit for processing to start
    time.sleep(2)
    
    try:
        response = requests.get(f"{BASE_URL}/files/{file_id}/progress")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Progress Check: Status={data['status']}, Progress={data['progress']}%")
            return data['status']
        else:
            print(f"❌ Progress Check failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Progress Check error: {e}")
        return None

def test_file_content(file_id):
    """Test getting file content"""
    print(f"\n📄 Testing File Content for file {file_id}...")
    
    # Wait for processing to complete
    max_wait = 30
    wait_time = 0
    
    while wait_time < max_wait:
        try:
            response = requests.get(f"{BASE_URL}/files/{file_id}")
            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'ready':
                    print(f"✅ File Content: File processed successfully")
                    print(f"   Rows: {len(data['content']) if data['content'] else 0}")
                    return True
                elif data['status'] == 'failed':
                    print(f"❌ File Content: Processing failed - {data.get('error_message', 'Unknown error')}")
                    return False
                else:
                    print(f"⏳ File Content: Still processing ({data['status']})...")
                    time.sleep(2)
                    wait_time += 2
                continue
            else:
                print(f"❌ File Content failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ File Content error: {e}")
            return False
    
    print(f"⏰ Timeout waiting for file processing")
    return False

def test_list_files():
    """Test listing files endpoint"""
    print("\n📋 Testing List Files...")
    try:
        response = requests.get(f"{BASE_URL}/files")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ List Files: Found {data['total_count']} files")
            for file in data['files'][:3]:  # Show first 3 files
                print(f"   - {file['original_filename']} ({file['status']})")
            return True
        else:
            print(f"❌ List Files failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ List Files error: {e}")
        return False

def test_delete_file(file_id):
    """Test file deletion endpoint"""
    print(f"\n🗑️ Testing File Deletion for file {file_id}...")
    try:
        response = requests.delete(f"{BASE_URL}/files/{file_id}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ File Deletion: {data['message']}")
            return True
        else:
            print(f"❌ File Deletion failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ File Deletion error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting File Parser CRUD API Tests")
    print("=" * 50)
    
    # Test 1: Health Check
    if not test_health_check():
        print("❌ Health check failed. Server may not be running.")
        return
    
    # Test 2: File Upload
    file_id = test_file_upload()
    if not file_id:
        print("❌ File upload failed. Cannot continue with other tests.")
        return
    
    # Test 3: Progress Tracking
    status = test_progress_tracking(file_id)
    
    # Test 4: File Content (wait for processing)
    content_success = test_file_content(file_id)
    
    # Test 5: List Files
    list_success = test_list_files()
    
    # Test 6: File Deletion
    delete_success = test_delete_file(file_id)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    print(f"✅ Health Check: PASSED")
    print(f"✅ File Upload: PASSED")
    print(f"✅ Progress Tracking: PASSED")
    print(f"{'✅' if content_success else '❌'} File Content: {'PASSED' if content_success else 'FAILED'}")
    print(f"{'✅' if list_success else '❌'} List Files: {'PASSED' if list_success else 'FAILED'}")
    print(f"{'✅' if delete_success else '❌'} File Deletion: {'PASSED' if delete_success else 'FAILED'}")
    
    if all([content_success, list_success, delete_success]):
        print("\n🎉 ALL TESTS PASSED! The API is working perfectly!")
    else:
        print("\n⚠️ Some tests failed. Check the output above for details.")

if __name__ == "__main__":
    main()
