"""
Unit tests for GitHub metadata service.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from app.services.github_service import (
    GitHubService,
    GitHubServiceError,
    RepositoryNotFoundError,
    RateLimitError,
    get_github_service
)
from app.models.github import GitHubRepoMetadata, GitHubOwner


class TestGitHubService:
    """Test cases for GitHubService class."""
    
    def test_init_without_token(self):
        """Test service initialization without token."""
        service = GitHubService()
        assert service.session is not None
        assert "User-Agent" in service.session.headers
        assert "Accept" in service.session.headers
    
    def test_init_with_token(self):
        """Test service initialization with token."""
        service = GitHubService(token="test_token_123")
        assert "Authorization" in service.session.headers
        assert service.session.headers["Authorization"] == "token test_token_123"
    
    @patch('app.services.github_service.requests.Session')
    def test_fetch_repository_metadata_success(self, mock_session_class):
        """Test successful repository metadata fetch."""
        # Mock response data
        mock_response_data = {
            "name": "Hello-World",
            "full_name": "octocat/Hello-World",
            "description": "My first repository",
            "owner": {
                "login": "octocat",
                "type": "User",
                "avatar_url": "https://github.com/images/error/octocat_happy.gif"
            },
            "stargazers_count": 1500,
            "forks_count": 500,
            "watchers_count": 1500,
            "open_issues_count": 10,
            "language": "Python",
            "topics": ["python", "api"],
            "default_branch": "main",
            "created_at": "2011-01-26T19:01:12Z",
            "updated_at": "2024-01-15T10:30:00Z",
            "pushed_at": "2024-01-15T10:30:00Z",
            "size": 180,
            "fork": False,
            "archived": False,
            "private": False,
            "html_url": "https://github.com/octocat/Hello-World",
            "clone_url": "https://github.com/octocat/Hello-World.git",
            "ssh_url": "git@github.com:octocat/Hello-World.git",
            "homepage": "https://example.com",
            "license": {
                "name": "MIT License",
                "spdx_id": "MIT"
            }
        }
        
        # Setup mock
        mock_session = MagicMock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_response_data
        mock_session.get.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        # Test
        service = GitHubService()
        metadata = service.fetch_repository_metadata("octocat", "Hello-World")
        
        # Assertions
        assert isinstance(metadata, GitHubRepoMetadata)
        assert metadata.name == "Hello-World"
        assert metadata.full_name == "octocat/Hello-World"
        assert metadata.stars == 1500
        assert metadata.primary_language == "Python"
        assert metadata.topics == ["python", "api"]
        assert metadata.owner.login == "octocat"
        assert metadata.license == "MIT License"
    
    @patch('app.services.github_service.requests.Session')
    def test_fetch_repository_not_found(self, mock_session_class):
        """Test repository not found error."""
        mock_session = MagicMock()
        mock_response = Mock()
        mock_response.status_code = 404
        mock_session.get.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        service = GitHubService()
        
        with pytest.raises(RepositoryNotFoundError) as exc_info:
            service.fetch_repository_metadata("nonexistent", "repo")
        
        assert "not found" in str(exc_info.value).lower()
    
    @patch('app.services.github_service.requests.Session')
    def test_fetch_repository_rate_limit(self, mock_session_class):
        """Test rate limit error handling."""
        mock_session = MagicMock()
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.headers = {
            "X-RateLimit-Remaining": "0",
            "X-RateLimit-Reset": "1234567890"
        }
        mock_session.get.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        service = GitHubService()
        
        with pytest.raises(RateLimitError) as exc_info:
            service.fetch_repository_metadata("owner", "repo")
        
        assert "rate limit" in str(exc_info.value).lower()
    
    @patch('app.services.github_service.requests.Session')
    def test_fetch_repository_timeout(self, mock_session_class):
        """Test timeout error handling."""
        mock_session = MagicMock()
        mock_session.get.side_effect = Exception("Timeout")
        mock_session_class.return_value = mock_session
        
        service = GitHubService()
        
        with pytest.raises(GitHubServiceError):
            service.fetch_repository_metadata("owner", "repo")
    
    @patch('app.services.github_service.requests.Session')
    def test_get_rate_limit_info_success(self, mock_session_class):
        """Test successful rate limit info fetch."""
        mock_response_data = {
            "resources": {
                "core": {
                    "limit": 5000,
                    "remaining": 4999,
                    "reset": 1234567890,
                    "used": 1
                }
            }
        }
        
        mock_session = MagicMock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_response_data
        mock_session.get.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        service = GitHubService()
        rate_info = service.get_rate_limit_info()
        
        assert rate_info["limit"] == 5000
        assert rate_info["remaining"] == 4999
        assert rate_info["used"] == 1
    
    @patch('app.services.github_service.requests.Session')
    def test_get_rate_limit_info_error(self, mock_session_class):
        """Test rate limit info fetch error handling."""
        mock_session = MagicMock()
        mock_response = Mock()
        mock_response.status_code = 500
        mock_session.get.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        service = GitHubService()
        rate_info = service.get_rate_limit_info()
        
        assert "error" in rate_info
    
    @patch('app.services.github_service.requests.Session')
    def test_metadata_without_license(self, mock_session_class):
        """Test metadata fetch for repository without license."""
        mock_response_data = {
            "name": "test-repo",
            "full_name": "user/test-repo",
            "description": None,
            "owner": {
                "login": "user",
                "type": "User",
                "avatar_url": None
            },
            "stargazers_count": 0,
            "forks_count": 0,
            "watchers_count": 0,
            "open_issues_count": 0,
            "language": None,
            "topics": [],
            "default_branch": "main",
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z",
            "pushed_at": "2024-01-01T00:00:00Z",
            "size": 0,
            "fork": False,
            "archived": False,
            "private": False,
            "html_url": "https://github.com/user/test-repo",
            "clone_url": "https://github.com/user/test-repo.git",
            "ssh_url": "git@github.com:user/test-repo.git",
            "homepage": None,
            "license": None
        }
        
        mock_session = MagicMock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_response_data
        mock_session.get.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        service = GitHubService()
        metadata = service.fetch_repository_metadata("user", "test-repo")
        
        assert metadata.license is None
        assert metadata.description is None
        assert metadata.primary_language is None


class TestGetGitHubService:
    """Test cases for get_github_service singleton function."""
    
    def test_singleton_returns_same_instance(self):
        """Test that get_github_service returns the same instance."""
        service1 = get_github_service()
        service2 = get_github_service()
        
        assert service1 is service2
    
    def test_singleton_instance_is_github_service(self):
        """Test that singleton returns GitHubService instance."""
        service = get_github_service()
        assert isinstance(service, GitHubService)


# Integration test markers
@pytest.mark.integration
class TestGitHubServiceIntegration:
    """Integration tests for GitHub service (requires internet connection)."""
    
    def test_fetch_real_repository(self):
        """Test fetching a real public repository."""
        service = GitHubService()
        
        # Use a well-known public repository
        metadata = service.fetch_repository_metadata("octocat", "Hello-World")
        
        assert metadata.name == "Hello-World"
        assert metadata.owner.login == "octocat"
        assert metadata.stars >= 0
        assert metadata.html_url == "https://github.com/octocat/Hello-World"
    
    def test_fetch_nonexistent_repository(self):
        """Test fetching a non-existent repository."""
        service = GitHubService()
        
        with pytest.raises(RepositoryNotFoundError):
            service.fetch_repository_metadata(
                "this-user-definitely-does-not-exist-12345",
                "this-repo-does-not-exist-67890"
            )
    
    def test_get_real_rate_limit(self):
        """Test getting real rate limit information."""
        service = GitHubService()
        rate_info = service.get_rate_limit_info()
        
        assert "limit" in rate_info
        assert "remaining" in rate_info
        assert isinstance(rate_info["limit"], int)
        assert isinstance(rate_info["remaining"], int)

# Made with Bob