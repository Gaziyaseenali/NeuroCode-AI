"""
FastAPI routes for GitHub URL parsing, repository metadata, tree fetching, and analysis.
"""
from typing import Optional
from fastapi import APIRouter, HTTPException, status, Query
from app.models.github import (
    GitHubURLRequest,
    GitHubRepoInfo,
    GitHubRepoMetadata,
    ErrorResponse,
    TreeFetchRequest,
    RepositoryTree
)
from app.models.analyzer import (
    AnalyzerRequest,
    RepositoryIntelligence
)
from app.models.intelligence import (
    IntelligenceRequest,
    UnifiedRepositoryIntelligence
)
from app.utils.github_parser import parse_github_url, InvalidGitHubURLError
from app.services.github_service import (
    get_github_service,
    GitHubServiceError,
    RepositoryNotFoundError,
    RateLimitError
)
from app.services.github_tree_service import (
    get_github_tree_service,
    GitHubTreeServiceError
)
from app.services.repository_analyzer import get_repository_analyzer
from app.services.intelligence_service import (
    get_intelligence_service,
    IntelligenceServiceError
)


router = APIRouter(
    prefix="/api",
    tags=["GitHub"]
)


@router.post(
    "/parse-github-url",
    response_model=GitHubRepoInfo,
    status_code=status.HTTP_200_OK,
    responses={
        400: {
            "model": ErrorResponse,
            "description": "Invalid GitHub URL format"
        }
    },
    summary="Parse GitHub Repository URL",
    description="""
    Parse a GitHub repository URL and extract the owner and repository name.
    
    Supports the following URL formats:
    - https://github.com/owner/repo
    - https://github.com/owner/repo/
    - https://github.com/owner/repo.git
    - http://github.com/owner/repo
    - git@github.com:owner/repo.git
    
    Returns structured information about the repository including owner and repo name.
    """
)
async def parse_github_url_endpoint(request: GitHubURLRequest) -> GitHubRepoInfo:
    """
    Parse a GitHub repository URL.
    
    Args:
        request: GitHubURLRequest containing the URL to parse
        
    Returns:
        GitHubRepoInfo with owner, repo name, and original URL
        
    Raises:
        HTTPException: 400 error if URL is invalid
    """
    try:
        owner, repo = parse_github_url(request.url)
        return GitHubRepoInfo(
            owner=owner,
            repo=repo,
            url=request.url
        )
    except InvalidGitHubURLError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post(
    "/fetch-repo-metadata",
    response_model=GitHubRepoMetadata,
    status_code=status.HTTP_200_OK,
    responses={
        400: {
            "model": ErrorResponse,
            "description": "Invalid GitHub URL format"
        },
        404: {
            "model": ErrorResponse,
            "description": "Repository not found or inaccessible"
        },
        429: {
            "model": ErrorResponse,
            "description": "GitHub API rate limit exceeded"
        },
        500: {
            "model": ErrorResponse,
            "description": "Internal server error or GitHub API error"
        }
    },
    summary="Fetch GitHub Repository Metadata",
    description="""
    Fetch complete repository metadata from GitHub REST API without cloning.
    
    This endpoint:
    - Parses the GitHub URL to extract owner and repo name
    - Fetches comprehensive metadata using GitHub REST API v3
    - Returns structured data including stars, language, topics, and more
    - Does NOT clone the repository (lightweight and fast)
    - Optimized for low RAM usage
    
    Supports the same URL formats as the parse endpoint.
    
    **Rate Limits:**
    - Without authentication: 60 requests/hour
    - With GitHub token: 5000 requests/hour
    
    Set GITHUB_TOKEN environment variable for higher limits.
    """
)
async def fetch_repo_metadata_endpoint(request: GitHubURLRequest) -> GitHubRepoMetadata:
    """
    Fetch complete GitHub repository metadata.
    
    Args:
        request: GitHubURLRequest containing the repository URL
        
    Returns:
        GitHubRepoMetadata with complete repository information
        
    Raises:
        HTTPException: Various status codes for different error conditions
    """
    try:
        # Parse URL to get owner and repo
        owner, repo = parse_github_url(request.url)
        
        # Fetch metadata from GitHub API
        github_service = get_github_service()
        metadata = github_service.fetch_repository_metadata(owner, repo)
        
        return metadata
        
    except InvalidGitHubURLError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except RepositoryNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except RateLimitError as e:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=str(e)
        )
    except GitHubServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"GitHub API error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )


@router.get(
    "/repo-metadata/{owner}/{repo}",
    response_model=GitHubRepoMetadata,
    status_code=status.HTTP_200_OK,
    responses={
        404: {
            "model": ErrorResponse,
            "description": "Repository not found or inaccessible"
        },
        429: {
            "model": ErrorResponse,
            "description": "GitHub API rate limit exceeded"
        },
        500: {
            "model": ErrorResponse,
            "description": "Internal server error or GitHub API error"
        }
    },
    summary="Fetch Repository Metadata by Owner and Repo Name",
    description="""
    Fetch repository metadata directly using owner and repository name.
    
    This is a convenience endpoint that doesn't require URL parsing.
    Useful when you already know the owner and repo name.
    
    **Rate Limits:**
    - Without authentication: 60 requests/hour
    - With GitHub token: 5000 requests/hour
    """
)
async def get_repo_metadata_endpoint(
    owner: str, #Query(..., description="Repository owner username or organization"),
    repo: str# Query(..., description="Repository name")
) -> GitHubRepoMetadata:
    """
    Fetch repository metadata by owner and repo name.
    
    Args:
        owner: Repository owner username or organization name
        repo: Repository name
        
    Returns:
        GitHubRepoMetadata with complete repository information
        
    Raises:
        HTTPException: Various status codes for different error conditions
    """
    try:
        github_service = get_github_service()
        metadata = github_service.fetch_repository_metadata(owner, repo)
        return metadata
        
    except RepositoryNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except RateLimitError as e:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=str(e)
        )
    except GitHubServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"GitHub API error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )


@router.get(
    "/rate-limit",
    summary="Get GitHub API Rate Limit Information",
    description="""
    Check current GitHub API rate limit status.
    
    Returns information about:
    - Maximum requests per hour
    - Remaining requests
    - When the limit resets
    - Number of requests used
    
    Useful for monitoring API usage and avoiding rate limit errors.
    """
)
async def get_rate_limit_endpoint():
    """
    Get GitHub API rate limit information.
    
    Returns:
        Dictionary with rate limit details
    """
    try:
        github_service = get_github_service()
        rate_limit_info = github_service.get_rate_limit_info()
        return {
            "status": "success",
            "rate_limit": rate_limit_info
        }
    except Exception as e:
        return {
            "status": "error",
            "detail": str(e)
        }

# Made with Bob



@router.post(
    "/fetch-repo-tree",
    response_model=RepositoryTree,
    status_code=status.HTTP_200_OK,
    responses={
        400: {
            "model": ErrorResponse,
            "description": "Invalid GitHub URL format"
        },
        404: {
            "model": ErrorResponse,
            "description": "Repository or branch not found"
        },
        429: {
            "model": ErrorResponse,
            "description": "GitHub API rate limit exceeded"
        },
        500: {
            "model": ErrorResponse,
            "description": "Internal server error or GitHub API error"
        }
    },
    summary="Fetch GitHub Repository Tree Structure",
    description="""
    Fetch complete repository tree structure using GitHub REST API without cloning.
    
    This endpoint:
    - Uses GitHub Git Trees API for efficient recursive fetching
    - Filters out node_modules, .git, binaries, model weights, and cache folders
    - Detects important ML/medical AI files (train.py, infer.py, configs, etc.)
    - Separates files and directories
    - Groups important files by importance level (critical, high, medium, low)
    - Optimized for low RAM usage and large repositories
    - Does NOT clone the repository
    
    **Filtering:**
    - Automatically filters: node_modules, .git, __pycache__, venv, cache, build, dist
    - Filters binary files: .exe, .dll, .so, .zip, .tar
    - Filters model weights: .h5, .pth, .ckpt, .pb, .onnx
    - Set `include_filtered: true` to disable filtering
    
    **ML/Medical AI File Detection:**
    - Critical: train.py, infer.py, model.py, main.py
    - High: requirements.txt, README.md, config files, Dockerfile
    - Medium: notebooks, data processing, utils, metrics
    - Low: tests, docs, examples
    
    **Rate Limits:**
    - Without authentication: 60 requests/hour
    - With GitHub token: 5000 requests/hour
    """
)
async def fetch_repo_tree_endpoint(request: TreeFetchRequest) -> RepositoryTree:
    """
    Fetch complete repository tree structure.
    
    Args:
        request: TreeFetchRequest containing URL, branch, and options
        
    Returns:
        RepositoryTree with complete tree structure and metadata
        
    Raises:
        HTTPException: Various status codes for different error conditions
    """
    try:
        # Parse URL to get owner and repo
        owner, repo = parse_github_url(request.url)
        
        # Fetch tree from GitHub API
        tree_service = get_github_tree_service()
        tree = tree_service.fetch_repository_tree(
            owner=owner,
            repo=repo,
            branch=request.branch,
            max_depth=request.max_depth,
            include_filtered=request.include_filtered
        )
        
        return tree
        
    except InvalidGitHubURLError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except GitHubTreeServiceError as e:
        error_msg = str(e)
        if "not found" in error_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_msg
            )
        elif "rate limit" in error_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=error_msg
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"GitHub API error: {error_msg}"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )


@router.get(
    "/repo-tree/{owner}/{repo}",
    response_model=RepositoryTree,
    status_code=status.HTTP_200_OK,
    responses={
        404: {
            "model": ErrorResponse,
            "description": "Repository or branch not found"
        },
        429: {
            "model": ErrorResponse,
            "description": "GitHub API rate limit exceeded"
        },
        500: {
            "model": ErrorResponse,
            "description": "Internal server error or GitHub API error"
        }
    },
    summary="Fetch Repository Tree by Owner and Repo Name",
    description="""
    Fetch repository tree structure directly using owner and repository name.
    
    This is a convenience endpoint that doesn't require URL parsing.
    Supports all the same features as the POST endpoint.
    """
)
async def get_repo_tree_endpoint(
    owner: str, # Query(..., description="Repository owner username or organization"),
    repo: str,# Query(..., description="Repository name"),
    branch: Optional[str] = Query(None, description="Branch name (defaults to default branch)"),
    max_depth: Optional[int] = Query(None, description="Maximum depth to traverse"),
    include_filtered: bool = Query(False, description="Include filtered files/directories")
) -> RepositoryTree:
    """
    Fetch repository tree by owner and repo name.
    
    Args:
        owner: Repository owner username or organization name
        repo: Repository name
        branch: Optional branch name
        max_depth: Optional maximum depth
        include_filtered: Whether to include filtered files
        
    Returns:
        RepositoryTree with complete tree structure
        
    Raises:
        HTTPException: Various status codes for different error conditions
    """
    try:
        tree_service = get_github_tree_service()
        tree = tree_service.fetch_repository_tree(
            owner=owner,
            repo=repo,
            branch=branch,
            max_depth=max_depth,
            include_filtered=include_filtered
        )
        return tree
        
    except GitHubTreeServiceError as e:
        error_msg = str(e)
        if "not found" in error_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_msg
            )
        elif "rate limit" in error_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=error_msg
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"GitHub API error: {error_msg}"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )




@router.post(
    "/analyze-repository",
    response_model=RepositoryIntelligence,
    status_code=status.HTTP_200_OK,
    responses={
        400: {
            "model": ErrorResponse,
            "description": "Invalid GitHub URL format"
        },
        404: {
            "model": ErrorResponse,
            "description": "Repository or branch not found"
        },
        429: {
            "model": ErrorResponse,
            "description": "GitHub API rate limit exceeded"
        },
        500: {
            "model": ErrorResponse,
            "description": "Internal server error or GitHub API error"
        }
    },
    summary="Analyze GitHub Repository Structure",
    description="""
    Analyze repository structure and generate intelligence report.
    
    This endpoint:
    - Fetches repository tree structure using GitHub API
    - Analyzes file paths and names using rule-based detection
    - Detects repository type (ML, medical imaging, segmentation, research, inference)
    - Identifies workflow components (preprocessing, training, inference, evaluation, deployment)
    - Detects AI/ML frameworks (PyTorch, TensorFlow, MONAI, SimpleITK, nibabel, etc.)
    - Identifies medical AI signals (segmentation, MRI, CT, DICOM, volumetric processing)
    - Extracts key files and statistics
    - Generates human-readable summary
    
    **Analysis Features:**
    - Lightweight rule-based analysis (no embeddings or vector databases)
    - Optimized for low RAM usage
    - Fast analysis without file content reading
    - Explainable detection with evidence
    - Confidence levels for all detections
    
    **Repository Types Detected:**
    - Machine Learning: General ML projects with PyTorch/TensorFlow
    - Medical Imaging: Projects using MONAI, SimpleITK, medical data
    - Segmentation: Image/medical segmentation projects
    - Research: Projects with notebooks and papers
    - Inference: Deployment-focused projects without training
    
    **Frameworks Detected:**
    - PyTorch, TensorFlow, Keras
    - MONAI (medical imaging)
    - SimpleITK, nibabel (medical data processing)
    - scikit-learn, OpenCV
    
    **Medical AI Signals:**
    - Segmentation tasks
    - MRI, CT imaging
    - DICOM format
    - NIfTI format
    - Volumetric/3D processing
    
    **Rate Limits:**
    - Without authentication: 60 requests/hour
    - With GitHub token: 5000 requests/hour
    """
)
async def analyze_repository_endpoint(request: AnalyzerRequest) -> RepositoryIntelligence:
    """
    Analyze repository structure and generate intelligence.
    
    Args:
        request: AnalyzerRequest containing URL and optional branch
        
    Returns:
        RepositoryIntelligence with complete analysis
        
    Raises:
        HTTPException: Various status codes for different error conditions
    """
    try:
        # Parse URL to get owner and repo
        owner, repo = parse_github_url(request.url)
        
        # Fetch tree from GitHub API
        tree_service = get_github_tree_service()
        tree = tree_service.fetch_repository_tree(
            owner=owner,
            repo=repo,
            branch=request.branch,
            max_depth=None,
            include_filtered=False
        )
        
        # Analyze tree structure
        analyzer = get_repository_analyzer()
        intelligence = analyzer.analyze(tree)
        
        return intelligence
        
    except InvalidGitHubURLError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except GitHubTreeServiceError as e:
        error_msg = str(e)
        if "not found" in error_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_msg
            )
        elif "rate limit" in error_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=error_msg
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"GitHub API error: {error_msg}"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )


@router.get(
    "/analyze-repository/{owner}/{repo}",
    response_model=RepositoryIntelligence,
    status_code=status.HTTP_200_OK,
    responses={
        404: {
            "model": ErrorResponse,
            "description": "Repository or branch not found"
        },
        429: {
            "model": ErrorResponse,
            "description": "GitHub API rate limit exceeded"
        },
        500: {
            "model": ErrorResponse,
            "description": "Internal server error or GitHub API error"
        }
    },
    summary="Analyze Repository by Owner and Repo Name",
    description="""
    Analyze repository structure directly using owner and repository name.
    
    This is a convenience endpoint that doesn't require URL parsing.
    Supports all the same analysis features as the POST endpoint.
    """
)
async def get_analyze_repository_endpoint(
    owner: str, #= Query(..., description="Repository owner username or organization"),
    repo: str, # = Query(..., description="Repository name"),
    branch: Optional[str] = Query(None, description="Branch name (defaults to default branch)")
) -> RepositoryIntelligence:
    """
    Analyze repository by owner and repo name.
    
    Args:
        owner: Repository owner username or organization name
        repo: Repository name
        branch: Optional branch name
        
    Returns:
        RepositoryIntelligence with complete analysis
        
    Raises:
        HTTPException: Various status codes for different error conditions
    """
    try:
        # Fetch tree from GitHub API
        tree_service = get_github_tree_service()
        tree = tree_service.fetch_repository_tree(
            owner=owner,
            repo=repo,
            branch=branch,
            max_depth=None,
            include_filtered=False
        )
        
        # Analyze tree structure
        analyzer = get_repository_analyzer()
        intelligence = analyzer.analyze(tree)
        
        return intelligence
        
    except GitHubTreeServiceError as e:
        error_msg = str(e)
        if "not found" in error_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_msg
            )
        elif "rate limit" in error_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=error_msg
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"GitHub API error: {error_msg}"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )


@router.post(
    "/repository-intelligence",
    response_model=UnifiedRepositoryIntelligence,
    status_code=status.HTTP_200_OK,
    responses={
        400: {
            "model": ErrorResponse,
            "description": "Invalid GitHub URL format"
        },
        404: {
            "model": ErrorResponse,
            "description": "Repository or branch not found"
        },
        429: {
            "model": ErrorResponse,
            "description": "GitHub API rate limit exceeded"
        },
        500: {
            "model": ErrorResponse,
            "description": "Internal server error or GitHub API error"
        }
    },
    summary="Get Unified Repository Intelligence",
    description="""
    Get complete unified repository intelligence by orchestrating all analysis services.
    
    This endpoint combines:
    - **Repository Metadata**: Stars, forks, language, topics, license, etc.
    - **Repository Tree Structure**: Files, directories, important files
    - **Repository Analysis**: Type detection, frameworks, workflows, medical AI signals
    
    **Output includes:**
    - Metadata summary (condensed repository info)
    - Structure summary (file counts, important files)
    - Classification (primary and secondary types with confidence)
    - Workflow summary (training, inference, preprocessing, etc.)
    - Technology stack (detected frameworks)
    - Medical AI context (modalities, tasks, signals)
    - Project statistics (Python files, notebooks, configs)
    - LLM-optimized context summary (for future LLM usage)
    
    **Features:**
    - Lightweight orchestration (no embeddings or vector databases)
    - Optimized for low RAM usage
    - Fast analysis without cloning repository
    - Structured output ready for LLM consumption
    - Explainable detections with evidence
    
    **Use Cases:**
    - Repository understanding and exploration
    - Project classification and categorization
    - Technology stack detection
    - Medical AI project identification
    - LLM context preparation
    - Repository recommendation systems
    
    **Rate Limits:**
    - Without authentication: 60 requests/hour
    - With GitHub token: 5000 requests/hour
    """
)
async def get_repository_intelligence_endpoint(
    request: IntelligenceRequest
) -> UnifiedRepositoryIntelligence:
    """
    Get unified repository intelligence.
    
    Args:
        request: IntelligenceRequest containing URL and options
        
    Returns:
        UnifiedRepositoryIntelligence with complete analysis
        
    Raises:
        HTTPException: Various status codes for different error conditions
    """
    try:
        # Get intelligence service and analyze
        intelligence_service = get_intelligence_service()
        intelligence = intelligence_service.analyze_repository(
            url=request.url,
            branch=request.branch,
            include_filtered=request.include_filtered,
            max_depth=request.max_depth
        )
        
        return intelligence
        
    except InvalidGitHubURLError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except IntelligenceServiceError as e:
        error_msg = str(e)
        if "not found" in error_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_msg
            )
        elif "rate limit" in error_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=error_msg
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Intelligence service error: {error_msg}"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )


@router.get(
    "/repository-intelligence/{owner}/{repo}",
    response_model=UnifiedRepositoryIntelligence,
    status_code=status.HTTP_200_OK,
    responses={
        404: {
            "model": ErrorResponse,
            "description": "Repository or branch not found"
        },
        429: {
            "model": ErrorResponse,
            "description": "GitHub API rate limit exceeded"
        },
        500: {
            "model": ErrorResponse,
            "description": "Internal server error or GitHub API error"
        }
    },
    summary="Get Repository Intelligence by Owner and Repo Name",
    description="""
    Get unified repository intelligence directly using owner and repository name.
    
    This is a convenience endpoint that doesn't require URL parsing.
    Supports all the same intelligence features as the POST endpoint.
    """
)
async def get_repository_intelligence_by_name_endpoint(
    owner: str, # = Query(..., description="Repository owner username or organization"),
    repo: str, # = Query(..., description="Repository name"),
    branch: Optional[str] = Query(None, description="Branch name (defaults to default branch)"),
    include_filtered: bool = Query(False, description="Include filtered files in tree"),
    max_depth: Optional[int] = Query(None, description="Maximum tree depth")
) -> UnifiedRepositoryIntelligence:
    """
    Get repository intelligence by owner and repo name.
    
    Args:
        owner: Repository owner username or organization name
        repo: Repository name
        branch: Optional branch name
        include_filtered: Whether to include filtered files
        max_depth: Optional maximum depth
        
    Returns:
        UnifiedRepositoryIntelligence with complete analysis
        
    Raises:
        HTTPException: Various status codes for different error conditions
    """
    try:
        # Construct URL for the service
        url = f"https://github.com/{owner}/{repo}"
        
        # Get intelligence service and analyze
        intelligence_service = get_intelligence_service()
        intelligence = intelligence_service.analyze_repository(
            url=url,
            branch=branch,
            include_filtered=include_filtered,
            max_depth=max_depth
        )
        
        return intelligence
        
    except IntelligenceServiceError as e:
        error_msg = str(e)
        if "not found" in error_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_msg
            )
        elif "rate limit" in error_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=error_msg
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Intelligence service error: {error_msg}"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )
