"""
Unit tests for GitHub URL parser utility.
Comprehensive test coverage for all supported URL formats and edge cases.
"""
import pytest
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.utils.github_parser import parse_github_url, validate_github_url, InvalidGitHubURLError


class TestParseGitHubURL:
    """Test cases for parse_github_url function."""
    
    def test_standard_https_url(self):
        """Test parsing standard HTTPS GitHub URL."""
        owner, repo = parse_github_url("https://github.com/octocat/Hello-World")
        assert owner == "octocat"
        assert repo == "Hello-World"
    
    def test_http_url(self):
        """Test parsing HTTP GitHub URL."""
        owner, repo = parse_github_url("http://github.com/owner/repo")
        assert owner == "owner"
        assert repo == "repo"
    
    def test_url_with_trailing_slash(self):
        """Test parsing URL with trailing slash."""
        owner, repo = parse_github_url("https://github.com/owner/repo/")
        assert owner == "owner"
        assert repo == "repo"
    
    def test_url_with_git_extension(self):
        """Test parsing URL with .git extension."""
        owner, repo = parse_github_url("https://github.com/owner/repo.git")
        assert owner == "owner"
        assert repo == "repo"
    
    def test_url_with_git_extension_and_trailing_slash(self):
        """Test parsing URL with .git extension and trailing slash."""
        owner, repo = parse_github_url("https://github.com/owner/repo.git/")
        assert owner == "owner"
        assert repo == "repo"
    
    def test_ssh_url(self):
        """Test parsing SSH format GitHub URL."""
        owner, repo = parse_github_url("git@github.com:owner/repo.git")
        assert owner == "owner"
        assert repo == "repo"
    
    def test_ssh_url_without_git_extension(self):
        """Test parsing SSH format URL without .git extension."""
        owner, repo = parse_github_url("git@github.com:owner/repo")
        assert owner == "owner"
        assert repo == "repo"
    
    def test_repo_with_hyphens(self):
        """Test parsing repo name with hyphens."""
        owner, repo = parse_github_url("https://github.com/my-org/my-repo")
        assert owner == "my-org"
        assert repo == "my-repo"
    
    def test_repo_with_underscores(self):
        """Test parsing repo name with underscores."""
        owner, repo = parse_github_url("https://github.com/my_org/my_repo")
        assert owner == "my_org"
        assert repo == "my_repo"
    
    def test_repo_with_dots(self):
        """Test parsing repo name with dots."""
        owner, repo = parse_github_url("https://github.com/owner/repo.name")
        assert owner == "owner"
        assert repo == "repo.name"
    
    def test_repo_with_numbers(self):
        """Test parsing repo name with numbers."""
        owner, repo = parse_github_url("https://github.com/user123/repo456")
        assert owner == "user123"
        assert repo == "repo456"
    
    def test_url_with_whitespace_stripped(self):
        """Test parsing URL with leading/trailing whitespace."""
        owner, repo = parse_github_url("  https://github.com/owner/repo  ")
        assert owner == "owner"
        assert repo == "repo"
    
    def test_invalid_url_not_github(self):
        """Test that non-GitHub URLs raise error."""
        with pytest.raises(InvalidGitHubURLError) as exc_info:
            parse_github_url("https://gitlab.com/owner/repo")
        assert "Invalid GitHub URL format" in str(exc_info.value)
    
    def test_invalid_url_missing_repo(self):
        """Test that URL missing repo name raises error."""
        with pytest.raises(InvalidGitHubURLError) as exc_info:
            parse_github_url("https://github.com/owner")
        assert "Invalid GitHub URL format" in str(exc_info.value)
    
    def test_invalid_url_missing_owner(self):
        """Test that URL missing owner raises error."""
        with pytest.raises(InvalidGitHubURLError) as exc_info:
            parse_github_url("https://github.com/")
        assert "Invalid GitHub URL format" in str(exc_info.value)
    
    def test_invalid_url_empty_string(self):
        """Test that empty string raises error."""
        with pytest.raises(InvalidGitHubURLError) as exc_info:
            parse_github_url("")
        assert "URL cannot be empty" in str(exc_info.value)
    
    def test_invalid_url_whitespace_only(self):
        """Test that whitespace-only string raises error."""
        with pytest.raises(InvalidGitHubURLError) as exc_info:
            parse_github_url("   ")
        assert "URL cannot be empty" in str(exc_info.value)
    
    def test_invalid_url_none(self):
        """Test that None raises error."""
        with pytest.raises(InvalidGitHubURLError) as exc_info:
            parse_github_url(None)
        assert "URL must be a non-empty string" in str(exc_info.value)
    
    def test_invalid_url_malformed(self):
        """Test that malformed URL raises error."""
        with pytest.raises(InvalidGitHubURLError) as exc_info:
            parse_github_url("not-a-url")
        assert "Invalid GitHub URL format" in str(exc_info.value)
    
    def test_invalid_url_with_extra_path(self):
        """Test that URL with extra path segments raises error."""
        with pytest.raises(InvalidGitHubURLError) as exc_info:
            parse_github_url("https://github.com/owner/repo/issues")
        assert "Invalid GitHub URL format" in str(exc_info.value)
    
    def test_invalid_url_with_query_params(self):
        """Test that URL with query parameters raises error."""
        with pytest.raises(InvalidGitHubURLError) as exc_info:
            parse_github_url("https://github.com/owner/repo?tab=readme")
        assert "Invalid GitHub URL format" in str(exc_info.value)


class TestValidateGitHubURL:
    """Test cases for validate_github_url function."""
    
    def test_validate_valid_url(self):
        """Test validation of valid GitHub URL."""
        assert validate_github_url("https://github.com/owner/repo") is True
    
    def test_validate_valid_url_with_git(self):
        """Test validation of valid GitHub URL with .git."""
        assert validate_github_url("https://github.com/owner/repo.git") is True
    
    def test_validate_valid_ssh_url(self):
        """Test validation of valid SSH URL."""
        assert validate_github_url("git@github.com:owner/repo.git") is True
    
    def test_validate_invalid_url(self):
        """Test validation of invalid URL."""
        assert validate_github_url("https://gitlab.com/owner/repo") is False
    
    def test_validate_empty_string(self):
        """Test validation of empty string."""
        assert validate_github_url("") is False
    
    def test_validate_malformed_url(self):
        """Test validation of malformed URL."""
        assert validate_github_url("not-a-url") is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

# Made with Bob
