"""
Pydantic models for unified repository intelligence aggregation.
Combines metadata, tree structure, and analysis into a single comprehensive output.
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime
from app.models.github import GitHubRepoMetadata, TreeNode
from app.models.analyzer import (
    RepositoryTypeDetection,
    WorkflowDetection,
    FrameworkDetection,
    MedicalSignalDetection
)


class RepositoryMetadataSummary(BaseModel):
    """Condensed repository metadata for intelligence output."""
    name: str = Field(..., description="Repository name")
    full_name: str = Field(..., description="Full repository name (owner/repo)")
    description: Optional[str] = Field(None, description="Repository description")
    stars: int = Field(..., description="Number of stars")
    forks: int = Field(..., description="Number of forks")
    primary_language: Optional[str] = Field(None, description="Primary programming language")
    topics: List[str] = Field(default_factory=list, description="Repository topics")
    created_at: str = Field(..., description="Creation timestamp")
    updated_at: str = Field(..., description="Last update timestamp")
    size: int = Field(..., description="Repository size in KB")
    license: Optional[str] = Field(None, description="License name")
    html_url: str = Field(..., description="Repository web URL")


class RepositoryStructureSummary(BaseModel):
    """Condensed repository structure summary."""
    total_files: int = Field(..., description="Total number of files")
    total_directories: int = Field(..., description="Total number of directories")
    filtered_files: int = Field(..., description="Number of files after filtering")
    filtered_directories: int = Field(..., description="Number of directories after filtering")
    important_files_count: Dict[str, int] = Field(
        default_factory=dict,
        description="Count of important files by level"
    )
    critical_files: List[TreeNode] = Field(
        default_factory=list,
        description="Critical files (train.py, infer.py, etc.)"
    )
    high_importance_files: List[TreeNode] = Field(
        default_factory=list,
        description="High importance files (requirements.txt, README, etc.)"
    )


class RepositoryClassification(BaseModel):
    """Repository classification and categorization."""
    primary_type: str = Field(..., description="Primary repository type")
    secondary_types: List[str] = Field(
        default_factory=list,
        description="Additional repository types"
    )
    confidence: str = Field(..., description="Overall classification confidence")
    all_detections: List[RepositoryTypeDetection] = Field(
        default_factory=list,
        description="All type detections with evidence"
    )


class WorkflowSummary(BaseModel):
    """Summary of detected workflow components."""
    has_training: bool = Field(False, description="Has training workflow")
    has_inference: bool = Field(False, description="Has inference workflow")
    has_preprocessing: bool = Field(False, description="Has preprocessing workflow")
    has_evaluation: bool = Field(False, description="Has evaluation workflow")
    has_deployment: bool = Field(False, description="Has deployment workflow")
    components: List[WorkflowDetection] = Field(
        default_factory=list,
        description="Detailed workflow component detections"
    )


class TechnologyStack(BaseModel):
    """Detected technology stack and frameworks."""
    primary_frameworks: List[str] = Field(
        default_factory=list,
        description="Primary AI/ML frameworks"
    )
    all_frameworks: List[FrameworkDetection] = Field(
        default_factory=list,
        description="All detected frameworks with evidence"
    )
    medical_frameworks: List[str] = Field(
        default_factory=list,
        description="Medical imaging specific frameworks"
    )


class MedicalAIContext(BaseModel):
    """Medical AI specific context and signals."""
    is_medical_ai: bool = Field(False, description="Whether this is a medical AI repository")
    confidence: str = Field("none", description="Confidence level for medical AI classification")
    detected_signals: List[MedicalSignalDetection] = Field(
        default_factory=list,
        description="Detected medical AI signals"
    )
    modalities: List[str] = Field(
        default_factory=list,
        description="Detected medical imaging modalities (MRI, CT, etc.)"
    )
    tasks: List[str] = Field(
        default_factory=list,
        description="Detected medical AI tasks (segmentation, classification, etc.)"
    )


class ProjectStatistics(BaseModel):
    """Repository project statistics."""
    total_python_files: int = Field(0, description="Total Python files")
    total_notebook_files: int = Field(0, description="Total Jupyter notebooks")
    total_config_files: int = Field(0, description="Total configuration files")
    has_requirements: bool = Field(False, description="Has requirements.txt")
    has_dockerfile: bool = Field(False, description="Has Dockerfile")
    has_readme: bool = Field(False, description="Has README")
    has_tests: bool = Field(False, description="Has test files")
    has_ci_cd: bool = Field(False, description="Has CI/CD configuration")


class LLMContextSummary(BaseModel):
    """Structured summary optimized for LLM context usage."""
    repository_overview: str = Field(..., description="High-level repository overview")
    technical_summary: str = Field(..., description="Technical stack and architecture summary")
    key_capabilities: List[str] = Field(
        default_factory=list,
        description="Key capabilities and features"
    )
    important_files_summary: str = Field(
        ...,
        description="Summary of important files and their purposes"
    )
    suggested_entry_points: List[str] = Field(
        default_factory=list,
        description="Suggested files to start exploring"
    )


class ReasoningStep(BaseModel):
    """Individual reasoning step explaining a detection."""
    category: str = Field(..., description="Reasoning category (classification, framework, workflow, medical)")
    title: str = Field(..., description="Step title")
    explanation: str = Field(..., description="Detailed explanation")
    evidence: List[str] = Field(default_factory=list, description="Supporting evidence")
    confidence_impact: str = Field(..., description="How this impacts confidence (positive, neutral, negative)")


class AIReasoning(BaseModel):
    """AI reasoning explaining WHY classifications were made."""
    classification_reasoning: List[ReasoningStep] = Field(
        default_factory=list,
        description="Steps explaining repository classification"
    )
    framework_reasoning: List[ReasoningStep] = Field(
        default_factory=list,
        description="Steps explaining framework detection"
    )
    workflow_reasoning: List[ReasoningStep] = Field(
        default_factory=list,
        description="Steps explaining workflow detection"
    )
    medical_reasoning: List[ReasoningStep] = Field(
        default_factory=list,
        description="Steps explaining medical AI detection"
    )
    summary: str = Field(..., description="Overall reasoning summary")


class MaturityIndicator(BaseModel):
    """Individual maturity indicator."""
    name: str = Field(..., description="Indicator name")
    status: str = Field(..., description="Status (present, absent, partial)")
    impact: str = Field(..., description="Impact on maturity (high, medium, low)")
    description: str = Field(..., description="What this indicates")


class RepositoryMaturity(BaseModel):
    """Repository maturity assessment."""
    level: str = Field(..., description="Maturity level (production_ready, enterprise_scale, research_grade, prototype, experimental)")
    score: float = Field(..., description="Maturity score (0-100)")
    confidence: str = Field(..., description="Confidence in assessment")
    indicators: List[MaturityIndicator] = Field(
        default_factory=list,
        description="Maturity indicators found"
    )
    strengths: List[str] = Field(default_factory=list, description="Repository strengths")
    gaps: List[str] = Field(default_factory=list, description="Areas for improvement")
    summary: str = Field(..., description="Maturity summary")


class ArchitectureInsight(BaseModel):
    """Individual architecture insight."""
    insight_type: str = Field(..., description="Insight type")
    title: str = Field(..., description="Insight title")
    description: str = Field(..., description="Detailed description")
    evidence: List[str] = Field(default_factory=list, description="Supporting evidence")
    significance: str = Field(..., description="Significance (high, medium, low)")


class ArchitectureAnalysis(BaseModel):
    """Architecture insights and patterns."""
    insights: List[ArchitectureInsight] = Field(
        default_factory=list,
        description="Detected architecture insights"
    )
    patterns: List[str] = Field(
        default_factory=list,
        description="Architecture patterns detected"
    )
    summary: str = Field(..., description="Architecture summary")


class ExecutiveSummary(BaseModel):
    """Executive-style repository summary."""
    headline: str = Field(..., description="One-line headline")
    overview: str = Field(..., description="2-3 sentence overview")
    key_highlights: List[str] = Field(
        default_factory=list,
        description="3-5 key highlights"
    )
    technical_profile: str = Field(..., description="Technical profile summary")
    use_cases: List[str] = Field(
        default_factory=list,
        description="Potential use cases"
    )
    target_audience: str = Field(..., description="Target audience description")


class UnifiedRepositoryIntelligence(BaseModel):
    """
    Unified repository intelligence combining metadata, structure, and analysis.
    Optimized for LLM consumption and lightweight processing.
    """
    # Basic info
    owner: str = Field(..., description="Repository owner")
    repo: str = Field(..., description="Repository name")
    branch: str = Field(..., description="Analyzed branch")
    
    # Metadata summary
    metadata: RepositoryMetadataSummary = Field(
        ...,
        description="Repository metadata summary"
    )
    
    # Structure summary
    structure: RepositoryStructureSummary = Field(
        ...,
        description="Repository structure summary"
    )
    
    # Classification
    classification: RepositoryClassification = Field(
        ...,
        description="Repository classification and type"
    )
    
    # Workflow
    workflow: WorkflowSummary = Field(
        ...,
        description="Detected workflow components"
    )
    
    # Technology stack
    technology: TechnologyStack = Field(
        ...,
        description="Detected technology stack"
    )
    
    # Medical AI context
    medical_context: MedicalAIContext = Field(
        ...,
        description="Medical AI specific context"
    )
    
    # Statistics
    statistics: ProjectStatistics = Field(
        ...,
        description="Project statistics"
    )
    
    # LLM-optimized summary
    llm_context: LLMContextSummary = Field(
        ...,
        description="Structured summary for LLM usage"
    )
    
    # Premium Intelligence Features
    ai_reasoning: Optional[AIReasoning] = Field(
        None,
        description="AI reasoning explaining detection decisions"
    )
    
    maturity: Optional[RepositoryMaturity] = Field(
        None,
        description="Repository maturity assessment"
    )
    
    architecture: Optional[ArchitectureAnalysis] = Field(
        None,
        description="Architecture insights and patterns"
    )
    
    executive_summary: Optional[ExecutiveSummary] = Field(
        None,
        description="Executive-style summary"
    )
    
    # Timestamp
    analyzed_at: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat(),
        description="Analysis timestamp"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "owner": "Project-MONAI",
                "repo": "MONAI",
                "branch": "main",
                "metadata": {
                    "name": "MONAI",
                    "full_name": "Project-MONAI/MONAI",
                    "description": "AI Toolkit for Healthcare Imaging",
                    "stars": 5000,
                    "forks": 800,
                    "primary_language": "Python",
                    "topics": ["medical-imaging", "deep-learning", "pytorch"],
                    "created_at": "2019-01-01T00:00:00Z",
                    "updated_at": "2024-01-15T10:30:00Z",
                    "size": 50000,
                    "license": "Apache-2.0",
                    "html_url": "https://github.com/Project-MONAI/MONAI"
                },
                "classification": {
                    "primary_type": "medical_imaging",
                    "secondary_types": ["machine_learning", "research"],
                    "confidence": "high"
                },
                "medical_context": {
                    "is_medical_ai": True,
                    "confidence": "high",
                    "modalities": ["MRI", "CT", "DICOM"],
                    "tasks": ["segmentation", "classification"]
                },
                "llm_context": {
                    "repository_overview": "Medical imaging AI toolkit using PyTorch",
                    "technical_summary": "PyTorch-based framework for medical imaging with MONAI",
                    "key_capabilities": ["Medical image segmentation", "3D volumetric processing"],
                    "important_files_summary": "Training in train.py, models in models/",
                    "suggested_entry_points": ["train.py", "README.md", "requirements.txt"]
                }
            }
        }


class IntelligenceRequest(BaseModel):
    """Request model for unified repository intelligence."""
    url: str = Field(..., description="GitHub repository URL")
    branch: Optional[str] = Field(None, description="Branch name (defaults to default branch)")
    include_filtered: bool = Field(
        default=False,
        description="Include filtered files in tree analysis"
    )
    max_depth: Optional[int] = Field(
        None,
        description="Maximum tree depth (None for unlimited)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://github.com/Project-MONAI/MONAI",
                "branch": "main",
                "include_filtered": False,
                "max_depth": None
            }
        }

# Made with Bob