"""
Example script demonstrating repository structure analysis.
Analyzes a GitHub repository and generates intelligence report.
"""
import asyncio
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.utils.github_parser import parse_github_url
from app.services.github_tree_service import get_github_tree_service
from app.services.repository_analyzer import get_repository_analyzer


async def analyze_repository(url: str, branch: str = None):
    """
    Analyze a GitHub repository and print intelligence report.
    
    Args:
        url: GitHub repository URL
        branch: Optional branch name
    """
    print(f"\n{'='*80}")
    print(f"ANALYZING REPOSITORY: {url}")
    print(f"{'='*80}\n")
    
    try:
        # Parse URL
        print("📋 Parsing GitHub URL...")
        owner, repo = parse_github_url(url)
        print(f"   Owner: {owner}")
        print(f"   Repo: {repo}\n")
        
        # Fetch repository tree
        print("🌳 Fetching repository tree structure...")
        tree_service = get_github_tree_service()
        tree = tree_service.fetch_repository_tree(
            owner=owner,
            repo=repo,
            branch=branch,
            max_depth=None,
            include_filtered=False
        )
        print(f"   Total files: {tree.total_files}")
        print(f"   Total directories: {tree.total_directories}")
        print(f"   Filtered files: {tree.filtered_files}")
        print(f"   Filtered directories: {tree.filtered_directories}\n")
        
        # Analyze repository
        print("🔍 Analyzing repository structure...")
        analyzer = get_repository_analyzer()
        intelligence = analyzer.analyze(tree)
        
        # Print results
        print(f"\n{'='*80}")
        print("ANALYSIS RESULTS")
        print(f"{'='*80}\n")
        
        # Summary
        print(f"📊 SUMMARY")
        print(f"   {intelligence.summary}\n")
        
        # Repository Types
        if intelligence.repository_types:
            print(f"🏷️  REPOSITORY TYPES")
            for rt in intelligence.repository_types:
                print(f"   • {rt.type.value.replace('_', ' ').title()} ({rt.confidence.value} confidence)")
                if rt.evidence:
                    print(f"     Evidence: {', '.join(rt.evidence[:3])}")
            print()
        
        # Frameworks
        if intelligence.frameworks:
            print(f"🔧 FRAMEWORKS DETECTED")
            for fw in intelligence.frameworks:
                print(f"   • {fw.framework.value.replace('_', ' ').title()} ({fw.confidence.value} confidence)")
                if fw.evidence:
                    print(f"     Evidence: {', '.join(fw.evidence[:3])}")
            print()
        
        # Workflow Components
        if intelligence.workflow_components:
            print(f"⚙️  WORKFLOW COMPONENTS")
            for wc in intelligence.workflow_components:
                print(f"   • {wc.component.value.title()} ({wc.confidence.value} confidence)")
                if wc.evidence:
                    print(f"     Evidence: {', '.join(wc.evidence[:3])}")
            print()
        
        # Medical Signals
        if intelligence.medical_signals:
            print(f"🏥 MEDICAL AI SIGNALS")
            for ms in intelligence.medical_signals:
                print(f"   • {ms.signal.value.replace('_', ' ').title()} ({ms.confidence.value} confidence)")
                if ms.evidence:
                    print(f"     Evidence: {', '.join(ms.evidence[:3])}")
            print()
        
        # Key Files
        if intelligence.key_files:
            print(f"📁 KEY FILES")
            for category, files in intelligence.key_files.items():
                if files:
                    print(f"   {category.title()}:")
                    for file in files[:5]:  # Show top 5
                        print(f"     • {file}")
            print()
        
        # Statistics
        print(f"📈 STATISTICS")
        print(f"   Python files: {intelligence.total_python_files}")
        print(f"   Notebook files: {intelligence.total_notebook_files}")
        print(f"   Config files: {intelligence.total_config_files}")
        print(f"   Has requirements.txt: {'✓' if intelligence.has_requirements else '✗'}")
        print(f"   Has Dockerfile: {'✓' if intelligence.has_dockerfile else '✗'}")
        print(f"   Has README: {'✓' if intelligence.has_readme else '✗'}")
        
        print(f"\n{'='*80}\n")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}\n")
        raise


async def main():
    """Main function with example repositories."""
    
    # Example repositories to analyze
    examples = [
        {
            "name": "MONAI - Medical Imaging Framework",
            "url": "https://github.com/Project-MONAI/MONAI",
            "branch": None
        },
        {
            "name": "PyTorch - Deep Learning Framework",
            "url": "https://github.com/pytorch/pytorch",
            "branch": None
        },
        {
            "name": "FastAPI - Web Framework",
            "url": "https://github.com/tiangolo/fastapi",
            "branch": None
        }
    ]
    
    # Check if URL provided as command line argument
    if len(sys.argv) > 1:
        url = sys.argv[1]
        branch = sys.argv[2] if len(sys.argv) > 2 else None
        await analyze_repository(url, branch)
    else:
        # Show usage
        print("\n" + "="*80)
        print("REPOSITORY STRUCTURE ANALYZER")
        print("="*80)
        print("\nUsage:")
        print("  python analyze_repository.py <github_url> [branch]")
        print("\nExamples:")
        print("  python analyze_repository.py https://github.com/Project-MONAI/MONAI")
        print("  python analyze_repository.py https://github.com/pytorch/pytorch main")
        print("\n" + "="*80)
        
        # Ask user to select an example
        print("\nExample repositories to analyze:")
        for i, example in enumerate(examples, 1):
            print(f"  {i}. {example['name']}")
            print(f"     {example['url']}")
        
        print(f"\n  0. Exit")
        
        try:
            choice = input("\nSelect an example (0-3): ").strip()
            
            if choice == "0":
                print("\nExiting...\n")
                return
            
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(examples):
                example = examples[choice_idx]
                await analyze_repository(example["url"], example["branch"])
            else:
                print("\n❌ Invalid choice\n")
        except (ValueError, KeyboardInterrupt):
            print("\n\nExiting...\n")


if __name__ == "__main__":
    asyncio.run(main())

# Made with Bob
