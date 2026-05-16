"""
Quick test script to verify GitHub metadata API endpoints.
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_parse_url():
    """Test URL parsing endpoint."""
    print("\n" + "="*60)
    print("Test 1: Parse GitHub URL")
    print("="*60)
    
    url = f"{BASE_URL}/api/parse-github-url"
    data = {"url": "https://github.com/fastapi/fastapi"}
    
    try:
        response = requests.post(url, json=data, timeout=5)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_fetch_metadata():
    """Test metadata fetching endpoint."""
    print("\n" + "="*60)
    print("Test 2: Fetch Repository Metadata")
    print("="*60)
    
    url = f"{BASE_URL}/api/fetch-repo-metadata"
    data = {"url": "https://github.com/octocat/Hello-World"}
    
    try:
        response = requests.post(url, json=data, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            metadata = response.json()
            print(f"\nRepository: {metadata['full_name']}")
            print(f"Stars: {metadata['stars']}")
            print(f"Language: {metadata['primary_language']}")
            print(f"Topics: {metadata['topics']}")
            print(f"Description: {metadata['description']}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_get_metadata():
    """Test GET metadata endpoint."""
    print("\n" + "="*60)
    print("Test 3: GET Repository Metadata")
    print("="*60)
    
    url = f"{BASE_URL}/api/repo-metadata/fastapi/fastapi"
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            metadata = response.json()
            print(f"\nRepository: {metadata['full_name']}")
            print(f"Stars: {metadata['stars']}")
            print(f"Language: {metadata['primary_language']}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_rate_limit():
    """Test rate limit endpoint."""
    print("\n" + "="*60)
    print("Test 4: Check Rate Limit")
    print("="*60)
    
    url = f"{BASE_URL}/api/rate-limit"
    
    try:
        response = requests.get(url, timeout=5)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_health():
    """Test health endpoint."""
    print("\n" + "="*60)
    print("Test 0: Health Check")
    print("="*60)
    
    url = f"{BASE_URL}/"
    
    try:
        response = requests.get(url, timeout=5)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("GitHub Metadata API - Test Suite")
    print("="*60)
    print("\nMake sure the server is running on http://localhost:8000")
    print("Waiting 2 seconds for server to be ready...")
    time.sleep(2)
    
    results = []
    
    # Run tests
    results.append(("Health Check", test_health()))
    results.append(("Parse URL", test_parse_url()))
    results.append(("Fetch Metadata (POST)", test_fetch_metadata()))
    results.append(("Get Metadata (GET)", test_get_metadata()))
    results.append(("Rate Limit", test_rate_limit()))
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
    
    print("="*60 + "\n")


if __name__ == "__main__":
    main()

# Made with Bob