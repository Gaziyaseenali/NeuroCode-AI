"""
Pydantic models for GitHub URL parsing, repository metadata, and tree structure.
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum


class GitHubURLRequest(BaseModel):
    """Request model for GitHub URL parsing."""
    url: str = Field(..., description="GitHub repository URL to parse")
    
    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://github.com/owner/repo"
            }
        }


class GitHubRepoInfo(BaseModel):
    """Response model containing parsed GitHub repository information."""
    owner: str = Field(..., description="Repository owner/organization name")
    repo: str = Field(..., description="Repository name")
    url: str = Field(..., description="Original GitHub URL provided")
    
    class Config:
        json_schema_extra = {
            "example": {
                "owner": "octocat",
                "repo": "Hello-World",
                "url": "https://github.com/octocat/Hello-World"
            }
        }


class GitHubOwner(BaseModel):
    """GitHub repository owner information."""
    login: str = Field(..., description="Owner username or organization name")
    type: str = Field(..., description="Owner type (User or Organization)")
    avatar_url: Optional[str] = Field(None, description="Owner avatar URL")


class GitHubRepoMetadata(BaseModel):
    """Complete GitHub repository metadata from REST API."""
    name: str = Field(..., description="Repository name")
    full_name: str = Field(..., description="Full repository name (owner/repo)")
    description: Optional[str] = Field(None, description="Repository description")
    owner: GitHubOwner = Field(..., description="Repository owner information")
    stars: int = Field(..., description="Number of stars", alias="stargazers_count")
    forks: int = Field(..., description="Number of forks", alias="forks_count")
    watchers: int = Field(..., description="Number of watchers", alias="watchers_count")
    open_issues: int = Field(..., description="Number of open issues", alias="open_issues_count")
    primary_language: Optional[str] = Field(None, description="Primary programming language", alias="language")
    topics: List[str] = Field(default_factory=list, description="Repository topics/tags")
    default_branch: str = Field(..., description="Default branch name")
    created_at: str = Field(..., description="Repository creation timestamp")
    updated_at: str = Field(..., description="Last update timestamp")
    pushed_at: str = Field(..., description="Last push timestamp")
    size: int = Field(..., description="Repository size in KB")
    is_fork: bool = Field(..., description="Whether this is a fork", alias="fork")
    is_archived: bool = Field(..., description="Whether repository is archived", alias="archived")
    is_private: bool = Field(..., description="Whether repository is private", alias="private")
    html_url: str = Field(..., description="Repository web URL")
    clone_url: str = Field(..., description="HTTPS clone URL")
    ssh_url: str = Field(..., description="SSH clone URL")
    homepage: Optional[str] = Field(None, description="Project homepage URL")
    license: Optional[str] = Field(None, description="License name")
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "name": "Hello-World",
                "full_name": "octocat/Hello-World",
                "description": "My first repository on GitHub!",
                "owner": {
                    "login": "octocat",
                    "type": "User",
                    "avatar_url": "https://github.com/images/error/octocat_happy.gif"
                },
                "stars": 1500,
                "forks": 500,
                "watchers": 1500,
                "open_issues": 10,
                "primary_language": "Python",
                "topics": ["python", "fastapi", "api"],
                "default_branch": "main",
                "created_at": "2011-01-26T19:01:12Z",
                "updated_at": "2024-01-15T10:30:00Z",
                "pushed_at": "2024-01-15T10:30:00Z",
                "size": 180,
                "is_fork": False,
                "is_archived": False,
                "is_private": False,
                "html_url": "https://github.com/octocat/Hello-World",
                "clone_url": "https://github.com/octocat/Hello-World.git",
                "ssh_url": "git@github.com:octocat/Hello-World.git",
                "homepage": "https://example.com",
                "license": "MIT"
            }
        }


class ErrorResponse(BaseModel):
    """Error response model."""
    detail: str = Field(..., description="Error message describing what went wrong")
    error_type: Optional[str] = Field(None, description="Type of error")
    
    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Invalid GitHub URL format: URL must be a valid GitHub repository URL",
                "error_type": "ValidationError"
            }
        }

# Made with Bob



class FileType(str, Enum):
    """Enum for file types in repository tree."""
    FILE = "file"
    DIRECTORY = "directory"


class ImportanceLevel(str, Enum):
    """Importance level for ML/medical AI files."""
    CRITICAL = "critical"  # train.py, infer.py, main model files
    HIGH = "high"  # requirements.txt, README.md, configs
    MEDIUM = "medium"  # notebooks, utils, data processing
    LOW = "low"  # tests, docs, examples
    NONE = "none"  # other files


class TreeNode(BaseModel):
    """Represents a node in the repository tree structure."""
    path: str = Field(..., description="Full path of the file/directory")
    name: str = Field(..., description="Name of the file/directory")
    type: FileType = Field(..., description="Type: file or directory")
    size: Optional[int] = Field(None, description="Size in bytes (for files only)")
    sha: Optional[str] = Field(None, description="Git SHA hash")
    url: Optional[str] = Field(None, description="GitHub API URL for this item")
    importance: ImportanceLevel = Field(
        default=ImportanceLevel.NONE,
        description="Importance level for ML/medical AI projects"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "path": "src/train.py",
                "name": "train.py",
                "type": "file",
                "size": 15420,
                "sha": "abc123def456",
                "url": "https://api.github.com/repos/owner/repo/contents/src/train.py",
                "importance": "critical"
            }
        }


class RepositoryTree(BaseModel):
    """Complete repository tree structure with filtering applied."""
    owner: str = Field(..., description="Repository owner")
    repo: str = Field(..., description="Repository name")
    branch: str = Field(..., description="Branch name")
    total_files: int = Field(..., description="Total number of files")
    total_directories: int = Field(..., description="Total number of directories")
    filtered_files: int = Field(..., description="Number of files after filtering")
    filtered_directories: int = Field(..., description="Number of directories after filtering")
    files: List[TreeNode] = Field(default_factory=list, description="List of files")
    directories: List[TreeNode] = Field(default_factory=list, description="List of directories")
    important_files: Dict[str, List[TreeNode]] = Field(
        default_factory=dict,
        description="Important files grouped by importance level"
    )
    truncated: bool = Field(
        default=False,
        description="Whether the tree was truncated due to size limits"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "owner": "octocat",
                "repo": "medical-ai-project",
                "branch": "main",
                "total_files": 150,
                "total_directories": 25,
                "filtered_files": 120,
                "filtered_directories": 20,
                "files": [
                    {
                        "path": "train.py",
                        "name": "train.py",
                        "type": "file",
                        "size": 15420,
                        "importance": "critical"
                    }
                ],
                "directories": [
                    {
                        "path": "src",
                        "name": "src",
                        "type": "directory",
                        "importance": "none"
                    }
                ],
                "important_files": {
                    "critical": [],
                    "high": [],
                    "medium": []
                },
                "truncated": False
            }
        }


class TreeFetchRequest(BaseModel):
    """Request model for fetching repository tree."""
    url: str = Field(..., description="GitHub repository URL")
    branch: Optional[str] = Field(None, description="Branch name (defaults to default branch)")
    max_depth: Optional[int] = Field(None, description="Maximum depth to traverse (None for unlimited)")
    include_filtered: bool = Field(
        default=False,
        description="Include filtered files (node_modules, .git, etc.)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://github.com/owner/repo",
                "branch": "main",
                "max_depth": None,
                "include_filtered": False
            }
        }

