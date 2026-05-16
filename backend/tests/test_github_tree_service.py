"""
Tests for GitHub tree service.
"""
import pytest
from unittest.mock import Mock, patch
from app.services.github_tree_service import (
    GitHubTreeService,
    GitHubTreeServiceError
)
from app.models.github import FileType, ImportanceLevel


class TestGitHubTreeService:
    """Test cases for GitHubTreeService."""
    
    def test_should_filter_path_node_modules(self):
        """Test filtering of node_modules directory."""
        service = GitHubTreeService()
        
        assert service._should_filter_path("node_modules/package.json") is True
        assert service._should_filter_path("src/node_modules/file.js") is True
        assert service._should_filter_path("src/components/Button.tsx") is False
    
    def test_should_filter_path_git_directory(self):
        """Test filtering of .git directory."""
        service = GitHubTreeService()
        
        assert service._should_filter_path(".git/config") is True
        assert service._should_filter_path("src/.git/HEAD") is True
        assert service._should_filter_path(".github/workflows/ci.yml") is False
    
    def test_should_filter_path_pycache(self):
        """Test filtering of __pycache__ directory."""
        service = GitHubTreeService()
        
        assert service._should_filter_path("__pycache__/module.pyc") is True
        assert service._should_filter_path("src/__pycache__/test.pyc") is True
        assert service._should_filter_path("src/cache_utils.py") is False
    
    def test_should_filter_path_model_weights(self):
        """Test filtering of model weight files."""
        service = GitHubTreeService()
        
        assert service._should_filter_path("models/model.h5") is True
        assert service._should_filter_path("checkpoints/best.pth") is True
        assert service._should_filter_path("weights/model.ckpt") is True
        assert service._should_filter_path("models/architecture.py") is False
    
    def test_should_filter_path_binaries(self):
        """Test filtering of binary files."""
        service = GitHubTreeService()
        
        assert service._should_filter_path("dist/app.exe") is True
        assert service._should_filter_path("lib/library.dll") is True
        assert service._should_filter_path("build/output.so") is True
        assert service._should_filter_path("src/main.py") is False
    
    def test_should_filter_path_with_include_filtered(self):
        """Test that filtering is disabled when include_filtered is True."""
        service = GitHubTreeService()
        
        assert service._should_filter_path("node_modules/package.json", include_filtered=True) is False
        assert service._should_filter_path(".git/config", include_filtered=True) is False
        assert service._should_filter_path("models/model.h5", include_filtered=True) is False
    
    def test_detect_importance_critical_files(self):
        """Test detection of critical ML/AI files."""
        service = GitHubTreeService()
        
        assert service._detect_importance("train.py", "train.py") == ImportanceLevel.CRITICAL
        assert service._detect_importance("src/training.py", "training.py") == ImportanceLevel.CRITICAL
        assert service._detect_importance("infer.py", "infer.py") == ImportanceLevel.CRITICAL
        assert service._detect_importance("inference.py", "inference.py") == ImportanceLevel.CRITICAL
        assert service._detect_importance("model.py", "model.py") == ImportanceLevel.CRITICAL
        assert service._detect_importance("main.py", "main.py") == ImportanceLevel.CRITICAL
    
    def test_detect_importance_high_files(self):
        """Test detection of high importance files."""
        service = GitHubTreeService()
        
        assert service._detect_importance("requirements.txt", "requirements.txt") == ImportanceLevel.HIGH
        assert service._detect_importance("README.md", "README.md") == ImportanceLevel.HIGH
        assert service._detect_importance("Dockerfile", "Dockerfile") == ImportanceLevel.HIGH
        assert service._detect_importance("config.yaml", "config.yaml") == ImportanceLevel.HIGH
        assert service._detect_importance("setup.py", "setup.py") == ImportanceLevel.HIGH
    
    def test_detect_importance_medium_files(self):
        """Test detection of medium importance files."""
        service = GitHubTreeService()
        
        assert service._detect_importance("notebook.ipynb", "notebook.ipynb") == ImportanceLevel.MEDIUM
        assert service._detect_importance("data_preprocessing.py", "data_preprocessing.py") == ImportanceLevel.MEDIUM
        assert service._detect_importance("utils.py", "utils.py") == ImportanceLevel.MEDIUM
        assert service._detect_importance("metrics.py", "metrics.py") == ImportanceLevel.MEDIUM
        assert service._detect_importance("augmentation.py", "augmentation.py") == ImportanceLevel.MEDIUM
    
    def test_detect_importance_low_files(self):
        """Test detection of low importance files."""
        service = GitHubTreeService()
        
        assert service._detect_importance("tests/test_model.py", "test_model.py") == ImportanceLevel.LOW
        assert service._detect_importance("docs/api.md", "api.md") == ImportanceLevel.LOW
        assert service._detect_importance("examples/demo.py", "demo.py") == ImportanceLevel.LOW
    
    def test_detect_importance_none(self):
        """Test files with no special importance."""
        service = GitHubTreeService()
        
        assert service._detect_importance("src/helper.py", "helper.py") == ImportanceLevel.NONE
        assert service._detect_importance("lib/constants.py", "constants.py") == ImportanceLevel.NONE
    
    @patch('app.services.github_tree_service.requests.Session')
    def test_get_default_branch_success(self, mock_session_class):
        """Test getting default branch successfully."""
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"default_branch": "main"}
        mock_session.get.return_value = mock_response
        
        service = GitHubTreeService()
        branch = service._get_default_branch("owner", "repo")
        
        assert branch == "main"
    
    @patch('app.services.github_tree_service.requests.Session')
    def test_get_default_branch_fallback(self, mock_session_class):
        """Test fallback to 'main' when API call fails."""
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        
        mock_response = Mock()
        mock_response.status_code = 404
        mock_session.get.return_value = mock_response
        
        service = GitHubTreeService()
        branch = service._get_default_branch("owner", "repo")
        
        assert branch == "main"
    
    @patch('app.services.github_tree_service.requests.Session')
    def test_fetch_repository_tree_success(self, mock_session_class):
        """Test successful repository tree fetch."""
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        
        # Mock responses for default branch, tree SHA, and tree fetch
        mock_responses = [
            # Default branch response
            Mock(status_code=200, json=lambda: {"default_branch": "main"}),
            # Tree SHA response (branch ref)
            Mock(status_code=200, json=lambda: {"object": {"sha": "commit123"}}),
            # Commit response
            Mock(status_code=200, json=lambda: {"tree": {"sha": "tree123"}}),
            # Tree response
            Mock(status_code=200, json=lambda: {
                "tree": [
                    {
                        "path": "train.py",
                        "type": "blob",
                        "size": 1500,
                        "sha": "abc123",
                        "url": "https://api.github.com/repos/owner/repo/git/blobs/abc123"
                    },
                    {
                        "path": "src",
                        "type": "tree",
                        "sha": "def456",
                        "url": "https://api.github.com/repos/owner/repo/git/trees/def456"
                    },
                    {
                        "path": "requirements.txt",
                        "type": "blob",
                        "size": 200,
                        "sha": "ghi789",
                        "url": "https://api.github.com/repos/owner/repo/git/blobs/ghi789"
                    }
                ],
                "truncated": False
            })
        ]
        mock_session.get.side_effect = mock_responses
        
        service = GitHubTreeService()
        tree = service.fetch_repository_tree("owner", "repo")
        
        assert tree.owner == "owner"
        assert tree.repo == "repo"
        assert tree.branch == "main"
        assert tree.total_files == 2
        assert tree.total_directories == 1
        assert len(tree.files) == 2
        assert len(tree.directories) == 1
        assert tree.truncated is False
        
        # Check important files
        assert len(tree.important_files["critical"]) == 1
        assert tree.important_files["critical"][0].name == "train.py"
        assert len(tree.important_files["high"]) == 1
        assert tree.important_files["high"][0].name == "requirements.txt"
    
    @patch('app.services.github_tree_service.requests.Session')
    def test_fetch_repository_tree_with_filtering(self, mock_session_class):
        """Test tree fetch with filtering applied."""
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        
        mock_responses = [
            Mock(status_code=200, json=lambda: {"default_branch": "main"}),
            Mock(status_code=200, json=lambda: {"object": {"sha": "commit123"}}),
            Mock(status_code=200, json=lambda: {"tree": {"sha": "tree123"}}),
            Mock(status_code=200, json=lambda: {
                "tree": [
                    {"path": "train.py", "type": "blob", "size": 1500},
                    {"path": "node_modules/package.json", "type": "blob", "size": 100},
                    {"path": "model.h5", "type": "blob", "size": 50000000},
                    {"path": "src/utils.py", "type": "blob", "size": 800}
                ],
                "truncated": False
            })
        ]
        mock_session.get.side_effect = mock_responses
        
        service = GitHubTreeService()
        tree = service.fetch_repository_tree("owner", "repo", include_filtered=False)
        
        # Should only include train.py and utils.py (filtered out node_modules and .h5)
        assert tree.filtered_files == 2
        assert tree.total_files == 3  # Excludes directories
    
    @patch('app.services.github_tree_service.requests.Session')
    def test_fetch_repository_tree_not_found(self, mock_session_class):
        """Test error handling when repository is not found."""
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        
        mock_responses = [
            Mock(status_code=200, json=lambda: {"default_branch": "main"}),
            Mock(status_code=200, json=lambda: {"object": {"sha": "commit123"}}),
            Mock(status_code=200, json=lambda: {"tree": {"sha": "tree123"}}),
            Mock(status_code=404, text="Not Found")
        ]
        mock_session.get.side_effect = mock_responses
        
        service = GitHubTreeService()
        
        with pytest.raises(GitHubTreeServiceError) as exc_info:
            service.fetch_repository_tree("owner", "repo")
        
        assert "not found" in str(exc_info.value).lower()


# Made with Bob