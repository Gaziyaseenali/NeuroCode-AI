"""
Lightweight repository intelligence aggregation service.
Orchestrates metadata fetching, tree fetching, and analysis services.
Optimized for low RAM usage and hackathon MVP simplicity.
"""
from typing import Optional
from app.services.github_service import GitHubService, get_github_service
from app.services.github_tree_service import GitHubTreeService, get_github_tree_service
from app.services.repository_analyzer import RepositoryAnalyzer, get_repository_analyzer
from app.services.premium_intelligence import PremiumIntelligenceService, get_premium_intelligence_service
from app.utils.github_parser import parse_github_url
from app.models.intelligence import (
    UnifiedRepositoryIntelligence,
    RepositoryMetadataSummary,
    RepositoryStructureSummary,
    RepositoryClassification,
    WorkflowSummary,
    TechnologyStack,
    MedicalAIContext,
    ProjectStatistics,
    LLMContextSummary
)
from app.models.analyzer import DetectionConfidence


class IntelligenceServiceError(Exception):
    """Base exception for intelligence service errors."""
    pass


class RepositoryIntelligenceService:
    """
    Orchestration service for unified repository intelligence.
    
    Features:
    - Combines metadata, tree, and analysis services
    - Generates structured intelligence output
    - Creates LLM-optimized context summaries
    - Lightweight and scalable
    - No embeddings, vector DBs, or LLM inference
    """
    
    def __init__(
        self,
        github_service: Optional[GitHubService] = None,
        tree_service: Optional[GitHubTreeService] = None,
        analyzer: Optional[RepositoryAnalyzer] = None,
        premium_service: Optional[PremiumIntelligenceService] = None
    ):
        """
        Initialize intelligence service with optional service instances.
        
        Args:
            github_service: GitHub metadata service (uses singleton if None)
            tree_service: GitHub tree service (uses singleton if None)
            analyzer: Repository analyzer (uses singleton if None)
            premium_service: Premium intelligence service (uses singleton if None)
        """
        self.github_service = github_service or get_github_service()
        self.tree_service = tree_service or get_github_tree_service()
        self.analyzer = analyzer or get_repository_analyzer()
        self.premium_service = premium_service or get_premium_intelligence_service()
    
    def analyze_repository(
        self,
        url: str,
        branch: Optional[str] = None,
        include_filtered: bool = False,
        max_depth: Optional[int] = None
    ) -> UnifiedRepositoryIntelligence:
        """
        Perform complete repository intelligence analysis.
        
        Args:
            url: GitHub repository URL
            branch: Branch name (defaults to default branch)
            include_filtered: Include filtered files in tree
            max_depth: Maximum tree depth
            
        Returns:
            UnifiedRepositoryIntelligence with complete analysis
            
        Raises:
            IntelligenceServiceError: For any analysis errors
        """
        try:
            # Parse GitHub URL
            owner, repo = parse_github_url(url)
            
            # Step 1: Fetch repository metadata
            metadata = self.github_service.fetch_repository_metadata(owner, repo)
            
            # Use default branch if not specified
            if not branch:
                branch = metadata.default_branch
            
            # Step 2: Fetch repository tree
            tree = self.tree_service.fetch_repository_tree(
                owner=owner,
                repo=repo,
                branch=branch,
                max_depth=max_depth,
                include_filtered=include_filtered
            )
            
            # Step 3: Analyze repository structure
            analysis = self.analyzer.analyze(tree)
            
            # Step 4: Aggregate intelligence
            intelligence = self._aggregate_intelligence(
                owner=owner,
                repo=repo,
                branch=branch,
                metadata=metadata,
                tree=tree,
                analysis=analysis
            )
            
            # Step 5: Enhance with premium intelligence features
            intelligence = self.premium_service.enhance_intelligence(intelligence)
            
            return intelligence
            
        except Exception as e:
            raise IntelligenceServiceError(f"Failed to analyze repository: {str(e)}")
    
    def _aggregate_intelligence(
        self,
        owner: str,
        repo: str,
        branch: str,
        metadata,
        tree,
        analysis
    ) -> UnifiedRepositoryIntelligence:
        """Aggregate all intelligence into unified output."""
        
        # Build metadata summary
        metadata_summary = RepositoryMetadataSummary(
            name=metadata.name,
            full_name=metadata.full_name,
            description=metadata.description,
            stars=metadata.stars,
            forks=metadata.forks,
            primary_language=metadata.primary_language,
            topics=metadata.topics,
            created_at=metadata.created_at,
            updated_at=metadata.updated_at,
            size=metadata.size,
            license=metadata.license,
            html_url=metadata.html_url
        )
        
        # Build structure summary
        important_files_count = {
            level: len(files)
            for level, files in tree.important_files.items()
            if files
        }
        
        structure_summary = RepositoryStructureSummary(
            total_files=tree.total_files,
            total_directories=tree.total_directories,
            filtered_files=tree.filtered_files,
            filtered_directories=tree.filtered_directories,
            important_files_count=important_files_count,
            critical_files=tree.important_files.get("critical", [])[:5],
            high_importance_files=tree.important_files.get("high", [])[:5]
        )
        
        # Build classification
        primary_type = analysis.repository_types[0].type.value if analysis.repository_types else "general"
        secondary_types = [
            t.type.value for t in analysis.repository_types[1:3]
        ]
        confidence = analysis.repository_types[0].confidence.value if analysis.repository_types else "low"
        
        classification = RepositoryClassification(
            primary_type=primary_type,
            secondary_types=secondary_types,
            confidence=confidence,
            all_detections=analysis.repository_types
        )
        
        # Build workflow summary
        workflow_map = {comp.component.value: True for comp in analysis.workflow_components}
        workflow_summary = WorkflowSummary(
            has_training=workflow_map.get("training", False),
            has_inference=workflow_map.get("inference", False),
            has_preprocessing=workflow_map.get("preprocessing", False),
            has_evaluation=workflow_map.get("evaluation", False),
            has_deployment=workflow_map.get("deployment", False),
            components=analysis.workflow_components
        )
        
        # Build technology stack
        primary_frameworks = [
            f.framework.value for f in analysis.frameworks[:3]
            if f.confidence in [DetectionConfidence.HIGH, DetectionConfidence.MEDIUM]
        ]
        medical_frameworks = [
            f.framework.value for f in analysis.frameworks
            if f.framework.value in ["monai", "simpleitk", "nibabel"]
        ]
        
        technology = TechnologyStack(
            primary_frameworks=primary_frameworks,
            all_frameworks=analysis.frameworks,
            medical_frameworks=medical_frameworks
        )
        
        # Build medical AI context
        is_medical = any(
            t.type.value == "medical_imaging" for t in analysis.repository_types
        )
        medical_confidence = "none"
        if is_medical:
            medical_type = next(
                (t for t in analysis.repository_types if t.type.value == "medical_imaging"),
                None
            )
            if medical_type:
                medical_confidence = medical_type.confidence.value
        
        modalities = [
            s.signal.value for s in analysis.medical_signals
            if s.signal.value in ["mri", "ct", "dicom", "nifti"]
        ]
        tasks = [
            s.signal.value for s in analysis.medical_signals
            if s.signal.value in ["segmentation", "volumetric"]
        ]
        
        medical_context = MedicalAIContext(
            is_medical_ai=is_medical,
            confidence=medical_confidence,
            detected_signals=analysis.medical_signals,
            modalities=modalities,
            tasks=tasks
        )
        
        # Build statistics
        has_tests = any("test" in f.lower() for f in [node.path for node in tree.files])
        has_ci_cd = any(
            ".github/workflows" in f or ".gitlab-ci" in f or "jenkinsfile" in f.lower()
            for f in [node.path for node in tree.files]
        )
        
        statistics = ProjectStatistics(
            total_python_files=analysis.total_python_files,
            total_notebook_files=analysis.total_notebook_files,
            total_config_files=analysis.total_config_files,
            has_requirements=analysis.has_requirements,
            has_dockerfile=analysis.has_dockerfile,
            has_readme=analysis.has_readme,
            has_tests=has_tests,
            has_ci_cd=has_ci_cd
        )
        
        # Build LLM context summary
        llm_context = self._build_llm_context(
            metadata_summary=metadata_summary,
            classification=classification,
            workflow_summary=workflow_summary,
            technology=technology,
            medical_context=medical_context,
            analysis=analysis,
            tree=tree
        )
        
        # Build unified intelligence
        return UnifiedRepositoryIntelligence(
            owner=owner,
            repo=repo,
            branch=branch,
            metadata=metadata_summary,
            structure=structure_summary,
            classification=classification,
            workflow=workflow_summary,
            technology=technology,
            medical_context=medical_context,
            statistics=statistics,
            llm_context=llm_context
        )
    
    def _build_llm_context(
        self,
        metadata_summary,
        classification,
        workflow_summary,
        technology,
        medical_context,
        analysis,
        tree
    ) -> LLMContextSummary:
        """Build LLM-optimized context summary."""
        
        # Repository overview
        repo_type = classification.primary_type.replace("_", " ").title()
        overview_parts = [f"{repo_type} repository"]
        
        if metadata_summary.description:
            overview_parts.append(f": {metadata_summary.description}")
        
        if metadata_summary.stars > 100:
            overview_parts.append(f"({metadata_summary.stars} stars)")
        
        repository_overview = " ".join(overview_parts)
        
        # Technical summary
        tech_parts = []
        if metadata_summary.primary_language:
            tech_parts.append(f"Primary language: {metadata_summary.primary_language}")
        
        if technology.primary_frameworks:
            frameworks_str = ", ".join(technology.primary_frameworks)
            tech_parts.append(f"Frameworks: {frameworks_str}")
        
        if medical_context.is_medical_ai and medical_context.modalities:
            modalities_str = ", ".join(medical_context.modalities)
            tech_parts.append(f"Medical modalities: {modalities_str}")
        
        technical_summary = ". ".join(tech_parts) if tech_parts else "General purpose repository"
        
        # Key capabilities
        capabilities = []
        
        if workflow_summary.has_training:
            capabilities.append("Model training")
        if workflow_summary.has_inference:
            capabilities.append("Inference/prediction")
        if workflow_summary.has_preprocessing:
            capabilities.append("Data preprocessing")
        if medical_context.tasks:
            for task in medical_context.tasks:
                capabilities.append(f"Medical {task}")
        
        # Important files summary
        file_summary_parts = []
        
        if analysis.key_files.get("training"):
            training_files = ", ".join(analysis.key_files["training"][:2])
            file_summary_parts.append(f"Training: {training_files}")
        
        if analysis.key_files.get("inference"):
            inference_files = ", ".join(analysis.key_files["inference"][:2])
            file_summary_parts.append(f"Inference: {inference_files}")
        
        if analysis.key_files.get("models"):
            model_files = ", ".join(analysis.key_files["models"][:2])
            file_summary_parts.append(f"Models: {model_files}")
        
        important_files_summary = ". ".join(file_summary_parts) if file_summary_parts else "No key files identified"
        
        # Suggested entry points
        entry_points = []
        
        # Add README first
        if analysis.has_readme:
            readme_files = [f.path for f in tree.files if "readme" in f.name.lower()]
            if readme_files:
                entry_points.append(readme_files[0])
        
        # Add critical files
        critical_files = tree.important_files.get("critical", [])
        for file in critical_files[:3]:
            if file.path not in entry_points:
                entry_points.append(file.path)
        
        # Add requirements
        if analysis.has_requirements:
            entry_points.append("requirements.txt")
        
        # Add main config files
        config_files = [
            f.path for f in tree.files
            if f.name.lower() in ["config.py", "config.yaml", "config.yml", "setup.py"]
        ]
        for config in config_files[:2]:
            if config not in entry_points:
                entry_points.append(config)
        
        return LLMContextSummary(
            repository_overview=repository_overview,
            technical_summary=technical_summary,
            key_capabilities=capabilities[:5],
            important_files_summary=important_files_summary,
            suggested_entry_points=entry_points[:7]
        )


# Singleton instance
_intelligence_service_instance: Optional[RepositoryIntelligenceService] = None


def get_intelligence_service() -> RepositoryIntelligenceService:
    """
    Get or create singleton RepositoryIntelligenceService instance.
    
    Returns:
        RepositoryIntelligenceService instance
    """
    global _intelligence_service_instance
    if _intelligence_service_instance is None:
        _intelligence_service_instance = RepositoryIntelligenceService()
    return _intelligence_service_instance

# Made with Bob