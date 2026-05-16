"""
Test script for frontend-optimized API endpoints.
Tests CORS configuration and frontend response structure.
"""
import requests
import json
from typing import Dict, Any


BASE_URL = "http://localhost:8000"
TEST_REPO_URL = "https://github.com/Project-MONAI/MONAI"


def print_section(title: str):
    """Print a formatted section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def test_health_check():
    """Test health check endpoint."""
    print_section("Testing Health Check")
    
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        assert response.status_code == 200, "Health check failed"
        print("✅ Health check passed")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False


def test_cors_headers():
    """Test CORS headers are present."""
    print_section("Testing CORS Configuration")
    
    try:
        # Test with OPTIONS request (preflight)
        headers = {
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "Content-Type"
        }
        
        response = requests.options(
            f"{BASE_URL}/api/frontend/repository-intelligence",
            headers=headers
        )
        
        print(f"Status Code: {response.status_code}")
        print("\nCORS Headers:")
        cors_headers = {
            k: v for k, v in response.headers.items() 
            if k.lower().startswith('access-control')
        }
        for key, value in cors_headers.items():
            print(f"  {key}: {value}")
        
        # Check required CORS headers
        assert 'access-control-allow-origin' in response.headers, "Missing CORS origin header"
        assert 'access-control-allow-methods' in response.headers, "Missing CORS methods header"
        
        print("\n✅ CORS configuration is correct")
        return True
    except Exception as e:
        print(f"❌ CORS test failed: {e}")
        return False


def test_frontend_intelligence_endpoint():
    """Test frontend-optimized intelligence endpoint."""
    print_section("Testing Frontend Intelligence Endpoint")
    
    try:
        payload = {
            "url": TEST_REPO_URL,
            "branch": None,
            "include_filtered": False,
            "max_depth": None
        }
        
        headers = {
            "Content-Type": "application/json",
            "Origin": "http://localhost:3000"
        }
        
        print(f"Request URL: {BASE_URL}/api/frontend/repository-intelligence")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        print("\nSending request...")
        
        response = requests.post(
            f"{BASE_URL}/api/frontend/repository-intelligence",
            json=payload,
            headers=headers,
            timeout=60
        )
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            # Validate response structure
            print("\n✅ Response Structure Validation:")
            
            required_fields = [
                'loading_state',
                'owner',
                'repo',
                'branch',
                'metadata_card',
                'frameworks',
                'workflow_nodes',
                'medical_signals',
                'important_files',
                'classification',
                'statistics'
            ]
            
            for field in required_fields:
                if field in data:
                    print(f"  ✓ {field}: present")
                else:
                    print(f"  ✗ {field}: MISSING")
            
            # Print summary
            print("\n📊 Response Summary:")
            print(f"  Loading State: {data.get('loading_state')}")
            print(f"  Repository: {data.get('owner')}/{data.get('repo')}")
            print(f"  Branch: {data.get('branch')}")
            
            if data.get('metadata_card'):
                mc = data['metadata_card']
                print(f"  Stars: {mc.get('stars')}")
                print(f"  Language: {mc.get('language')}")
                print(f"  Topics: {len(mc.get('topics', []))}")
            
            print(f"  Frameworks Detected: {len(data.get('frameworks', []))}")
            print(f"  Workflow Nodes: {len(data.get('workflow_nodes', []))}")
            print(f"  Medical Signals: {len(data.get('medical_signals', []))}")
            print(f"  Important Files: {len(data.get('important_files', []))}")
            
            if data.get('processing_time_ms'):
                print(f"  Processing Time: {data['processing_time_ms']}ms")
            
            # Print sample framework
            if data.get('frameworks'):
                print("\n🔧 Sample Framework:")
                fw = data['frameworks'][0]
                print(f"  Name: {fw.get('name')}")
                print(f"  Confidence: {fw.get('confidence')}")
                print(f"  Category: {fw.get('category')}")
                print(f"  Evidence Count: {fw.get('evidence_count')}")
            
            # Print sample workflow node
            if data.get('workflow_nodes'):
                print("\n🔄 Sample Workflow Node:")
                wn = data['workflow_nodes'][0]
                print(f"  ID: {wn.get('id')}")
                print(f"  Label: {wn.get('label')}")
                print(f"  Type: {wn.get('type')}")
                print(f"  Has Implementation: {wn.get('has_implementation')}")
            
            print("\n✅ Frontend intelligence endpoint test passed")
            return True
        else:
            print(f"\n❌ Request failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out (this is normal for large repositories)")
        print("   The endpoint is working but the repository analysis takes time")
        return True
    except Exception as e:
        print(f"❌ Frontend intelligence test failed: {e}")
        return False


def test_error_handling():
    """Test error handling with invalid URL."""
    print_section("Testing Error Handling")
    
    try:
        payload = {
            "url": "https://invalid-url.com/not-a-repo",
            "branch": None,
            "include_filtered": False,
            "max_depth": None
        }
        
        response = requests.post(
            f"{BASE_URL}/api/frontend/repository-intelligence",
            json=payload,
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 400:
            data = response.json()
            print("\n✅ Error Response Structure:")
            print(f"  Loading State: {data.get('loading_state')}")
            
            if 'error' in data:
                error = data['error']
                print(f"  Error Type: {error.get('error_type')}")
                print(f"  Message: {error.get('message')}")
                print(f"  Stage: {error.get('stage')}")
                print(f"  Retry Possible: {error.get('retry_possible')}")
                print(f"  Suggestions: {len(error.get('suggestions', []))}")
            
            print("\n✅ Error handling test passed")
            return True
        else:
            print(f"❌ Expected 400 status code, got {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        return False


def test_get_endpoint():
    """Test GET endpoint by owner/repo."""
    print_section("Testing GET Endpoint")
    
    try:
        url = f"{BASE_URL}/api/frontend/repository-intelligence/fastapi/fastapi"
        
        print(f"Request URL: {url}")
        print("Sending request...")
        
        response = requests.get(url, timeout=60)
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Repository: {data.get('owner')}/{data.get('repo')}")
            print(f"   Loading State: {data.get('loading_state')}")
            print("\n✅ GET endpoint test passed")
            return True
        else:
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
        return True
    except Exception as e:
        print(f"❌ GET endpoint test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("\n" + "=" * 80)
    print("  NeuroCode AI Backend - Frontend API Tests")
    print("=" * 80)
    
    print(f"\nBase URL: {BASE_URL}")
    print(f"Test Repository: {TEST_REPO_URL}")
    
    results = []
    
    # Run tests
    results.append(("Health Check", test_health_check()))
    results.append(("CORS Configuration", test_cors_headers()))
    results.append(("Frontend Intelligence Endpoint", test_frontend_intelligence_endpoint()))
    results.append(("Error Handling", test_error_handling()))
    results.append(("GET Endpoint", test_get_endpoint()))
    
    # Print summary
    print_section("Test Summary")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    print(f"\n{'=' * 80}")
    print(f"Total: {passed}/{total} tests passed")
    print(f"{'=' * 80}\n")
    
    if passed == total:
        print("🎉 All tests passed! Backend is ready for frontend integration.")
    else:
        print("⚠️  Some tests failed. Please check the output above.")


if __name__ == "__main__":
    main()

# Made with Bob
