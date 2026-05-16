"""
Quick test script for repository analyzer API endpoints.
Tests the analyzer functionality with real GitHub repositories.
"""
import requests
import json

BASE_URL = "http://localhost:8000"


def test_analyze_repository():
    """Test POST /api/analyze-repository endpoint."""
    print("\n" + "="*80)
    print("Testing POST /api/analyze-repository")
    print("="*80)
    
    # Test with MONAI repository (medical imaging)
    url = f"{BASE_URL}/api/analyze-repository"
    payload = {
        "url": "https://github.com/Project-MONAI/MONAI",
        "branch": None
    }
    
    print(f"\nRequest: POST {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ SUCCESS!")
            print(f"\nRepository: {data['owner']}/{data['repo']}")
            print(f"Summary: {data['summary']}")
            
            print(f"\nRepository Types ({len(data['repository_types'])}):")
            for rt in data['repository_types'][:3]:
                print(f"  • {rt['type']} ({rt['confidence']} confidence)")
            
            print(f"\nFrameworks ({len(data['frameworks'])}):")
            for fw in data['frameworks'][:3]:
                print(f"  • {fw['framework']} ({fw['confidence']} confidence)")
            
            print(f"\nWorkflow Components ({len(data['workflow_components'])}):")
            for wc in data['workflow_components'][:3]:
                print(f"  • {wc['component']} ({wc['confidence']} confidence)")
            
            print(f"\nMedical Signals ({len(data['medical_signals'])}):")
            for ms in data['medical_signals'][:3]:
                print(f"  • {ms['signal']} ({ms['confidence']} confidence)")
            
            print(f"\nStatistics:")
            print(f"  Python files: {data['total_python_files']}")
            print(f"  Notebook files: {data['total_notebook_files']}")
            print(f"  Config files: {data['total_config_files']}")
            print(f"  Has requirements: {data['has_requirements']}")
            print(f"  Has Dockerfile: {data['has_dockerfile']}")
            print(f"  Has README: {data['has_readme']}")
            
        else:
            print(f"\n❌ FAILED!")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to server")
        print("Make sure the FastAPI server is running:")
        print("  cd backend")
        print("  uvicorn app.main:app --reload")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")


def test_analyze_repository_get():
    """Test GET /api/analyze-repository/{owner}/{repo} endpoint."""
    print("\n" + "="*80)
    print("Testing GET /api/analyze-repository/{owner}/{repo}")
    print("="*80)
    
    # Test with PyTorch repository
    owner = "pytorch"
    repo = "pytorch"
    url = f"{BASE_URL}/api/analyze-repository/{owner}/{repo}"
    
    print(f"\nRequest: GET {url}")
    
    try:
        response = requests.get(url, timeout=30)
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ SUCCESS!")
            print(f"\nRepository: {data['owner']}/{data['repo']}")
            print(f"Summary: {data['summary']}")
            
            print(f"\nRepository Types: {len(data['repository_types'])}")
            print(f"Frameworks: {len(data['frameworks'])}")
            print(f"Workflow Components: {len(data['workflow_components'])}")
            print(f"Medical Signals: {len(data['medical_signals'])}")
            
        else:
            print(f"\n❌ FAILED!")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to server")
        print("Make sure the FastAPI server is running:")
        print("  cd backend")
        print("  uvicorn app.main:app --reload")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")


def test_invalid_url():
    """Test with invalid GitHub URL."""
    print("\n" + "="*80)
    print("Testing with invalid URL (should return 400)")
    print("="*80)
    
    url = f"{BASE_URL}/api/analyze-repository"
    payload = {
        "url": "https://invalid-url.com/repo"
    }
    
    print(f"\nRequest: POST {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 400:
            print("\n✅ SUCCESS! (Correctly rejected invalid URL)")
            print(f"Error: {response.json()['detail']}")
        else:
            print(f"\n❌ UNEXPECTED STATUS CODE")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")


def main():
    """Run all tests."""
    print("\n" + "="*80)
    print("REPOSITORY ANALYZER API TESTS")
    print("="*80)
    print("\nMake sure the FastAPI server is running:")
    print("  cd backend")
    print("  uvicorn app.main:app --reload")
    print("\nPress Enter to continue or Ctrl+C to cancel...")
    
    try:
        input()
    except KeyboardInterrupt:
        print("\n\nCancelled.")
        return
    
    # Run tests
    test_analyze_repository()
    test_analyze_repository_get()
    test_invalid_url()
    
    print("\n" + "="*80)
    print("TESTS COMPLETED")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()

# Made with Bob
