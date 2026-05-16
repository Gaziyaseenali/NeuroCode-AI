"""
Pydantic models for repository structure analysis and intelligence output.
Lightweight rule-based analysis for ML/medical AI repository detection.
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from enum import Enum


class RepositoryType(str, Enum):
    """Detected repository type with expanded domain categories."""
    # Core AI/ML domains
    NLP = "nlp"
    FOUNDATION_MODELS = "foundation_models"
    MULTIMODAL_AI = "multimodal_ai"
    COMPUTER_VISION = "computer_vision"
    OBJECT_DETECTION = "object_detection"
    SEGMENTATION = "segmentation"
    MEDICAL_IMAGING = "medical_imaging"
    REINFORCEMENT_LEARNING = "reinforcement_learning"
    ROBOTICS = "robotics"
    DATA_SCIENCE = "data_science"
    
    # Legacy/general categories
    MACHINE_LEARNING = "machine_learning"
    RESEARCH = "research"
    INFERENCE = "inference"
    GENERAL = "general"


class WorkflowComponent(str, Enum):
    """Detected workflow components."""
    PREPROCESSING = "preprocessing"
    TRAINING = "training"
    INFERENCE = "inference"
    EVALUATION = "evaluation"
    DEPLOYMENT = "deployment"


class Framework(str, Enum):
    """Detected AI/ML frameworks."""
    PYTORCH = "pytorch"
    TENSORFLOW = "tensorflow"
    MONAI = "monai"
    SIMPLEITK = "simpleitk"
    NIBABEL = "nibabel"
    KERAS = "keras"
    SCIKIT_LEARN = "scikit_learn"
    OPENCV = "opencv"


class MedicalSignal(str, Enum):
    """Detected medical AI signals."""
    SEGMENTATION = "segmentation"
    MRI = "mri"
    CT = "ct"
    DICOM = "dicom"
    VOLUMETRIC = "volumetric"
    NIFTI = "nifti"
    MEDICAL_IMAGING = "medical_imaging"


class DetectionConfidence(str, Enum):
    """Confidence level for detections."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class FrameworkDetection(BaseModel):
    """Framework detection result."""
    framework: Framework
    confidence: DetectionConfidence
    evidence: List[str] = Field(default_factory=list, description="Files/patterns that indicate this framework")


class WorkflowDetection(BaseModel):
    """Workflow component detection result."""
    component: WorkflowComponent
    confidence: DetectionConfidence
    evidence: List[str] = Field(default_factory=list, description="Files/patterns that indicate this component")


class MedicalSignalDetection(BaseModel):
    """Medical AI signal detection result with debugging information."""
    signal: MedicalSignal
    confidence: DetectionConfidence
    evidence: List[str] = Field(default_factory=list, description="Files/patterns that indicate this signal")
    explanation: str = Field("", description="Debugging explanation of why this signal was detected")


class RepositoryTypeDetection(BaseModel):
    """Repository type detection result with weighted scoring."""
    type: RepositoryType
    confidence: DetectionConfidence
    evidence: List[str] = Field(default_factory=list, description="Reasons for this classification")
    score: float = Field(0.0, description="Weighted score for this classification")
    explanation: str = Field("", description="Human-readable explanation of why this classification was assigned")


class RepositoryIntelligence(BaseModel):
    """Complete repository intelligence analysis output."""
    owner: str = Field(..., description="Repository owner")
    repo: str = Field(..., description="Repository name")
    
    # Primary classification
    repository_types: List[RepositoryTypeDetection] = Field(
        default_factory=list,
        description="Detected repository types with confidence"
    )
    
    # Workflow components
    workflow_components: List[WorkflowDetection] = Field(
        default_factory=list,
        description="Detected workflow components"
    )
    
    # Frameworks
    frameworks: List[FrameworkDetection] = Field(
        default_factory=list,
        description="Detected AI/ML frameworks"
    )
    
    # Medical AI signals
    medical_signals: List[MedicalSignalDetection] = Field(
        default_factory=list,
        description="Detected medical AI signals"
    )
    
    # Key files
    key_files: Dict[str, List[str]] = Field(
        default_factory=dict,
        description="Important files grouped by category"
    )
    
    # Statistics
    total_python_files: int = Field(0, description="Total Python files")
    total_notebook_files: int = Field(0, description="Total Jupyter notebooks")
    total_config_files: int = Field(0, description="Total configuration files")
    has_requirements: bool = Field(False, description="Has requirements.txt")
    has_dockerfile: bool = Field(False, description="Has Dockerfile")
    has_readme: bool = Field(False, description="Has README")
    
    # Summary
    summary: str = Field("", description="Human-readable summary of the repository")
    
    class Config:
        json_schema_extra = {
            "example": {
                "owner": "Project-MONAI",
                "repo": "MONAI",
                "repository_types": [
                    {
                        "type": "medical_imaging",
                        "confidence": "high",
                        "evidence": ["MONAI framework", "medical imaging files", "segmentation models"]
                    }
                ],
                "workflow_components": [
                    {
                        "component": "training",
                        "confidence": "high",
                        "evidence": ["train.py", "trainer.py"]
                    }
                ],
                "frameworks": [
                    {
                        "framework": "pytorch",
                        "confidence": "high",
                        "evidence": ["torch imports", "model.py"]
                    }
                ],
                "medical_signals": [
                    {
                        "signal": "segmentation",
                        "confidence": "high",
                        "evidence": ["segmentation in filenames", "UNet architecture"]
                    }
                ],
                "key_files": {
                    "training": ["train.py", "trainer.py"],
                    "models": ["model.py", "unet.py"]
                },
                "total_python_files": 150,
                "total_notebook_files": 10,
                "has_requirements": True,
                "summary": "Medical imaging repository using PyTorch and MONAI for segmentation tasks"
            }
        }


class AnalyzerRequest(BaseModel):
    """Request model for repository analysis."""
    url: str = Field(..., description="GitHub repository URL")
    branch: Optional[str] = Field(None, description="Branch name (defaults to default branch)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://github.com/Project-MONAI/MONAI",
                "branch": "main"
            }
        }

# Made with Bob
