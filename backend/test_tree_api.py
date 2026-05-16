"""
Quick test script for GitHub tree fetcher API endpoints.

Usage:
    python test_tree_api.py
"""
import requests
import json


BASE_URL = "http://localhost:8000"


def print_separator(title=""):
    """Print a separator line."""
    if title:
        print(f"\n{'=' * 80}")
        print(f"{title:^80}")
        print('=' * 80)
    else:
        print('-' * 80)


def test_fetch_repo_tree_post():
    """Test POST /api/fetch-repo-tree endpoint."""
    print_separator("TEST 1: POST /api/fetch-repo-tree")
    
    url = f"{BASE_URL}/api/fetch-repo-tree"
    payload = {
        "url": "https://github.com/octocat/Hello-World",
        "branch": None,
        "max_depth": None,
        "include_filtered": False
    }
    
    print(f"\nRequest URL: {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ SUCCESS!")
            print(f"Owner: {data['owner']}")
            print(f"Repo: {data['repo']}")
            print(f"Branch: {data['branch']}")
            print(f"Total files: {data['total_files']}")
            print(f"Total directories: {data['total_directories']}")
            print(f"Filtered files: {data['filtered_files']}")
            print(f"Filtered directories: {data['filtered_directories']}")
            print(f"Truncated: {data['truncated']}")
            
            # Show important files
            print("\n📋 Important Files:")
            for level in ['critical', 'high', 'medium', 'low']:
                count = len(data['important_files'].get(level, []))
                if count > 0:
                    print(f"  {level.upper()}: {count} files")
                    for file in data['important_files'][level][:3]:
                        print(f"    - {file['path']}")
            
            # Show sample files
            print("\n📁 Sample Files (first 5):")
            for i, file in enumerate(data['files'][:5], 1):
                print(f"  {i}. {file['path']} ({file['size']} bytes) - {file['importance']}")
        else:
            print(f"\n❌ ERROR: {response.text}")
    
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to server. Is it running?")
        print("   Start server with: uvicorn app.main:app --reload")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")


def test_get_repo_tree():
    """Test GET /api/repo-tree/{owner}/{repo} endpoint."""
    print_separator("TEST 2: GET /api/repo-tree/{owner}/{repo}")
    
    url = f"{BASE_URL}/api/repo-tree/octocat/Hello-World"
    params = {
        "branch": None,
        "max_depth": 2,
        "include_filtered": False
    }
    
    print(f"\nRequest URL: {url}")
    print(f"Params: {json.dumps(params, indent=2)}")
    
    try:
        response = requests.get(url, params=params, timeout=30)
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ SUCCESS!")
            print(f"Owner: {data['owner']}")
            print(f"Repo: {data['repo']}")
            print(f"Branch: {data['branch']}")
            print(f"Total files: {data['total_files']}")
            print(f"Filtered files: {data['filtered_files']}")
            
            # Show directories
            print(f"\n📁 Directories ({len(data['directories'])}):")
            for directory in data['directories'][:5]:
                print(f"  - {directory['path']}/")
        else:
            print(f"\n❌ ERROR: {response.text}")
    
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to server. Is it running?")
        print("   Start server with: uvicorn app.main:app --reload")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")


def test_ml_project():
    """Test with an ML project repository."""
    print_separator("TEST 3: ML Project Analysis")
    
    url = f"{BASE_URL}/api/fetch-repo-tree"
    payload = {
        "url": "https://github.com/pytorch/examples",
        "branch": None,
        "max_depth": 3,
        "include_filtered": False
    }
    
    print(f"\nAnalyzing ML project: pytorch/examples")
    print(f"Max depth: 3 (for faster results)")
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ SUCCESS!")
            print(f"Total files: {data['total_files']}")
            print(f"Filtered files: {data['filtered_files']}")
            
            # Analyze important files
            print("\n🔍 ML/AI File Analysis:")
            critical = data['important_files'].get('critical', [])
            high = data['important_files'].get('high', [])
            medium = data['important_files'].get('medium', [])
            
            print(f"\n🔴 CRITICAL ({len(critical)} files):")
            for file in critical[:5]:
                print(f"  - {file['path']}")
            
            print(f"\n🟡 HIGH ({len(high)} files):")
            for file in high[:5]:
                print(f"  - {file['path']}")
            
            print(f"\n🟢 MEDIUM ({len(medium)} files):")
            for file in medium[:5]:
                print(f"  - {file['path']}")
        else:
            print(f"\n❌ ERROR: {response.text}")
    
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to server. Is it running?")
        print("   Start server with: uvicorn app.main:app --reload")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")


def test_error_handling():
    """Test error handling with invalid repository."""
    print_separator("TEST 4: Error Handling")
    
    url = f"{BASE_URL}/api/fetch-repo-tree"
    payload = {
        "url": "https://github.com/invalid-user/invalid-repo-12345",
        "branch": None,
        "max_depth": None,
        "include_filtered": False
    }
    
    print(f"\nTesting with invalid repository...")
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 404:
            print("\n✅ Correct error handling!")
            print(f"Error message: {response.json()['detail']}")
        else:
            print(f"\n⚠️  Unexpected status code: {response.status_code}")
            print(f"Response: {response.text}")
    
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to server. Is it running?")
        print("   Start server with: uvicorn app.main:app --reload")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")


def main():
    """Run all tests."""
    print("\n" + "=" * 80)
    print("GitHub Repository Tree Fetcher - API Tests")
    print("=" * 80)
    print("\nTesting FastAPI endpoints for tree fetching functionality.")
    print("Make sure the server is running: uvicorn app.main:app --reload")
    
    # Run tests
    test_fetch_repo_tree_post()
    test_get_repo_tree()
    test_ml_project()
    test_error_handling()
    
    print_separator("Tests Completed")
    print("\n✅ All tests completed!")
    print("\nFor more examples, run: python examples/fetch_github_tree.py")
    print("For documentation, see: backend/README_GITHUB_TREE.md")
    print()


if __name__ == "__main__":
    main()


# Made with Bob