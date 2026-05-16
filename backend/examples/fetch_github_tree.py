"""
Example script demonstrating GitHub repository tree fetching.

This script shows how to use the GitHubTreeService to fetch and analyze
repository tree structures without cloning.

Usage:
    python examples/fetch_github_tree.py
"""
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.github_tree_service import get_github_tree_service, GitHubTreeServiceError
from app.models.github import ImportanceLevel


def print_separator(char="-", length=80):
    """Print a separator line."""
    print(char * length)


def example_1_basic_fetch():
    """Example 1: Basic repository tree fetch."""
    print("\n" + "=" * 80)
    print("EXAMPLE 1: Basic Repository Tree Fetch")
    print("=" * 80)
    
    tree_service = get_github_tree_service()
    
    try:
        # Fetch tree for a small public repository
        print("\nFetching tree for 'octocat/Hello-World'...")
        tree = tree_service.fetch_repository_tree(
            owner="octocat",
            repo="Hello-World"
        )
        
        print(f"\n✅ Successfully fetched repository tree!")
        print(f"   Owner: {tree.owner}")
        print(f"   Repository: {tree.repo}")
        print(f"   Branch: {tree.branch}")
        print(f"   Total files: {tree.total_files}")
        print(f"   Total directories: {tree.total_directories}")
        print(f"   Filtered files: {tree.filtered_files}")
        print(f"   Filtered directories: {tree.filtered_directories}")
        print(f"   Truncated: {tree.truncated}")
        
        print("\n📁 Sample files:")
        for i, file in enumerate(tree.files[:5], 1):
            print(f"   {i}. {file.path} ({file.size} bytes)")
        
        if len(tree.files) > 5:
            print(f"   ... and {len(tree.files) - 5} more files")
        
    except GitHubTreeServiceError as e:
        print(f"\n❌ Error: {e}")


def example_2_ml_project_analysis():
    """Example 2: Analyze ML project structure."""
    print("\n" + "=" * 80)
    print("EXAMPLE 2: ML Project Analysis")
    print("=" * 80)
    
    tree_service = get_github_tree_service()
    
    try:
        # Analyze a machine learning repository
        print("\nAnalyzing ML project structure...")
        print("Repository: pytorch/examples")
        
        tree = tree_service.fetch_repository_tree(
            owner="pytorch",
            repo="examples",
            max_depth=3  # Limit depth for faster results
        )
        
        print(f"\n✅ Analysis complete!")
        print(f"   Total files: {tree.total_files}")
        print(f"   Filtered files: {tree.filtered_files}")
        
        # Show important files by category
        print("\n🔴 CRITICAL FILES (Training/Inference):")
        critical_files = tree.important_files.get("critical", [])
        if critical_files:
            for file in critical_files[:10]:
                print(f"   - {file.path}")
            if len(critical_files) > 10:
                print(f"   ... and {len(critical_files) - 10} more")
        else:
            print("   None found")
        
        print("\n🟡 HIGH IMPORTANCE FILES (Config/Dependencies):")
        high_files = tree.important_files.get("high", [])
        if high_files:
            for file in high_files[:10]:
                print(f"   - {file.path}")
            if len(high_files) > 10:
                print(f"   ... and {len(high_files) - 10} more")
        else:
            print("   None found")
        
        print("\n🟢 MEDIUM IMPORTANCE FILES (Notebooks/Utils):")
        medium_files = tree.important_files.get("medium", [])
        if medium_files:
            for file in medium_files[:10]:
                print(f"   - {file.path}")
            if len(medium_files) > 10:
                print(f"   ... and {len(medium_files) - 10} more")
        else:
            print("   None found")
        
    except GitHubTreeServiceError as e:
        print(f"\n❌ Error: {e}")


def example_3_find_specific_files():
    """Example 3: Find specific file types."""
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Find Specific File Types")
    print("=" * 80)
    
    tree_service = get_github_tree_service()
    
    try:
        print("\nSearching for Jupyter notebooks and Python files...")
        print("Repository: fastapi/fastapi")
        
        tree = tree_service.fetch_repository_tree(
            owner="fastapi",
            repo="fastapi",
            max_depth=2
        )
        
        # Find Jupyter notebooks
        notebooks = [f for f in tree.files if f.path.endswith('.ipynb')]
        print(f"\n📓 Found {len(notebooks)} Jupyter notebooks:")
        for nb in notebooks[:5]:
            print(f"   - {nb.path}")
        
        # Find Python files
        python_files = [f for f in tree.files if f.path.endswith('.py')]
        print(f"\n🐍 Found {len(python_files)} Python files")
        
        # Find configuration files
        config_files = [f for f in tree.files if any(
            x in f.name.lower() for x in ['config', 'settings', 'requirements']
        )]
        print(f"\n⚙️  Found {len(config_files)} configuration files:")
        for cfg in config_files[:5]:
            print(f"   - {cfg.path}")
        
    except GitHubTreeServiceError as e:
        print(f"\n❌ Error: {e}")


def example_4_with_filtering():
    """Example 4: Compare with and without filtering."""
    print("\n" + "=" * 80)
    print("EXAMPLE 4: Filtering Comparison")
    print("=" * 80)
    
    tree_service = get_github_tree_service()
    
    try:
        print("\nFetching tree WITH filtering (default)...")
        tree_filtered = tree_service.fetch_repository_tree(
            owner="tensorflow",
            repo="tensorflow",
            max_depth=2,
            include_filtered=False
        )
        
        print(f"   Filtered files: {tree_filtered.filtered_files}")
        print(f"   Filtered directories: {tree_filtered.filtered_directories}")
        
        print("\nFetching tree WITHOUT filtering...")
        tree_unfiltered = tree_service.fetch_repository_tree(
            owner="tensorflow",
            repo="tensorflow",
            max_depth=2,
            include_filtered=True
        )
        
        print(f"   Unfiltered files: {tree_unfiltered.filtered_files}")
        print(f"   Unfiltered directories: {tree_unfiltered.filtered_directories}")
        
        files_filtered_out = tree_unfiltered.filtered_files - tree_filtered.filtered_files
        dirs_filtered_out = tree_unfiltered.filtered_directories - tree_filtered.filtered_directories
        
        print(f"\n📊 Filtering Statistics:")
        print(f"   Files filtered out: {files_filtered_out}")
        print(f"   Directories filtered out: {dirs_filtered_out}")
        print(f"   Reduction: {files_filtered_out / tree_unfiltered.filtered_files * 100:.1f}% fewer files")
        
    except GitHubTreeServiceError as e:
        print(f"\n❌ Error: {e}")


def example_5_directory_structure():
    """Example 5: Analyze directory structure."""
    print("\n" + "=" * 80)
    print("EXAMPLE 5: Directory Structure Analysis")
    print("=" * 80)
    
    tree_service = get_github_tree_service()
    
    try:
        print("\nAnalyzing directory structure...")
        print("Repository: scikit-learn/scikit-learn")
        
        tree = tree_service.fetch_repository_tree(
            owner="scikit-learn",
            repo="scikit-learn",
            max_depth=2
        )
        
        print(f"\n📁 Top-level directories:")
        top_level_dirs = [d for d in tree.directories if '/' not in d.path]
        for directory in sorted(top_level_dirs, key=lambda x: x.name)[:15]:
            print(f"   - {directory.name}/")
        
        if len(top_level_dirs) > 15:
            print(f"   ... and {len(top_level_dirs) - 15} more")
        
        print(f"\n📊 Directory Statistics:")
        print(f"   Total directories: {tree.total_directories}")
        print(f"   After filtering: {tree.filtered_directories}")
        
    except GitHubTreeServiceError as e:
        print(f"\n❌ Error: {e}")


def main():
    """Run all examples."""
    print("\n" + "=" * 80)
    print("GitHub Repository Tree Fetcher - Examples")
    print("=" * 80)
    print("\nThese examples demonstrate how to use the GitHubTreeService")
    print("to fetch and analyze repository structures without cloning.")
    
    # Run examples
    example_1_basic_fetch()
    example_2_ml_project_analysis()
    example_3_find_specific_files()
    example_4_with_filtering()
    example_5_directory_structure()
    
    print("\n" + "=" * 80)
    print("Examples completed!")
    print("=" * 80)
    print("\nFor more information, see: backend/README_GITHUB_TREE.md")
    print()


if __name__ == "__main__":
    main()


# Made with Bob