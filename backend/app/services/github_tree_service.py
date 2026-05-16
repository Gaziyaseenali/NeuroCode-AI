"""
Lightweight GitHub repository tree fetcher service.
Uses GitHub REST API to fetch recursive repository tree structure without cloning.
Optimized for low RAM usage and hackathon MVP simplicity.
"""
import requests
from typing import Optional, List, Dict, Set, Tuple
from app.models.github import (
    TreeNode,
    RepositoryTree,
    FileType,
    ImportanceLevel
)
from app.core.config import GITHUB_TOKEN


class GitHubTreeServiceError(Exception):
    """Base exception for GitHub tree service errors."""
    pass


class GitHubTreeService:
    """
    Service for fetching GitHub repository tree structure using REST API.
    
    Features:
    - Recursive tree fetching using Git Trees API
    - Lightweight filtering (node_modules, .git, binaries, etc.)
    - ML/medical AI file detection
    - Separate files and directories
    - Optimized for low RAM usage
    - No repository cloning required
    """
    
    BASE_URL = "https://api.github.com"
    
    # Directories to filter out (lightweight filtering)
    FILTERED_DIRS = {
        'node_modules', '.git', '__pycache__', '.pytest_cache',
        'venv', 'env', '.venv', 'virtualenv',
        '.cache', 'cache', 'tmp', 'temp',
        'dist', 'build', '.next', '.nuxt',
        'coverage', '.coverage', 'htmlcov',
        '.idea', '.vscode', '.vs',
        'logs', 'log'
    }
    
    # File patterns to filter out
    FILTERED_EXTENSIONS = {
        # Binaries and executables
        '.exe', '.dll', '.so', '.dylib', '.bin', '.dat',
        # Archives
        '.zip', '.tar', '.gz', '.rar', '.7z',
        # Images (large)
        '.psd', '.ai', '.sketch',
        # Videos
        '.mp4', '.avi', '.mov', '.wmv', '.flv',
        # Model weights and large ML files
        '.h5', '.hdf5', '.ckpt', '.pth', '.pt', '.pb',
        '.onnx', '.tflite', '.caffemodel', '.pkl', '.pickle',
        # Database files
        '.db', '.sqlite', '.sqlite3',
        # Lock files
        '.lock', 'package-lock.json', 'yarn.lock', 'poetry.lock'
    }
    
    # Critical ML/medical AI files (exact matches)
    CRITICAL_FILES = {
        'train.py', 'training.py', 'trainer.py',
        'infer.py', 'inference.py', 'predict.py', 'prediction.py',
        'model.py', 'models.py', 'network.py', 'architecture.py',
        'main.py', 'run.py', 'app.py'
    }
    
    # High importance files
    HIGH_IMPORTANCE_FILES = {
        'requirements.txt', 'environment.yml', 'conda.yml',
        'readme.md', 'readme.rst', 'readme',
        'dockerfile', 'docker-compose.yml',
        'setup.py', 'setup.cfg', 'pyproject.toml',
        'config.py', 'config.yaml', 'config.yml', 'config.json',
        'settings.py', 'settings.yaml', 'settings.yml'
    }
    
    # Medium importance patterns
    MEDIUM_IMPORTANCE_PATTERNS = {
        'notebook', 'ipynb',  # Jupyter notebooks
        'data', 'dataset', 'preprocess', 'preprocessing',
        'utils', 'util', 'helper', 'helpers',
        'loss', 'metric', 'metrics',
        'augment', 'augmentation',
        'transform', 'transforms'
    }
    
    def __init__(self, token: Optional[str] = None):
        """
        Initialize GitHub tree service.
        
        Args:
            token: Optional GitHub personal access token for higher rate limits
        """
        self.token = token or GITHUB_TOKEN
        self.session = requests.Session()
        
        # Set headers for API requests
        self.session.headers.update({
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "NeuroCode-AI-Tree-Fetcher"
        })
        
        # Add authentication if token is provided and not empty
        if self.token and self.token.strip():
            self.session.headers.update({
                "Authorization": f"token {self.token}"
            })
    
    def _should_filter_path(self, path: str, include_filtered: bool = False) -> bool:
        """
        Check if a path should be filtered out.
        
        Args:
            path: File or directory path
            include_filtered: If True, don't filter anything
            
        Returns:
            True if path should be filtered out
        """
        if include_filtered:
            return False
        
        # Check directory names
        path_parts = path.split('/')
        for part in path_parts:
            if part in self.FILTERED_DIRS:
                return True
        
        # Check file extensions
        for ext in self.FILTERED_EXTENSIONS:
            if path.lower().endswith(ext):
                return True
        
        return False
    
    def _detect_importance(self, path: str, name: str) -> ImportanceLevel:
        """
        Detect importance level of a file for ML/medical AI projects.
        
        Args:
            path: Full file path
            name: File name
            
        Returns:
            ImportanceLevel enum value
        """
        name_lower = name.lower()
        path_lower = path.lower()
        
        # Critical files (exact match)
        if name_lower in self.CRITICAL_FILES:
            return ImportanceLevel.CRITICAL
        
        # High importance files (exact match)
        if name_lower in self.HIGH_IMPORTANCE_FILES:
            return ImportanceLevel.HIGH
        
        # Medium importance (pattern matching)
        for pattern in self.MEDIUM_IMPORTANCE_PATTERNS:
            if pattern in name_lower or pattern in path_lower:
                return ImportanceLevel.MEDIUM
        
        # Low importance (tests, docs, examples)
        if any(x in path_lower for x in ['test', 'doc', 'example', 'demo']):
            return ImportanceLevel.LOW
        
        return ImportanceLevel.NONE
    
    def fetch_repository_tree(
        self,
        owner: str,
        repo: str,
        branch: Optional[str] = None,
        max_depth: Optional[int] = None,
        include_filtered: bool = False
    ) -> RepositoryTree:
        """
        Fetch complete repository tree structure using GitHub Git Trees API.
        
        This method uses the recursive tree API which is efficient and doesn't
        require multiple requests for nested directories.
        
        Args:
            owner: Repository owner username or organization
            repo: Repository name
            branch: Branch name (defaults to default branch)
            max_depth: Maximum depth to traverse (None for unlimited)
            include_filtered: Include filtered files/directories
            
        Returns:
            RepositoryTree object with structured tree data
            
        Raises:
            GitHubTreeServiceError: For API errors
        """
        # Get default branch if not specified
        if not branch:
            branch = self._get_default_branch(owner, repo)
        
        # Get the tree SHA for the branch
        tree_sha = self._get_tree_sha(owner, repo, branch)
        
        # Fetch recursive tree
        url = f"{self.BASE_URL}/repos/{owner}/{repo}/git/trees/{tree_sha}"
        params = {"recursive": "1"}  # Recursive fetch
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            
            if response.status_code == 404:
                raise GitHubTreeServiceError(
                    f"Repository '{owner}/{repo}' or branch '{branch}' not found"
                )
            
            if response.status_code != 200:
                raise GitHubTreeServiceError(
                    f"GitHub API error: {response.status_code} - {response.text}"
                )
            
            data = response.json()
            tree_items = data.get("tree", [])
            truncated = data.get("truncated", False)
            
            # Process tree items
            files: List[TreeNode] = []
            directories: List[TreeNode] = []
            important_files: Dict[str, List[TreeNode]] = {
                "critical": [],
                "high": [],
                "medium": [],
                "low": []
            }
            
            total_files = 0
            total_directories = 0
            
            for item in tree_items:
                path = item.get("path", "")
                item_type = item.get("type", "")
                
                # Count totals
                if item_type == "blob":
                    total_files += 1
                elif item_type == "tree":
                    total_directories += 1
                
                # Apply filtering
                if self._should_filter_path(path, include_filtered):
                    continue
                
                # Apply max depth filter
                if max_depth is not None:
                    depth = path.count('/')
                    if depth >= max_depth:
                        continue
                
                # Extract name from path
                name = path.split('/')[-1] if '/' in path else path
                
                # Determine file type
                file_type = FileType.FILE if item_type == "blob" else FileType.DIRECTORY
                
                # Detect importance (only for files)
                importance = ImportanceLevel.NONE
                if file_type == FileType.FILE:
                    importance = self._detect_importance(path, name)
                
                # Create tree node
                node = TreeNode(
                    path=path,
                    name=name,
                    type=file_type,
                    size=item.get("size"),
                    sha=item.get("sha"),
                    url=item.get("url"),
                    importance=importance
                )
                
                # Categorize
                if file_type == FileType.FILE:
                    files.append(node)
                    # Add to important files if applicable
                    if importance != ImportanceLevel.NONE:
                        important_files[importance.value].append(node)
                else:
                    directories.append(node)
            
            # Build response
            return RepositoryTree(
                owner=owner,
                repo=repo,
                branch=branch,
                total_files=total_files,
                total_directories=total_directories,
                filtered_files=len(files),
                filtered_directories=len(directories),
                files=files,
                directories=directories,
                important_files=important_files,
                truncated=truncated
            )
            
        except requests.exceptions.Timeout:
            raise GitHubTreeServiceError("Request to GitHub API timed out")
        except requests.exceptions.ConnectionError:
            raise GitHubTreeServiceError("Failed to connect to GitHub API")
        except requests.exceptions.RequestException as e:
            raise GitHubTreeServiceError(f"Request error: {str(e)}")
        except (KeyError, ValueError) as e:
            raise GitHubTreeServiceError(f"Failed to parse GitHub API response: {str(e)}")
    
    def _get_default_branch(self, owner: str, repo: str) -> str:
        """Get the default branch of a repository."""
        url = f"{self.BASE_URL}/repos/{owner}/{repo}"
        
        try:
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data.get("default_branch", "main")
            return "main"
        except Exception:
            return "main"
    
    def _get_tree_sha(self, owner: str, repo: str, branch: str) -> str:
        """Get the tree SHA for a specific branch."""
        url = f"{self.BASE_URL}/repos/{owner}/{repo}/git/ref/heads/{branch}"
        
        try:
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 404:
                raise GitHubTreeServiceError(
                    f"Branch '{branch}' not found in repository '{owner}/{repo}'"
                )
            
            if response.status_code != 200:
                raise GitHubTreeServiceError(
                    f"Failed to get branch info: {response.status_code}"
                )
            
            data = response.json()
            commit_sha = data["object"]["sha"]
            
            # Get commit to find tree SHA
            commit_url = f"{self.BASE_URL}/repos/{owner}/{repo}/git/commits/{commit_sha}"
            commit_response = self.session.get(commit_url, timeout=10)
            
            if commit_response.status_code != 200:
                raise GitHubTreeServiceError("Failed to get commit info")
            
            commit_data = commit_response.json()
            return commit_data["tree"]["sha"]
            
        except requests.exceptions.RequestException as e:
            raise GitHubTreeServiceError(f"Failed to get tree SHA: {str(e)}")
    
    def __del__(self):
        """Clean up session on deletion."""
        if hasattr(self, 'session'):
            self.session.close()


# Singleton instance for reuse across requests
_github_tree_service_instance: Optional[GitHubTreeService] = None


def get_github_tree_service() -> GitHubTreeService:
    """
    Get or create a singleton GitHubTreeService instance.
    Reuses HTTP session for better performance.
    
    Returns:
        GitHubTreeService instance
    """
    global _github_tree_service_instance
    if _github_tree_service_instance is None:
        _github_tree_service_instance = GitHubTreeService()
    return _github_tree_service_instance


# Made with Bob