"""
Lightweight GitHub repository metadata fetcher service.
Uses GitHub REST API v3 to fetch repository metadata without cloning.
Optimized for low RAM usage and hackathon MVP simplicity.
"""
import requests
from typing import Optional, Dict, Any
from app.models.github import GitHubRepoMetadata, GitHubOwner
from app.core.config import GITHUB_TOKEN


class GitHubServiceError(Exception):
    """Base exception for GitHub service errors."""
    pass


class RepositoryNotFoundError(GitHubServiceError):
    """Raised when repository is not found."""
    pass


class RateLimitError(GitHubServiceError):
    """Raised when GitHub API rate limit is exceeded."""
    pass


class GitHubService:
    """
    Service for fetching GitHub repository metadata using REST API.
    
    Features:
    - No repository cloning (lightweight)
    - Uses GitHub REST API v3
    - Supports authenticated and unauthenticated requests
    - Optimized for low memory usage
    """
    
    BASE_URL = "https://api.github.com"
    
    def __init__(self, token: Optional[str] = None):
        """
        Initialize GitHub service.
        
        Args:
            token: Optional GitHub personal access token for higher rate limits
                  (5000 requests/hour vs 60 requests/hour for unauthenticated)
        """
        self.token = token or GITHUB_TOKEN
        self.session = requests.Session()
        
        # Set headers for API requests
        self.session.headers.update({
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "NeuroCode-AI-Metadata-Fetcher"
        })
        
        # Add authentication if token is provided and not empty
        if self.token and self.token.strip():
            self.session.headers.update({
                "Authorization": f"token {self.token}"
            })
    
    def fetch_repository_metadata(self, owner: str, repo: str) -> GitHubRepoMetadata:
        """
        Fetch complete repository metadata from GitHub REST API.
        
        Args:
            owner: Repository owner username or organization name
            repo: Repository name
            
        Returns:
            GitHubRepoMetadata object with all repository information
            
        Raises:
            RepositoryNotFoundError: If repository doesn't exist or is inaccessible
            RateLimitError: If API rate limit is exceeded
            GitHubServiceError: For other API errors
            
        Examples:
            >>> service = GitHubService()
            >>> metadata = service.fetch_repository_metadata("octocat", "Hello-World")
            >>> print(metadata.stars)
            1500
        """
        url = f"{self.BASE_URL}/repos/{owner}/{repo}"
        
        try:
            response = self.session.get(url, timeout=10)
            
            # Handle rate limiting
            if response.status_code == 403:
                rate_limit_remaining = response.headers.get("X-RateLimit-Remaining", "0")
                if rate_limit_remaining == "0":
                    reset_time = response.headers.get("X-RateLimit-Reset", "unknown")
                    raise RateLimitError(
                        f"GitHub API rate limit exceeded. Resets at: {reset_time}. "
                        "Consider using a GitHub token for higher limits."
                    )
            
            # Handle not found
            if response.status_code == 404:
                raise RepositoryNotFoundError(
                    f"Repository '{owner}/{repo}' not found or is private/inaccessible"
                )
            
            # Handle other errors
            if response.status_code != 200:
                raise GitHubServiceError(
                    f"GitHub API error: {response.status_code} - {response.text}"
                )
            
            # Parse response
            data = response.json()
            
            # Extract license name if present
            license_name = None
            if data.get("license") and isinstance(data["license"], dict):
                license_name = data["license"].get("name") or data["license"].get("spdx_id")
            
            # Build owner object
            owner_data = data.get("owner", {})
            owner_obj = GitHubOwner(
                login=owner_data.get("login", owner),
                type=owner_data.get("type", "User"),
                avatar_url=owner_data.get("avatar_url")
            )
            
            # Create metadata object with all fields
            metadata = GitHubRepoMetadata(
                name=data["name"],
                full_name=data["full_name"],
                description=data.get("description"),
                owner=owner_obj,
                stargazers_count=data.get("stargazers_count", 0),
                forks_count=data.get("forks_count", 0),
                watchers_count=data.get("watchers_count", 0),
                open_issues_count=data.get("open_issues_count", 0),
                language=data.get("language"),
                topics=data.get("topics", []),
                default_branch=data.get("default_branch", "main"),
                created_at=data["created_at"],
                updated_at=data["updated_at"],
                pushed_at=data["pushed_at"],
                size=data.get("size", 0),
                fork=data.get("fork", False),
                archived=data.get("archived", False),
                private=data.get("private", False),
                html_url=data["html_url"],
                clone_url=data["clone_url"],
                ssh_url=data["ssh_url"],
                homepage=data.get("homepage"),
                license=license_name
            )
            
            return metadata
            
        except requests.exceptions.Timeout:
            raise GitHubServiceError("Request to GitHub API timed out")
        except requests.exceptions.ConnectionError:
            raise GitHubServiceError("Failed to connect to GitHub API")
        except requests.exceptions.RequestException as e:
            raise GitHubServiceError(f"Request error: {str(e)}")
        except (KeyError, ValueError) as e:
            raise GitHubServiceError(f"Failed to parse GitHub API response: {str(e)}")
    
    def get_rate_limit_info(self) -> Dict[str, Any]:
        """
        Get current rate limit information from GitHub API.
        
        Returns:
            Dictionary with rate limit information including:
            - limit: Maximum requests per hour
            - remaining: Remaining requests
            - reset: Unix timestamp when limit resets
            
        Examples:
            >>> service = GitHubService()
            >>> info = service.get_rate_limit_info()
            >>> print(f"Remaining: {info['remaining']}/{info['limit']}")
        """
        url = f"{self.BASE_URL}/rate_limit"
        
        try:
            response = self.session.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                core_limits = data.get("resources", {}).get("core", {})
                return {
                    "limit": core_limits.get("limit", 0),
                    "remaining": core_limits.get("remaining", 0),
                    "reset": core_limits.get("reset", 0),
                    "used": core_limits.get("used", 0)
                }
            return {"error": f"Failed to fetch rate limit: {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}
    
    def __del__(self):
        """Clean up session on deletion."""
        if hasattr(self, 'session'):
            self.session.close()


# Singleton instance for reuse across requests (connection pooling)
_github_service_instance: Optional[GitHubService] = None


def get_github_service() -> GitHubService:
    """
    Get or create a singleton GitHubService instance.
    Reuses HTTP session for better performance.
    
    Returns:
        GitHubService instance
    """
    global _github_service_instance
    if _github_service_instance is None:
        _github_service_instance = GitHubService()
    return _github_service_instance

# Made with Bob