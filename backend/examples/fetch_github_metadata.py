"""
Example script demonstrating GitHub metadata fetcher usage.

This script shows how to use the GitHub metadata service to fetch
repository information without cloning.
"""
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.github_service import GitHubService, get_github_service
from app.services.github_service import (
    RepositoryNotFoundError,
    RateLimitError,
    GitHubServiceError
)


def print_metadata(metadata):
    """Pretty print repository metadata."""
    print("\n" + "="*60)
    print(f"📦 Repository: {metadata.full_name}")
    print("="*60)
    
    if metadata.description:
        print(f"\n📝 Description: {metadata.description}")
    
    print(f"\n👤 Owner: {metadata.owner.login} ({metadata.owner.type})")
    
    print(f"\n⭐ Stats:")
    print(f"   Stars: {metadata.stars:,}")
    print(f"   Forks: {metadata.forks:,}")
    print(f"   Watchers: {metadata.watchers:,}")
    print(f"   Open Issues: {metadata.open_issues:,}")
    
    if metadata.primary_language:
        print(f"\n💻 Primary Language: {metadata.primary_language}")
    
    if metadata.topics:
        print(f"\n🏷️  Topics: {', '.join(metadata.topics)}")
    
    print(f"\n🌿 Default Branch: {metadata.default_branch}")
    
    print(f"\n📊 Repository Info:")
    print(f"   Size: {metadata.size:,} KB")
    print(f"   Fork: {'Yes' if metadata.is_fork else 'No'}")
    print(f"   Archived: {'Yes' if metadata.is_archived else 'No'}")
    print(f"   Private: {'Yes' if metadata.is_private else 'No'}")
    
    if metadata.license:
        print(f"\n📄 License: {metadata.license}")
    
    if metadata.homepage:
        print(f"\n🌐 Homepage: {metadata.homepage}")
    
    print(f"\n🔗 URLs:")
    print(f"   Web: {metadata.html_url}")
    print(f"   Clone (HTTPS): {metadata.clone_url}")
    print(f"   Clone (SSH): {metadata.ssh_url}")
    
    print(f"\n📅 Timestamps:")
    print(f"   Created: {metadata.created_at}")
    print(f"   Updated: {metadata.updated_at}")
    print(f"   Last Push: {metadata.pushed_at}")
    
    print("\n" + "="*60 + "\n")


def check_rate_limit(service):
    """Check and display rate limit information."""
    rate_info = service.get_rate_limit_info()
    
    if "error" in rate_info:
        print(f"⚠️  Could not fetch rate limit: {rate_info['error']}")
        return
    
    limit = rate_info.get("limit", 0)
    remaining = rate_info.get("remaining", 0)
    used = rate_info.get("used", 0)
    
    print(f"\n📊 GitHub API Rate Limit:")
    print(f"   Limit: {limit} requests/hour")
    print(f"   Used: {used}")
    print(f"   Remaining: {remaining}")
    
    if remaining < 10:
        print(f"   ⚠️  WARNING: Low rate limit remaining!")
    
    percentage = (remaining / limit * 100) if limit > 0 else 0
    print(f"   Available: {percentage:.1f}%")


def example_basic_usage():
    """Example 1: Basic usage with a well-known repository."""
    print("\n" + "="*60)
    print("Example 1: Basic Usage")
    print("="*60)
    
    # Create service instance
    service = GitHubService()
    
    try:
        # Fetch metadata for a popular repository
        print("\nFetching metadata for 'fastapi/fastapi'...")
        metadata = service.fetch_repository_metadata("fastapi", "fastapi")
        print_metadata(metadata)
        
    except RepositoryNotFoundError as e:
        print(f"❌ Repository not found: {e}")
    except RateLimitError as e:
        print(f"⚠️  Rate limit exceeded: {e}")
    except GitHubServiceError as e:
        print(f"❌ GitHub API error: {e}")


def example_with_token():
    """Example 2: Using GitHub token for higher rate limits."""
    print("\n" + "="*60)
    print("Example 2: Using GitHub Token")
    print("="*60)
    
    # Get token from environment variable
    token = os.getenv("GITHUB_TOKEN")
    
    if not token:
        print("\n⚠️  No GITHUB_TOKEN found in environment.")
        print("   Set GITHUB_TOKEN for higher rate limits (5000/hr vs 60/hr)")
        print("   Using unauthenticated access...")
        service = GitHubService()
    else:
        print("\n✅ Using GitHub token for authentication")
        service = GitHubService(token=token)
    
    # Check rate limit
    check_rate_limit(service)
    
    try:
        print("\nFetching metadata for 'python/cpython'...")
        metadata = service.fetch_repository_metadata("python", "cpython")
        print_metadata(metadata)
        
    except Exception as e:
        print(f"❌ Error: {e}")


def example_singleton_pattern():
    """Example 3: Using singleton pattern for efficiency."""
    print("\n" + "="*60)
    print("Example 3: Singleton Pattern (Recommended)")
    print("="*60)
    
    print("\nUsing get_github_service() for connection pooling...")
    
    # Get singleton instance (reuses HTTP connections)
    service = get_github_service()
    
    repositories = [
        ("octocat", "Hello-World"),
        ("torvalds", "linux"),
        ("microsoft", "vscode")
    ]
    
    print(f"\nFetching metadata for {len(repositories)} repositories...\n")
    
    for owner, repo in repositories:
        try:
            print(f"📦 Fetching {owner}/{repo}...")
            metadata = service.fetch_repository_metadata(owner, repo)
            print(f"   ⭐ {metadata.stars:,} stars | "
                  f"💻 {metadata.primary_language or 'N/A'} | "
                  f"🏷️  {len(metadata.topics)} topics")
            
        except RepositoryNotFoundError:
            print(f"   ❌ Not found or private")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Check final rate limit
    check_rate_limit(service)


def example_error_handling():
    """Example 4: Comprehensive error handling."""
    print("\n" + "="*60)
    print("Example 4: Error Handling")
    print("="*60)
    
    service = get_github_service()
    
    # Test with non-existent repository
    print("\n1. Testing with non-existent repository...")
    try:
        metadata = service.fetch_repository_metadata(
            "this-user-does-not-exist-12345",
            "this-repo-does-not-exist-67890"
        )
    except RepositoryNotFoundError as e:
        print(f"   ✅ Correctly caught: {e}")
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
    
    # Test with valid repository
    print("\n2. Testing with valid repository...")
    try:
        metadata = service.fetch_repository_metadata("octocat", "Hello-World")
        print(f"   ✅ Successfully fetched: {metadata.full_name}")
    except Exception as e:
        print(f"   ❌ Error: {e}")


def example_metadata_analysis():
    """Example 5: Analyzing repository metadata."""
    print("\n" + "="*60)
    print("Example 5: Metadata Analysis")
    print("="*60)
    
    service = get_github_service()
    
    try:
        print("\nAnalyzing 'django/django'...")
        metadata = service.fetch_repository_metadata("django", "django")
        
        print(f"\n📊 Analysis Results:")
        print(f"   Repository: {metadata.full_name}")
        
        # Popularity score (simple calculation)
        popularity = metadata.stars + (metadata.forks * 2) + metadata.watchers
        print(f"   Popularity Score: {popularity:,}")
        
        # Activity indicators
        print(f"\n   Activity Indicators:")
        print(f"   - Open Issues: {metadata.open_issues:,}")
        print(f"   - Is Active: {'Yes' if not metadata.is_archived else 'No'}")
        
        # Technology stack
        print(f"\n   Technology:")
        print(f"   - Primary Language: {metadata.primary_language or 'Not specified'}")
        print(f"   - Topics: {len(metadata.topics)} tags")
        if metadata.topics:
            print(f"     {', '.join(metadata.topics[:5])}")
        
        # Size and complexity
        size_mb = metadata.size / 1024
        print(f"\n   Size: {size_mb:.2f} MB")
        if size_mb < 1:
            print(f"   - Classification: Small project")
        elif size_mb < 10:
            print(f"   - Classification: Medium project")
        else:
            print(f"   - Classification: Large project")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """Run all examples."""
    print("\n" + "="*60)
    print("GitHub Metadata Fetcher - Examples")
    print("="*60)
    
    # Run examples
    example_basic_usage()
    example_with_token()
    example_singleton_pattern()
    example_error_handling()
    example_metadata_analysis()
    
    print("\n" + "="*60)
    print("✅ All examples completed!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()

# Made with Bob