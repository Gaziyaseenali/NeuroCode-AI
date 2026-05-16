"""
Unit tests for the repository intelligence aggregation service.
Tests the orchestration of metadata, tree, and analysis services.
"""
import pytest
from unittest.mock import Mock, patch
from app.services.intelligence_service import (
    RepositoryIntelligenceService,
    IntelligenceServiceError
)
from app.models.github import GitHubRepoMetadata, GitHubOwner, RepositoryTree, TreeNode, FileType, ImportanceLevel
from app.models.analyzer import (
    RepositoryIntelligence,
    RepositoryTypeDetection,
    RepositoryType,
    DetectionConfidence,
    FrameworkDetection,
    Framework,
    WorkflowDetection,
    WorkflowComponent
)


@pytest.fixture
def mock_metadata():
    """Create mock repository metadata."""
    return GitHubRepoMetadata(
        name="test-repo",
        full_name="test-owner/test-repo",
        description="Test repository for medical imaging",
        owner=GitHubOwner(
            login="test-owner",
            type="User",
            avatar_url="https://example.com/avatar.png"
        ),
        stargazers_count=1000,
        forks_count=200,
        watchers_count=1000,
        open_issues_count=50,
        language="Python",
        topics=["medical-imaging", "pytorch", "deep-learning"],
        default_branch="main",
        created_at="2020-01-01T00:00:00Z",
        updated_at="2024-01-01T00:00:00Z",
        pushed_at="2024-01-01T00:00:00Z",
        size=10000,
        fork=False,
        archived=False,
        private=False,
        html_url="https://github.com/test-owner/test-repo",
        clone_url="https://github.com/test-owner/test-repo.git",
        ssh_url="git@github.com:test-owner/test-repo.git",
        homepage="https://example.com",
        license="MIT"
    )


@pytest.fixture
def mock_tree():
    """Create mock repository tree."""
    files = [
        TreeNode(
            path="train.py",
            name="train.py",
            type=FileType.FILE,
            size=5000,
            importance=ImportanceLevel.CRITICAL
        ),
        TreeNode(
            path="infer.py",
            name="infer.py",
            type=FileType.FILE,
            size=3000,
            importance=ImportanceLevel.CRITICAL
        ),
        TreeNode(
            path="requirements.txt",
            name="requirements.txt",
            type=FileType.FILE,
            size=500,
            importance=ImportanceLevel.HIGH
        ),
        TreeNode(
            path="README.md",
            name="README.md",
            type=FileType.FILE,
            size=2000,
            importance=ImportanceLevel.HIGH
        )
    ]
    
    return RepositoryTree(
        owner="test-owner",
        repo="test-repo",
        branch="main",
        total_files=100,
        total_directories=20,
        filtered_files=4,
        filtered_directories=2,
        files=files,
        directories=[],
        important_files={
            "critical": files[:2],
            "high": files[2:],
            "medium": [],
            "low": []
        },
        truncated=False
    )


@pytest.fixture
def mock_analysis():
    """Create mock repository analysis."""
    return RepositoryIntelligence(
        owner="test-owner",
        repo="test-repo",
        repository_types=[
            RepositoryTypeDetection(
                type=RepositoryType.MEDICAL_IMAGING,
                confidence=DetectionConfidence.HIGH,
                evidence=["MONAI framework", "medical imaging files"]
            )
        ],
        workflow_components=[
            WorkflowDetection(
                component=WorkflowComponent.TRAINING,
                confidence=DetectionConfidence.HIGH,
                evidence=["train.py"]
            ),
            WorkflowDetection(
                component=WorkflowComponent.INFERENCE,
                confidence=DetectionConfidence.HIGH,
                evidence=["infer.py"]
            )
        ],
        frameworks=[
            FrameworkDetection(
                framework=Framework.PYTORCH,
                confidence=DetectionConfidence.HIGH,
                evidence=["torch imports"]
            ),
            FrameworkDetection(
                framework=Framework.MONAI,
                confidence=DetectionConfidence.HIGH,
                evidence=["monai imports"]
            )
        ],
        medical_signals=[],
        key_files={
            "training": ["train.py"],
            "inference": ["infer.py"],
            "models": ["model.py"]
        },
        total_python_files=50,
        total_notebook_files=5,
        total_config_files=3,
        has_requirements=True,
        has_dockerfile=False,
        has_readme=True,
        summary="Medical imaging repository using PyTorch and MONAI"
    )


class TestRepositoryIntelligenceService:
    """Test cases for RepositoryIntelligenceService."""
    
    def test_initialization(self):
        """Test service initialization."""
        service = RepositoryIntelligenceService()
        assert service.github_service is not None
        assert service.tree_service is not None
        assert service.analyzer is not None
    
    @patch('app.services.intelligence_service.parse_github_url')
    @patch('app.services.intelligence_service.get_github_service')
    @patch('app.services.intelligence_service.get_github_tree_service')
    @patch('app.services.intelligence_service.get_repository_analyzer')
    def test_analyze_repository_success(
        self,
        mock_get_analyzer,
        mock_get_tree_service,
        mock_get_github_service,
        mock_parse_url,
        mock_metadata,
        mock_tree,
        mock_analysis
    ):
        """Test successful repository analysis."""
        # Setup mocks
        mock_parse_url.return_value = ("test-owner", "test-repo")
        
        mock_github_service = Mock()
        mock_github_service.fetch_repository_metadata.return_value = mock_metadata
        mock_get_github_service.return_value = mock_github_service
        
        mock_tree_service = Mock()
        mock_tree_service.fetch_repository_tree.return_value = mock_tree
        mock_get_tree_service.return_value = mock_tree_service
        
        mock_analyzer = Mock()
        mock_analyzer.analyze.return_value = mock_analysis
        mock_get_analyzer.return_value = mock_analyzer
        
        # Create service and analyze
        service = RepositoryIntelligenceService(
            github_service=mock_github_service,
            tree_service=mock_tree_service,
            analyzer=mock_analyzer
        )
        
        intelligence = service.analyze_repository(
            url="https://github.com/test-owner/test-repo"
        )
        
        # Verify results
        assert intelligence.owner == "test-owner"
        assert intelligence.repo == "test-repo"
        assert intelligence.branch == "main"
        
        # Check metadata summary
        assert intelligence.metadata.name == "test-repo"
        assert intelligence.metadata.stars == 1000
        assert intelligence.metadata.primary_language == "Python"
        
        # Check structure summary
        assert intelligence.structure.total_files == 100
        assert intelligence.structure.filtered_files == 4
        assert len(intelligence.structure.critical_files) == 2
        
        # Check classification
        assert intelligence.classification.primary_type == "medical_imaging"
        assert intelligence.classification.confidence == "high"
        
        # Check workflow
        assert intelligence.workflow.has_training is True
        assert intelligence.workflow.has_inference is True
        
        # Check technology
        assert "pytorch" in intelligence.technology.primary_frameworks
        assert "monai" in intelligence.technology.medical_frameworks
        
        # Check medical context
        assert intelligence.medical_context.is_medical_ai is True
        
        # Check statistics
        assert intelligence.statistics.total_python_files == 50
        assert intelligence.statistics.has_requirements is True
        
        # Check LLM context
        assert intelligence.llm_context.repository_overview
        assert intelligence.llm_context.technical_summary
        assert len(intelligence.llm_context.suggested_entry_points) > 0
    
    @patch('app.services.intelligence_service.parse_github_url')
    def test_analyze_repository_invalid_url(self, mock_parse_url):
        """Test analysis with invalid URL."""
        mock_parse_url.side_effect = Exception("Invalid URL")
        
        service = RepositoryIntelligenceService()
        
        with pytest.raises(IntelligenceServiceError):
            service.analyze_repository(url="invalid-url")
    
    @patch('app.services.intelligence_service.parse_github_url')
    @patch('app.services.intelligence_service.get_github_service')
    def test_analyze_repository_metadata_error(
        self,
        mock_get_github_service,
        mock_parse_url
    ):
        """Test analysis when metadata fetching fails."""
        mock_parse_url.return_value = ("test-owner", "test-repo")
        
        mock_github_service = Mock()
        mock_github_service.fetch_repository_metadata.side_effect = Exception("API Error")
        mock_get_github_service.return_value = mock_github_service
        
        service = RepositoryIntelligenceService(github_service=mock_github_service)
        
        with pytest.raises(IntelligenceServiceError):
            service.analyze_repository(url="https://github.com/test-owner/test-repo")
    
    def test_llm_context_generation(self, mock_metadata, mock_tree, mock_analysis):
        """Test LLM context summary generation."""
        service = RepositoryIntelligenceService()
        
        # Create mock data structures
        from app.models.intelligence import (
            RepositoryMetadataSummary,
            RepositoryClassification,
            WorkflowSummary,
            TechnologyStack,
            MedicalAIContext
        )
        
        metadata_summary = RepositoryMetadataSummary(
            name=mock_metadata.name,
            full_name=mock_metadata.full_name,
            description=mock_metadata.description,
            stars=mock_metadata.stars,
            forks=mock_metadata.forks,
            primary_language=mock_metadata.primary_language,
            topics=mock_metadata.topics,
            created_at=mock_metadata.created_at,
            updated_at=mock_metadata.updated_at,
            size=mock_metadata.size,
            license=mock_metadata.license,
            html_url=mock_metadata.html_url
        )
        
        classification = RepositoryClassification(
            primary_type="medical_imaging",
            secondary_types=["machine_learning"],
            confidence="high",
            all_detections=mock_analysis.repository_types
        )
        
        workflow_summary = WorkflowSummary(
            has_training=True,
            has_inference=True,
            has_preprocessing=False,
            has_evaluation=False,
            has_deployment=False,
            components=mock_analysis.workflow_components
        )
        
        technology = TechnologyStack(
            primary_frameworks=["pytorch", "monai"],
            all_frameworks=mock_analysis.frameworks,
            medical_frameworks=["monai"]
        )
        
        medical_context = MedicalAIContext(
            is_medical_ai=True,
            confidence="high",
            detected_signals=[],
            modalities=["MRI", "CT"],
            tasks=["segmentation"]
        )
        
        # Generate LLM context
        llm_context = service._build_llm_context(
            metadata_summary=metadata_summary,
            classification=classification,
            workflow_summary=workflow_summary,
            technology=technology,
            medical_context=medical_context,
            analysis=mock_analysis,
            tree=mock_tree
        )
        
        # Verify LLM context
        assert llm_context.repository_overview
        assert "Medical Imaging" in llm_context.repository_overview
        assert llm_context.technical_summary
        assert "Python" in llm_context.technical_summary
        assert len(llm_context.key_capabilities) > 0
        assert llm_context.important_files_summary
        assert len(llm_context.suggested_entry_points) > 0


def test_get_intelligence_service():
    """Test singleton service getter."""
    from app.services.intelligence_service import get_intelligence_service
    
    service1 = get_intelligence_service()
    service2 = get_intelligence_service()
    
    assert service1 is service2  # Should be same instance

# Made with Bob