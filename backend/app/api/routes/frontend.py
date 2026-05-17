"""
Frontend-optimized API routes for dynamic UI rendering.
Supports progressive loading and cinematic repository analysis experience.
"""
from typing import Optional
from fastapi import APIRouter, HTTPException, status, Query
from app.models.frontend import (
    FrontendRepositoryIntelligence,
    FrontendErrorResponse,
    ErrorDetail,
    LoadingState,
    ProcessingStage
)
from app.models.intelligence import IntelligenceRequest
from app.services.intelligence_service import (
    get_intelligence_service,
    IntelligenceServiceError
)
from app.services.frontend_transformer import get_frontend_transformer
from app.utils.github_parser import InvalidGitHubURLError
import time


router = APIRouter(
    prefix="/api/frontend",
    tags=["Frontend"]
)


@router.post(
    "/repository-intelligence",
    response_model=FrontendRepositoryIntelligence,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": FrontendErrorResponse, "description": "Invalid request"},
        404: {"model": FrontendErrorResponse, "description": "Repository not found"},
        429: {"model": FrontendErrorResponse, "description": "Rate limit exceeded"},
        500: {"model": FrontendErrorResponse, "description": "Internal server error"}
    },
    summary="Get Frontend-Optimized Repository Intelligence",
    description="""
    Get repository intelligence optimized for dynamic frontend rendering.
    
    **Features:**
    - Progressive loading support with stage indicators
    - Frontend-friendly data structures
    - Optimized for card-based UI components
    - Framework visualization data
    - Workflow graph nodes
    - Medical AI signal cards
    - Important file highlights with context
    
    **Response Structure:**
    - `metadata_card`: Repository metadata for card display
    - `frameworks`: Framework detections with visualization metadata
    - `workflow_nodes`: Workflow components for graph rendering
    - `medical_signals`: Medical AI signals with descriptions
    - `important_files`: Key files with categories and descriptions
    - `classification`: Repository type classification
    - `statistics`: Project statistics
    
    **Loading States:**
    - `idle`: Not started
    - `loading`: In progress
    - `success`: Completed successfully
    - `error`: Failed with error details
    
    **Processing Stages:**
    1. `parsing`: Parsing repository URL
    2. `fetching_metadata`: Fetching repository metadata
    3. `analyzing_structure`: Analyzing file structure
    4. `detecting_frameworks`: Detecting frameworks and tools
    5. `generating_intelligence`: Generating final intelligence
    6. `complete`: Analysis complete
    
    **Use Cases:**
    - Dynamic repository exploration UI
    - Progressive loading experience
    - Cinematic analysis visualization
    - Repository dashboard cards
    - Technology stack visualization
    - Workflow graph rendering
    """
)
async def get_frontend_repository_intelligence(
    request: IntelligenceRequest
) -> FrontendRepositoryIntelligence:
    """
    Get frontend-optimized repository intelligence.
    
    Args:
        request: Intelligence request with URL and options
        
    Returns:
        Frontend-optimized intelligence response
        
    Raises:
        HTTPException: Various status codes with frontend-friendly errors
    """
    start_time = time.time()
    
    try:
        # Get intelligence service and analyze
        intelligence_service = get_intelligence_service()
        intelligence = intelligence_service.analyze_repository(
            url=request.url,
            branch=request.branch,
            include_filtered=request.include_filtered,
            max_depth=request.max_depth
        )
        
        # Calculate processing time
        processing_time_ms = int((time.time() - start_time) * 1000)
        
        # Transform to frontend format
        transformer = get_frontend_transformer()
        frontend_intelligence = transformer.transform_to_frontend(
            intelligence=intelligence,
            processing_time_ms=processing_time_ms
        )
        
        return frontend_intelligence
        
    except InvalidGitHubURLError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=FrontendErrorResponse(
                loading_state=LoadingState.ERROR,
                error=ErrorDetail(
                    error_type="InvalidGitHubURL",
                    message=str(e),
                    stage=ProcessingStage.PARSING,
                    retry_possible=False,
                    suggestions=[
                        "Check the GitHub URL format",
                        "Ensure URL is a valid GitHub repository URL",
                        "Example: https://github.com/owner/repo"
                    ]
                )
            ).model_dump()
        )
    except IntelligenceServiceError as e:
        error_msg = str(e).lower()
        
        if "not found" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=FrontendErrorResponse(
                    loading_state=LoadingState.ERROR,
                    error=ErrorDetail(
                        error_type="RepositoryNotFound",
                        message=str(e),
                        stage=ProcessingStage.FETCHING_METADATA,
                        retry_possible=False,
                        suggestions=[
                            "Verify the repository exists",
                            "Check if repository is public",
                            "Ensure correct owner and repo name"
                        ]
                    )
                ).model_dump()
            )
        elif "rate limit" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=FrontendErrorResponse(
                    loading_state=LoadingState.ERROR,
                    error=ErrorDetail(
                        error_type="RateLimitExceeded",
                        message=str(e),
                        stage=ProcessingStage.FETCHING_METADATA,
                        retry_possible=True,
                        suggestions=[
                            "Wait for rate limit to reset",
                            "Add GITHUB_TOKEN environment variable",
                            "Try again in a few minutes"
                        ]
                    )
                ).model_dump()
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=FrontendErrorResponse(
                    loading_state=LoadingState.ERROR,
                    error=ErrorDetail(
                        error_type="IntelligenceServiceError",
                        message=str(e),
                        stage=ProcessingStage.GENERATING_INTELLIGENCE,
                        retry_possible=True,
                        suggestions=[
                            "Try again in a moment",
                            "Check server logs for details",
                            "Contact support if issue persists"
                        ]
                    )
                ).model_dump()
            )
    except Exception as e:
        import traceback
        print("Error:", str(e))
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=FrontendErrorResponse(
                loading_state=LoadingState.ERROR,
                error=ErrorDetail(
                    error_type="UnexpectedError",
                    message=f"Unexpected error: {str(e)}",
                    stage=None,
                    retry_possible=True,
                    suggestions=[
                        "Try again in a moment",
                        "Check if the repository is accessible",
                        "Contact support if issue persists"
                    ]
                )
            ).model_dump()
        )


@router.get(
    "/repository-intelligence/{owner}/{repo}",
    response_model=FrontendRepositoryIntelligence,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"model": FrontendErrorResponse, "description": "Repository not found"},
        429: {"model": FrontendErrorResponse, "description": "Rate limit exceeded"},
        500: {"model": FrontendErrorResponse, "description": "Internal server error"}
    },
    summary="Get Frontend Intelligence by Owner and Repo",
    description="""
    Get frontend-optimized repository intelligence using owner and repo name.
    
    This is a convenience endpoint that doesn't require URL parsing.
    Supports all the same features as the POST endpoint.
    """
)
async def get_frontend_intelligence_by_name(
    owner: str, # = Query(..., description="Repository owner username or organization"),
    repo: str, # = Query(..., description="Repository name"),
    branch: Optional[str] = Query(None, description="Branch name (defaults to default branch)"),
    include_filtered: bool = Query(False, description="Include filtered files"),
    max_depth: Optional[int] = Query(None, description="Maximum tree depth")
) -> FrontendRepositoryIntelligence:
    """
    Get frontend intelligence by owner and repo name.
    
    Args:
        owner: Repository owner
        repo: Repository name
        branch: Optional branch name
        include_filtered: Include filtered files
        max_depth: Maximum tree depth
        
    Returns:
        Frontend-optimized intelligence response
    """
    # Construct URL and use the POST endpoint logic
    url = f"https://github.com/{owner}/{repo}"
    request = IntelligenceRequest(
        url=url,
        branch=branch,
        include_filtered=include_filtered,
        max_depth=max_depth
    )
    return await get_frontend_repository_intelligence(request)


# Made with Bob