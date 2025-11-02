#!/usr/bin/env python3
"""
Deployment Test Script
Verifies all components are working correctly
"""

import requests
import json
import time
import sys

def test_deployment(base_url="http://localhost:5005"):
    """Test the deployed application"""
    
    print("🧪 Testing Enhanced Writeup Automation AI Tool v2.0")
    print(f"📍 Testing URL: {base_url}")
    print("=" * 50)
    
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Homepage
    tests_total += 1
    try:
        response = requests.get(base_url, timeout=10)
        if response.status_code == 200:
            print("✅ Homepage loads successfully")
            tests_passed += 1
        else:
            print(f"❌ Homepage failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Homepage error: {e}")
    
    # Test 2: API Status
    tests_total += 1
    try:
        response = requests.get(f"{base_url}/api/status", timeout=10)
        if response.status_code == 200:
            print("✅ API status endpoint working")
            tests_passed += 1
        else:
            print(f"❌ API status failed: {response.status_code}")
    except Exception as e:
        print(f"❌ API status error: {e}")
    
    # Test 3: Sections endpoint
    tests_total += 1
    try:
        response = requests.get(f"{base_url}/api/sections", timeout=10)
        if response.status_code == 200:
            print("✅ Sections API working")
            tests_passed += 1
        else:
            print(f"❌ Sections API failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Sections API error: {e}")
    
    # Test 4: Chat endpoint
    tests_total += 1
    try:
        chat_data = {"message": "Hello, test message"}
        response = requests.post(
            f"{base_url}/api/chat/basic", 
            json=chat_data, 
            timeout=10
        )
        if response.status_code == 200:
            print("✅ Chat API working")
            tests_passed += 1
        else:
            print(f"❌ Chat API failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Chat API error: {e}")
    
    # Results
    print("=" * 50)
    print(f"📊 Test Results: {tests_passed}/{tests_total} passed")
    
    if tests_passed == tests_total:
        print("🎉 All tests passed! Deployment is successful!")
        return True
    else:
        print("⚠️  Some tests failed. Check the deployment.")
        return False

if __name__ == "__main__":
    # Test local deployment by default
    url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5005"
    success = test_deployment(url)
    sys.exit(0 if success else 1)