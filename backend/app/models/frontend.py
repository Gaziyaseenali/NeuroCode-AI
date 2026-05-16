"""
Frontend-optimized response models for dynamic UI rendering.
Supports progressive loading states and cinematic repository analysis experience.
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime


class ProcessingStage(str, Enum):
    """Stages of repository analysis for progressive frontend updates."""
    PARSING = "parsing"
    FETCHING_METADATA = "fetching_metadata"
    ANALYZING_STRUCTURE = "analyzing_structure"
    DETECTING_FRAMEWORKS = "detecting_frameworks"
    GENERATING_INTELLIGENCE = "generating_intelligence"
    COMPLETE = "complete"


class LoadingState(str, Enum):
    """Loading state for API responses."""
    IDLE = "idle"
    LOADING = "loading"
    SUCCESS = "success"
    ERROR = "error"


class RepositoryMetadataCard(BaseModel):
    """Condensed metadata for frontend card display."""
    name: str = Field(..., description="Repository name")
    owner: str = Field(..., description="Repository owner")
    description: Optional[str] = Field(None, description="Short description")
    stars: int = Field(..., description="Star count")
    forks: int = Field(..., description="Fork count")
    language: Optional[str] = Field(None, description="Primary language")
    topics: List[str] = Field(default_factory=list, description="Repository topics")
    avatar_url: Optional[str] = Field(None, description="Owner avatar URL")
    html_url: str = Field(..., description="Repository URL")
    updated_at: str = Field(..., description="Last update")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "MONAI",
                "owner": "Project-MONAI",
                "description": "AI Toolkit for Healthcare Imaging",
                "stars": 5000,
                "forks": 800,
                "language": "Python",
                "topics": ["medical-imaging", "deep-learning"],
                "avatar_url": "https://avatars.githubusercontent.com/u/12345",
                "html_url": "https://github.com/Project-MONAI/MONAI",
                "updated_at": "2024-01-15T10:30:00Z"
            }
        }


class FrameworkVisualization(BaseModel):
    """Framework detection data optimized for visualization."""
    name: str = Field(..., description="Framework name")
    confidence: str = Field(..., description="Detection confidence")
    category: str = Field(..., description="Framework category (ml, medical, data)")
    icon: Optional[str] = Field(None, description="Icon identifier")
    color: Optional[str] = Field(None, description="Color for visualization")
    evidence_count: int = Field(..., description="Number of evidence files")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "PyTorch",
                "confidence": "high",
                "category": "ml",
                "icon": "pytorch",
                "color": "#EE4C2C",
                "evidence_count": 15
            }
        }


class WorkflowNode(BaseModel):
    """Workflow component for graph visualization."""
    id: str = Field(..., description="Unique node ID")
    label: str = Field(..., description="Display label")
    type: str = Field(..., description="Workflow type")
    confidence: str = Field(..., description="Detection confidence")
    files: List[str] = Field(default_factory=list, description="Related files")
    has_implementation: bool = Field(..., description="Whether implementation exists")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "training",
                "label": "Model Training",
                "type": "training",
                "confidence": "high",
                "files": ["train.py", "trainer.py"],
                "has_implementation": True
            }
        }


class MedicalAISignalCard(BaseModel):
    """Medical AI signal for visualization."""
    signal_type: str = Field(..., description="Signal type")
    confidence: str = Field(..., description="Detection confidence")
    description: str = Field(..., description="Human-readable description")
    evidence: List[str] = Field(default_factory=list, description="Evidence files")
    icon: Optional[str] = Field(None, description="Icon identifier")
    
    class Config:
        json_schema_extra = {
            "example": {
                "signal_type": "MRI Processing",
                "confidence": "high",
                "description": "Detected MRI image processing capabilities",
                "evidence": ["mri_preprocess.py", "nifti_loader.py"],
                "icon": "brain-scan"
            }
        }


class ImportantFileHighlight(BaseModel):
    """Important file with context for frontend display."""
    path: str = Field(..., description="File path")
    name: str = Field(..., description="File name")
    importance: str = Field(..., description="Importance level")
    category: str = Field(..., description="File category")
    description: str = Field(..., description="What this file does")
    size: Optional[int] = Field(None, description="File size in bytes")
    
    class Config:
        json_schema_extra = {
            "example": {
                "path": "src/train.py",
                "name": "train.py",
                "importance": "critical",
                "category": "training",
                "description": "Main training script for model training",
                "size": 15420
            }
        }


class ProcessingProgress(BaseModel):
    """Processing progress for loading states."""
    stage: ProcessingStage = Field(..., description="Current processing stage")
    progress: int = Field(..., description="Progress percentage (0-100)")
    message: str = Field(..., description="Human-readable status message")
    estimated_time_remaining: Optional[int] = Field(None, description="Estimated seconds remaining")
    
    class Config:
        json_schema_extra = {
            "example": {
                "stage": "analyzing_structure",
                "progress": 60,
                "message": "Analyzing repository structure...",
                "estimated_time_remaining": 5
            }
        }


class ReasoningStepCard(BaseModel):
    """AI reasoning step for frontend display."""
    category: str = Field(..., description="Reasoning category")
    title: str = Field(..., description="Step title")
    explanation: str = Field(..., description="Detailed explanation")
    evidence: List[str] = Field(default_factory=list, description="Supporting evidence")
    confidence_impact: str = Field(..., description="Confidence impact indicator")


class MaturityBadge(BaseModel):
    """Repository maturity badge for frontend."""
    level: str = Field(..., description="Maturity level")
    score: float = Field(..., description="Maturity score (0-100)")
    label: str = Field(..., description="Display label")
    color: str = Field(..., description="Badge color")
    description: str = Field(..., description="Level description")


class ArchitectureInsightCard(BaseModel):
    """Architecture insight card for frontend."""
    insight_type: str = Field(..., description="Insight type")
    title: str = Field(..., description="Insight title")
    description: str = Field(..., description="Detailed description")
    evidence: List[str] = Field(default_factory=list, description="Supporting evidence")
    significance: str = Field(..., description="Significance level")
    icon: Optional[str] = Field(None, description="Icon identifier")


class FrontendRepositoryIntelligence(BaseModel):
    """
    Frontend-optimized repository intelligence response.
    Structured for progressive loading and dynamic UI rendering.
    """
    # Loading state
    loading_state: LoadingState = Field(..., description="Current loading state")
    processing_progress: Optional[ProcessingProgress] = Field(None, description="Processing progress")
    
    # Basic info
    owner: str = Field(..., description="Repository owner")
    repo: str = Field(..., description="Repository name")
    branch: str = Field(..., description="Analyzed branch")
    
    # Metadata card (loads first)
    metadata_card: Optional[RepositoryMetadataCard] = Field(None, description="Repository metadata card")
    
    # Framework visualization (loads second)
    frameworks: List[FrameworkVisualization] = Field(
        default_factory=list,
        description="Detected frameworks for visualization"
    )
    
    # Workflow graph (loads third)
    workflow_nodes: List[WorkflowNode] = Field(
        default_factory=list,
        description="Workflow components for graph visualization"
    )
    
    # Medical AI signals (loads fourth)
    medical_signals: List[MedicalAISignalCard] = Field(
        default_factory=list,
        description="Medical AI signals for visualization"
    )
    
    # Important files (loads fifth)
    important_files: List[ImportantFileHighlight] = Field(
        default_factory=list,
        description="Important files with context"
    )
    
    # Classification summary
    classification: Dict[str, Any] = Field(
        default_factory=dict,
        description="Repository classification summary"
    )
    
    # Statistics
    statistics: Dict[str, Any] = Field(
        default_factory=dict,
        description="Repository statistics"
    )
    
    # Premium Intelligence Features
    ai_reasoning: Optional[Dict[str, Any]] = Field(
        None,
        description="AI reasoning explaining detections"
    )
    
    maturity_badge: Optional[MaturityBadge] = Field(
        None,
        description="Repository maturity assessment"
    )
    
    maturity_indicators: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Detailed maturity indicators"
    )
    
    architecture_insights: List[ArchitectureInsightCard] = Field(
        default_factory=list,
        description="Architecture insights and patterns"
    )
    
    executive_summary: Optional[Dict[str, Any]] = Field(
        None,
        description="Executive-style summary"
    )
    
    # LLM context (for future use)
    llm_summary: Optional[str] = Field(None, description="LLM-optimized summary")
    
    # Metadata
    analyzed_at: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat(),
        description="Analysis timestamp"
    )
    processing_time_ms: Optional[int] = Field(None, description="Total processing time in milliseconds")
    
    class Config:
        json_schema_extra = {
            "example": {
                "loading_state": "success",
                "processing_progress": {
                    "stage": "complete",
                    "progress": 100,
                    "message": "Analysis complete",
                    "estimated_time_remaining": 0
                },
                "owner": "Project-MONAI",
                "repo": "MONAI",
                "branch": "main",
                "metadata_card": {
                    "name": "MONAI",
                    "owner": "Project-MONAI",
                    "description": "AI Toolkit for Healthcare Imaging",
                    "stars": 5000,
                    "forks": 800,
                    "language": "Python",
                    "topics": ["medical-imaging", "deep-learning"],
                    "html_url": "https://github.com/Project-MONAI/MONAI",
                    "updated_at": "2024-01-15T10:30:00Z"
                },
                "frameworks": [
                    {
                        "name": "PyTorch",
                        "confidence": "high",
                        "category": "ml",
                        "icon": "pytorch",
                        "color": "#EE4C2C",
                        "evidence_count": 15
                    }
                ],
                "workflow_nodes": [
                    {
                        "id": "training",
                        "label": "Model Training",
                        "type": "training",
                        "confidence": "high",
                        "files": ["train.py"],
                        "has_implementation": True
                    }
                ],
                "medical_signals": [
                    {
                        "signal_type": "MRI Processing",
                        "confidence": "high",
                        "description": "Detected MRI image processing",
                        "evidence": ["mri_preprocess.py"],
                        "icon": "brain-scan"
                    }
                ],
                "important_files": [
                    {
                        "path": "train.py",
                        "name": "train.py",
                        "importance": "critical",
                        "category": "training",
                        "description": "Main training script",
                        "size": 15420
                    }
                ],
                "classification": {
                    "primary_type": "medical_imaging",
                    "confidence": "high"
                },
                "statistics": {
                    "total_files": 500,
                    "python_files": 150
                },
                "analyzed_at": "2024-01-15T10:30:00Z",
                "processing_time_ms": 3500
            }
        }


class ErrorDetail(BaseModel):
    """Detailed error information for frontend."""
    error_type: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    stage: Optional[ProcessingStage] = Field(None, description="Stage where error occurred")
    retry_possible: bool = Field(False, description="Whether retry is possible")
    suggestions: List[str] = Field(default_factory=list, description="Suggestions to fix")
    
    class Config:
        json_schema_extra = {
            "example": {
                "error_type": "RateLimitError",
                "message": "GitHub API rate limit exceeded",
                "stage": "fetching_metadata",
                "retry_possible": True,
                "suggestions": [
                    "Wait for rate limit to reset",
                    "Add GITHUB_TOKEN to environment variables"
                ]
            }
        }


class FrontendErrorResponse(BaseModel):
    """Frontend-friendly error response."""
    loading_state: LoadingState = Field(default=LoadingState.ERROR, description="Error state")
    error: ErrorDetail = Field(..., description="Error details")
    timestamp: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat(),
        description="Error timestamp"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "loading_state": "error",
                "error": {
                    "error_type": "RepositoryNotFound",
                    "message": "Repository not found or inaccessible",
                    "stage": "fetching_metadata",
                    "retry_possible": False,
                    "suggestions": ["Check repository URL", "Verify repository is public"]
                },
                "timestamp": "2024-01-15T10:30:00Z"
            }
        }


# Made with Bob