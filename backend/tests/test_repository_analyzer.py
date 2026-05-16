"""
Tests for repository analyzer service.
"""
import pytest
from app.services.repository_analyzer import RepositoryAnalyzer, get_repository_analyzer
from app.models.github import RepositoryTree, TreeNode, FileType, ImportanceLevel
from app.models.analyzer import (
    RepositoryType,
    WorkflowComponent,
    Framework,
    MedicalSignal,
    DetectionConfidence
)


@pytest.fixture
def analyzer():
    """Create analyzer instance."""
    return RepositoryAnalyzer()


@pytest.fixture
def medical_imaging_tree():
    """Create a mock medical imaging repository tree."""
    files = [
        TreeNode(path="train.py", name="train.py", type=FileType.FILE, importance=ImportanceLevel.CRITICAL),
        TreeNode(path="inference.py", name="inference.py", type=FileType.FILE, importance=ImportanceLevel.CRITICAL),
        TreeNode(path="models/unet.py", name="unet.py", type=FileType.FILE, importance=ImportanceLevel.HIGH),
        TreeNode(path="data/preprocess_mri.py", name="preprocess_mri.py", type=FileType.FILE),
        TreeNode(path="utils/dicom_loader.py", name="dicom_loader.py", type=FileType.FILE),
        TreeNode(path="config.yaml", name="config.yaml", type=FileType.FILE, importance=ImportanceLevel.HIGH),
        TreeNode(path="requirements.txt", name="requirements.txt", type=FileType.FILE, importance=ImportanceLevel.HIGH),
        TreeNode(path="README.md", name="README.md", type=FileType.FILE, importance=ImportanceLevel.HIGH),
        TreeNode(path="notebooks/segmentation_demo.ipynb", name="segmentation_demo.ipynb", type=FileType.FILE),
        TreeNode(path="data/ct_scans/sample.nii.gz", name="sample.nii.gz", type=FileType.FILE),
    ]
    
    return RepositoryTree(
        owner="test-owner",
        repo="medical-ai-project",
        branch="main",
        total_files=10,
        total_directories=3,
        filtered_files=10,
        filtered_directories=3,
        files=files,
        directories=[],
        important_files={},
        truncated=False
    )


@pytest.fixture
def pytorch_ml_tree():
    """Create a mock PyTorch ML repository tree."""
    files = [
        TreeNode(path="train.py", name="train.py", type=FileType.FILE, importance=ImportanceLevel.CRITICAL),
        TreeNode(path="model.py", name="model.py", type=FileType.FILE, importance=ImportanceLevel.CRITICAL),
        TreeNode(path="utils/torch_utils.py", name="torch_utils.py", type=FileType.FILE),
        TreeNode(path="data/dataset.py", name="dataset.py", type=FileType.FILE),
        TreeNode(path="checkpoints/model.pth", name="model.pth", type=FileType.FILE),
        TreeNode(path="requirements.txt", name="requirements.txt", type=FileType.FILE, importance=ImportanceLevel.HIGH),
        TreeNode(path="README.md", name="README.md", type=FileType.FILE, importance=ImportanceLevel.HIGH),
    ]
    
    return RepositoryTree(
        owner="test-owner",
        repo="pytorch-project",
        branch="main",
        total_files=7,
        total_directories=2,
        filtered_files=7,
        filtered_directories=2,
        files=files,
        directories=[],
        important_files={},
        truncated=False
    )


def test_analyzer_singleton():
    """Test that get_repository_analyzer returns singleton."""
    analyzer1 = get_repository_analyzer()
    analyzer2 = get_repository_analyzer()
    assert analyzer1 is analyzer2


def test_detect_medical_imaging_repository(analyzer, medical_imaging_tree):
    """Test detection of medical imaging repository."""
    intelligence = analyzer.analyze(medical_imaging_tree)
    
    # Check repository types
    assert len(intelligence.repository_types) > 0
    repo_types = [rt.type for rt in intelligence.repository_types]
    assert RepositoryType.MEDICAL_IMAGING in repo_types or RepositoryType.SEGMENTATION in repo_types
    
    # Check owner and repo
    assert intelligence.owner == "test-owner"
    assert intelligence.repo == "medical-ai-project"


def test_detect_medical_signals(analyzer, medical_imaging_tree):
    """Test detection of medical AI signals."""
    intelligence = analyzer.analyze(medical_imaging_tree)
    
    # Should detect medical signals
    assert len(intelligence.medical_signals) > 0
    
    signal_types = [ms.signal for ms in intelligence.medical_signals]
    # Should detect at least some medical signals
    assert any(s in signal_types for s in [
        MedicalSignal.SEGMENTATION,
        MedicalSignal.MRI,
        MedicalSignal.DICOM,
        MedicalSignal.NIFTI
    ])


def test_detect_workflow_components(analyzer, medical_imaging_tree):
    """Test detection of workflow components."""
    intelligence = analyzer.analyze(medical_imaging_tree)
    
    # Should detect training and inference
    assert len(intelligence.workflow_components) > 0
    
    component_types = [wc.component for wc in intelligence.workflow_components]
    assert WorkflowComponent.TRAINING in component_types
    assert WorkflowComponent.INFERENCE in component_types


def test_detect_pytorch_framework(analyzer, pytorch_ml_tree):
    """Test detection of PyTorch framework."""
    intelligence = analyzer.analyze(pytorch_ml_tree)
    
    # Should detect PyTorch
    assert len(intelligence.frameworks) > 0
    
    framework_types = [f.framework for f in intelligence.frameworks]
    assert Framework.PYTORCH in framework_types


def test_extract_key_files(analyzer, medical_imaging_tree):
    """Test extraction of key files."""
    intelligence = analyzer.analyze(medical_imaging_tree)
    
    # Should have key files
    assert len(intelligence.key_files) > 0
    
    # Should have training files
    if 'training' in intelligence.key_files:
        assert 'train.py' in intelligence.key_files['training']
    
    # Should have inference files
    if 'inference' in intelligence.key_files:
        assert 'inference.py' in intelligence.key_files['inference']


def test_calculate_statistics(analyzer, medical_imaging_tree):
    """Test calculation of repository statistics."""
    intelligence = analyzer.analyze(medical_imaging_tree)
    
    # Check statistics
    assert intelligence.total_python_files > 0
    assert intelligence.total_notebook_files > 0
    assert intelligence.has_requirements is True
    assert intelligence.has_readme is True


def test_generate_summary(analyzer, medical_imaging_tree):
    """Test generation of human-readable summary."""
    intelligence = analyzer.analyze(medical_imaging_tree)
    
    # Should have a summary
    assert intelligence.summary
    assert len(intelligence.summary) > 0
    assert isinstance(intelligence.summary, str)


def test_confidence_levels(analyzer, medical_imaging_tree):
    """Test that confidence levels are assigned."""
    intelligence = analyzer.analyze(medical_imaging_tree)
    
    # Check that detections have confidence levels
    for repo_type in intelligence.repository_types:
        assert repo_type.confidence in [
            DetectionConfidence.HIGH,
            DetectionConfidence.MEDIUM,
            DetectionConfidence.LOW
        ]
    
    for framework in intelligence.frameworks:
        assert framework.confidence in [
            DetectionConfidence.HIGH,
            DetectionConfidence.MEDIUM,
            DetectionConfidence.LOW
        ]


def test_evidence_provided(analyzer, medical_imaging_tree):
    """Test that evidence is provided for detections."""
    intelligence = analyzer.analyze(medical_imaging_tree)
    
    # Check that detections have evidence
    for repo_type in intelligence.repository_types:
        assert isinstance(repo_type.evidence, list)
    
    for framework in intelligence.frameworks:
        assert isinstance(framework.evidence, list)
    
    for workflow in intelligence.workflow_components:
        assert isinstance(workflow.evidence, list)


def test_empty_repository():
    """Test analysis of empty repository."""
    analyzer = RepositoryAnalyzer()
    
    empty_tree = RepositoryTree(
        owner="test-owner",
        repo="empty-repo",
        branch="main",
        total_files=0,
        total_directories=0,
        filtered_files=0,
        filtered_directories=0,
        files=[],
        directories=[],
        important_files={},
        truncated=False
    )
    
    intelligence = analyzer.analyze(empty_tree)
    
    # Should still return valid intelligence
    assert intelligence.owner == "test-owner"
    assert intelligence.repo == "empty-repo"
    assert intelligence.total_python_files == 0
    assert len(intelligence.repository_types) > 0  # Should at least have GENERAL type


def test_research_repository_detection(analyzer):
    """Test detection of research repository."""
    files = [
        TreeNode(path="paper.pdf", name="paper.pdf", type=FileType.FILE),
        TreeNode(path="notebooks/experiment1.ipynb", name="experiment1.ipynb", type=FileType.FILE),
        TreeNode(path="notebooks/experiment2.ipynb", name="experiment2.ipynb", type=FileType.FILE),
        TreeNode(path="README.md", name="README.md", type=FileType.FILE),
    ]
    
    tree = RepositoryTree(
        owner="test-owner",
        repo="research-project",
        branch="main",
        total_files=4,
        total_directories=1,
        filtered_files=4,
        filtered_directories=1,
        files=files,
        directories=[],
        important_files={},
        truncated=False
    )
    
    intelligence = analyzer.analyze(tree)
    
    # Should detect research type
    repo_types = [rt.type for rt in intelligence.repository_types]
    assert RepositoryType.RESEARCH in repo_types


def test_inference_only_repository(analyzer):
    """Test detection of inference-only repository."""
    files = [
        TreeNode(path="inference.py", name="inference.py", type=FileType.FILE),
        TreeNode(path="predict.py", name="predict.py", type=FileType.FILE),
        TreeNode(path="api.py", name="api.py", type=FileType.FILE),
        TreeNode(path="Dockerfile", name="Dockerfile", type=FileType.FILE),
        TreeNode(path="model.pth", name="model.pth", type=FileType.FILE),
    ]
    
    tree = RepositoryTree(
        owner="test-owner",
        repo="inference-service",
        branch="main",
        total_files=5,
        total_directories=0,
        filtered_files=5,
        filtered_directories=0,
        files=files,
        directories=[],
        important_files={},
        truncated=False
    )
    
    intelligence = analyzer.analyze(tree)
    
    # Should detect inference type
    repo_types = [rt.type for rt in intelligence.repository_types]
    assert RepositoryType.INFERENCE in repo_types
    
    # Should detect deployment component
    component_types = [wc.component for wc in intelligence.workflow_components]
    assert WorkflowComponent.DEPLOYMENT in component_types

# Made with Bob
