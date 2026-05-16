"""
Test script for the unified repository intelligence API endpoint.
Tests the orchestration of metadata, tree, and analysis services.
"""
import requests
import json
import sys


def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}\n")


def test_intelligence_endpoint():
    """Test the unified repository intelligence endpoint."""
    
    base_url = "http://localhost:8000"
    
    # Test repositories
    test_cases = [
        {
            "name": "Medical Imaging Repository (MONAI)",
            "url": "https://github.com/Project-MONAI/MONAI",
            "branch": None
        },
        {
            "name": "ML Framework (PyTorch - small sample)",
            "url": "https://github.com/pytorch/examples",
            "branch": None
        }
    ]
    
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║           Repository Intelligence API Endpoint Test                         ║
║                                                                              ║
║  Testing: POST /api/repository-intelligence                                 ║
║  Testing: GET  /api/repository-intelligence/{owner}/{repo}                  ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Test health endpoint first
    print_section("Testing Health Endpoint")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✓ Server is running")
            print(f"  Response: {response.json()}")
        else:
            print(f"✗ Health check failed: {response.status_code}")
            return
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to server. Make sure the server is running:")
        print("  cd backend && uvicorn app.main:app --reload")
        return
    
    # Test POST endpoint
    for test_case in test_cases:
        print_section(f"Testing POST: {test_case['name']}")
        
        payload = {
            "url": test_case["url"],
            "branch": test_case["branch"],
            "include_filtered": False,
            "max_depth": None
        }
        
        print(f"Request URL: {base_url}/api/repository-intelligence")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        
        try:
            response = requests.post(
                f"{base_url}/api/repository-intelligence",
                json=payload,
                timeout=60
            )
            
            print(f"\nStatus Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                
                print("\n✓ SUCCESS - Intelligence Retrieved")
                print(f"\n📊 Repository: {data['owner']}/{data['repo']}")
                print(f"   Branch: {data['branch']}")
                
                # Metadata
                metadata = data['metadata']
                print(f"\n📈 Metadata:")
                print(f"   Stars: {metadata['stars']:,}")
                print(f"   Language: {metadata['primary_language']}")
                print(f"   Description: {metadata['description'][:80]}...")
                
                # Classification
                classification = data['classification']
                print(f"\n🏷️  Classification:")
                print(f"   Primary Type: {classification['primary_type']}")
                print(f"   Confidence: {classification['confidence']}")
                
                # Technology
                technology = data['technology']
                print(f"\n🔧 Technology:")
                print(f"   Frameworks: {', '.join(technology['primary_frameworks'][:3])}")
                
                # Medical Context
                medical = data['medical_context']
                print(f"\n🏥 Medical AI:")
                print(f"   Is Medical: {medical['is_medical_ai']}")
                if medical['is_medical_ai']:
                    print(f"   Confidence: {medical['confidence']}")
                    print(f"   Modalities: {', '.join(medical['modalities'])}")
                
                # Workflow
                workflow = data['workflow']
                print(f"\n⚙️  Workflow:")
                print(f"   Training: {'✓' if workflow['has_training'] else '✗'}")
                print(f"   Inference: {'✓' if workflow['has_inference'] else '✗'}")
                
                # Statistics
                stats = data['statistics']
                print(f"\n📊 Statistics:")
                print(f"   Python Files: {stats['total_python_files']}")
                print(f"   Notebooks: {stats['total_notebook_files']}")
                
                # LLM Context
                llm = data['llm_context']
                print(f"\n🤖 LLM Context:")
                print(f"   Overview: {llm['repository_overview']}")
                print(f"   Entry Points: {', '.join(llm['suggested_entry_points'][:3])}")
                
                # Save option
                save = input("\n💾 Save full JSON response? (y/n): ").strip().lower()
                if save == 'y':
                    filename = f"intelligence_{data['owner']}_{data['repo']}.json"
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                    print(f"✓ Saved to {filename}")
                
            else:
                print(f"\n✗ FAILED")
                print(f"Response: {response.text}")
                
        except requests.exceptions.Timeout:
            print("\n✗ Request timed out (>60s)")
        except Exception as e:
            print(f"\n✗ Error: {str(e)}")
    
    # Test GET endpoint
    print_section("Testing GET Endpoint")
    
    owner = "pytorch"
    repo = "examples"
    
    print(f"Request URL: {base_url}/api/repository-intelligence/{owner}/{repo}")
    
    try:
        response = requests.get(
            f"{base_url}/api/repository-intelligence/{owner}/{repo}",
            params={"branch": None, "include_filtered": False},
            timeout=60
        )
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("\n✓ SUCCESS - GET endpoint works")
            print(f"   Repository: {data['owner']}/{data['repo']}")
            print(f"   Type: {data['classification']['primary_type']}")
            print(f"   Frameworks: {', '.join(data['technology']['primary_frameworks'][:3])}")
        else:
            print(f"\n✗ FAILED")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
    
    print_section("Test Summary")
    print("✓ All tests completed")
    print("\nEndpoints tested:")
    print("  - POST /api/repository-intelligence")
    print("  - GET  /api/repository-intelligence/{owner}/{repo}")


if __name__ == "__main__":
    test_intelligence_endpoint()
    print("\n✨ Testing completed!\n")

# Made with Bob