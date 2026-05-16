"""
Lightweight GitHub repository URL parser utility.
Optimized for hackathon MVP with minimal dependencies and low RAM usage.
"""
import re
from typing import Tuple, Optional


# Compiled regex patterns for efficient parsing (cached in memory)
# Matches: https://github.com/owner/repo, http://github.com/owner/repo
HTTPS_PATTERN = re.compile(
    r'^https?://github\.com/([a-zA-Z0-9_-]+)/([a-zA-Z0-9_.-]+?)(?:\.git)?/?$'
)

# Matches: git@github.com:owner/repo.git
SSH_PATTERN = re.compile(
    r'^git@github\.com:([a-zA-Z0-9_-]+)/([a-zA-Z0-9_.-]+?)(?:\.git)?$'
)


class InvalidGitHubURLError(Exception):
    """Custom exception for invalid GitHub URLs."""
    pass


def parse_github_url(url: str) -> Tuple[str, str]:
    """
    Parse a GitHub repository URL and extract owner and repository name.
    
    Supports the following URL formats:
    - https://github.com/owner/repo
    - https://github.com/owner/repo/
    - https://github.com/owner/repo.git
    - http://github.com/owner/repo
    - git@github.com:owner/repo.git
    
    Args:
        url: GitHub repository URL to parse
        
    Returns:
        Tuple of (owner, repo_name)
        
    Raises:
        InvalidGitHubURLError: If the URL is not a valid GitHub repository URL
        
    Examples:
        >>> parse_github_url("https://github.com/octocat/Hello-World")
        ('octocat', 'Hello-World')
        
        >>> parse_github_url("https://github.com/owner/repo.git")
        ('owner', 'repo')
        
        >>> parse_github_url("git@github.com:owner/repo.git")
        ('owner', 'repo')
    """
    if not url or not isinstance(url, str):
        raise InvalidGitHubURLError("URL must be a non-empty string")
    
    # Strip whitespace
    url = url.strip()
    
    if not url:
        raise InvalidGitHubURLError("URL cannot be empty or whitespace only")
    
    # Try HTTPS/HTTP pattern first (most common)
    match = HTTPS_PATTERN.match(url)
    if match:
        owner, repo = match.groups()
        return owner, repo
    
    # Try SSH pattern
    match = SSH_PATTERN.match(url)
    if match:
        owner, repo = match.groups()
        return owner, repo
    
    # No pattern matched - invalid URL
    raise InvalidGitHubURLError(
        "Invalid GitHub URL format: URL must be a valid GitHub repository URL "
        "(e.g., https://github.com/owner/repo or git@github.com:owner/repo.git)"
    )


def validate_github_url(url: str) -> bool:
    """
    Validate if a URL is a valid GitHub repository URL.
    
    Args:
        url: URL to validate
        
    Returns:
        True if valid, False otherwise
        
    Examples:
        >>> validate_github_url("https://github.com/owner/repo")
        True
        
        >>> validate_github_url("https://gitlab.com/owner/repo")
        False
    """
    try:
        parse_github_url(url)
        return True
    except InvalidGitHubURLError:
        return False

# Made with Bob
