"""
Service to transform backend intelligence data into frontend-optimized formats.
Supports progressive loading and dynamic UI rendering.
"""
from typing import List, Dict, Any, Optional
from app.models.intelligence import UnifiedRepositoryIntelligence
from app.models.frontend import (
    FrontendRepositoryIntelligence,
    RepositoryMetadataCard,
    FrameworkVisualization,
    WorkflowNode,
    MedicalAISignalCard,
    ImportantFileHighlight,
    LoadingState,
    ProcessingProgress,
    ProcessingStage,
    ReasoningStepCard,
    MaturityBadge,
    ArchitectureInsightCard
)
from app.models.analyzer import Framework, WorkflowComponent, MedicalSignal


class FrontendTransformerService:
    """
    Transform backend intelligence into frontend-optimized structures.
    Optimized for progressive loading and cinematic UI experience.
    """
    
    # Framework metadata for visualization
    FRAMEWORK_METADATA = {
        Framework.PYTORCH: {
            "icon": "pytorch",
            "color": "#EE4C2C",
            "category": "ml"
        },
        Framework.TENSORFLOW: {
            "icon": "tensorflow",
            "color": "#FF6F00",
            "category": "ml"
        },
        Framework.MONAI: {
            "icon": "medical",
            "color": "#00A8E8",
            "category": "medical"
        },
        Framework.SIMPLEITK: {
            "icon": "medical",
            "color": "#4CAF50",
            "category": "medical"
        },
        Framework.NIBABEL: {
            "icon": "medical",
            "color": "#9C27B0",
            "category": "medical"
        },
        Framework.KERAS: {
            "icon": "keras",
            "color": "#D00000",
            "category": "ml"
        },
        Framework.SCIKIT_LEARN: {
            "icon": "scikit",
            "color": "#F7931E",
            "category": "ml"
        },
        Framework.OPENCV: {
            "icon": "opencv",
            "color": "#5C3EE8",
            "category": "data"
        }
    }
    
    # Workflow component labels
    WORKFLOW_LABELS = {
        WorkflowComponent.PREPROCESSING: "Data Preprocessing",
        WorkflowComponent.TRAINING: "Model Training",
        WorkflowComponent.INFERENCE: "Inference/Prediction",
        WorkflowComponent.EVALUATION: "Model Evaluation",
        WorkflowComponent.DEPLOYMENT: "Deployment"
    }
    
    # Medical signal descriptions
    MEDICAL_SIGNAL_DESCRIPTIONS = {
        MedicalSignal.SEGMENTATION: "Image segmentation capabilities detected",
        MedicalSignal.MRI: "MRI image processing detected",
        MedicalSignal.CT: "CT scan processing detected",
        MedicalSignal.DICOM: "DICOM format support detected",
        MedicalSignal.VOLUMETRIC: "3D volumetric processing detected",
        MedicalSignal.NIFTI: "NIfTI format support detected",
        MedicalSignal.MEDICAL_IMAGING: "General medical imaging capabilities"
    }
    
    def transform_to_frontend(
        self,
        intelligence: UnifiedRepositoryIntelligence,
        processing_time_ms: Optional[int] = None
    ) -> FrontendRepositoryIntelligence:
        """
        Transform unified intelligence to frontend-optimized format.
        
        Args:
            intelligence: Backend intelligence data
            processing_time_ms: Total processing time in milliseconds
            
        Returns:
            Frontend-optimized intelligence response
        """
        return FrontendRepositoryIntelligence(
            loading_state=LoadingState.SUCCESS,
            processing_progress=ProcessingProgress(
                stage=ProcessingStage.COMPLETE,
                progress=100,
                message="Analysis complete",
                estimated_time_remaining=0
            ),
            owner=intelligence.owner,
            repo=intelligence.repo,
            branch=intelligence.branch,
            metadata_card=self._create_metadata_card(intelligence),
            frameworks=self._create_framework_visualizations(intelligence),
            workflow_nodes=self._create_workflow_nodes(intelligence),
            medical_signals=self._create_medical_signal_cards(intelligence),
            important_files=self._create_important_file_highlights(intelligence),
            classification=self._create_classification_summary(intelligence),
            statistics=self._create_statistics_summary(intelligence),
            ai_reasoning=self._create_ai_reasoning(intelligence),
            maturity_badge=self._create_maturity_badge(intelligence),
            maturity_indicators=self._create_maturity_indicators(intelligence),
            architecture_insights=self._create_architecture_insights(intelligence),
            executive_summary=self._create_executive_summary_dict(intelligence),
            llm_summary=intelligence.llm_context.repository_overview,
            analyzed_at=intelligence.analyzed_at,
            processing_time_ms=processing_time_ms
        )
    
    def _create_metadata_card(
        self,
        intelligence: UnifiedRepositoryIntelligence
    ) -> RepositoryMetadataCard:
        """Create metadata card for frontend display."""
        metadata = intelligence.metadata
        return RepositoryMetadataCard(
            name=metadata.name,
            owner=intelligence.owner,
            description=metadata.description,
            stars=metadata.stars,
            forks=metadata.forks,
            language=metadata.primary_language,
            topics=metadata.topics,
            avatar_url=None,  # Can be added from owner info if needed
            html_url=metadata.html_url,
            updated_at=metadata.updated_at
        )
    
    def _create_framework_visualizations(
        self,
        intelligence: UnifiedRepositoryIntelligence
    ) -> List[FrameworkVisualization]:
        """Create framework visualizations for frontend."""
        visualizations = []
        
        for framework_detection in intelligence.technology.all_frameworks:
            framework = framework_detection.framework
            metadata = self.FRAMEWORK_METADATA.get(framework, {
                "icon": "default",
                "color": "#666666",
                "category": "other"
            })
            
            visualizations.append(FrameworkVisualization(
                name=framework.value.replace("_", " ").title(),
                confidence=framework_detection.confidence.value,
                category=metadata["category"],
                icon=metadata["icon"],
                color=metadata["color"],
                evidence_count=len(framework_detection.evidence)
            ))
        
        return visualizations
    
    def _create_workflow_nodes(
        self,
        intelligence: UnifiedRepositoryIntelligence
    ) -> List[WorkflowNode]:
        """Create workflow nodes for graph visualization."""
        nodes = []
        
        for workflow_detection in intelligence.workflow.components:
            component = workflow_detection.component
            
            nodes.append(WorkflowNode(
                id=component.value,
                label=self.WORKFLOW_LABELS.get(component, component.value.title()),
                type=component.value,
                confidence=workflow_detection.confidence.value,
                files=workflow_detection.evidence[:5],  # Limit to 5 files
                has_implementation=len(workflow_detection.evidence) > 0
            ))
        
        return nodes
    
    def _create_medical_signal_cards(
        self,
        intelligence: UnifiedRepositoryIntelligence
    ) -> List[MedicalAISignalCard]:
        """Create medical AI signal cards for visualization."""
        cards = []
        
        for signal_detection in intelligence.medical_context.detected_signals:
            signal = signal_detection.signal
            
            cards.append(MedicalAISignalCard(
                signal_type=signal.value.replace("_", " ").upper(),
                confidence=signal_detection.confidence.value,
                description=self.MEDICAL_SIGNAL_DESCRIPTIONS.get(
                    signal,
                    f"{signal.value} detected in repository"
                ),
                evidence=signal_detection.evidence[:3],  # Limit to 3 files
                icon=self._get_medical_signal_icon(signal)
            ))
        
        return cards
    
    def _get_medical_signal_icon(self, signal: MedicalSignal) -> str:
        """Get icon identifier for medical signal."""
        icon_map = {
            MedicalSignal.SEGMENTATION: "scissors",
            MedicalSignal.MRI: "brain-scan",
            MedicalSignal.CT: "ct-scan",
            MedicalSignal.DICOM: "medical-file",
            MedicalSignal.VOLUMETRIC: "cube",
            MedicalSignal.NIFTI: "file-medical",
            MedicalSignal.MEDICAL_IMAGING: "hospital"
        }
        return icon_map.get(signal, "medical")
    
    def _create_important_file_highlights(
        self,
        intelligence: UnifiedRepositoryIntelligence
    ) -> List[ImportantFileHighlight]:
        """Create important file highlights with context."""
        highlights = []
        
        # Add critical files
        for file_node in intelligence.structure.critical_files[:10]:  # Limit to 10
            highlights.append(ImportantFileHighlight(
                path=file_node.path,
                name=file_node.name,
                importance="critical",
                category=self._categorize_file(file_node.name),
                description=self._describe_file(file_node.name),
                size=file_node.size
            ))
        
        # Add high importance files
        for file_node in intelligence.structure.high_importance_files[:10]:  # Limit to 10
            highlights.append(ImportantFileHighlight(
                path=file_node.path,
                name=file_node.name,
                importance="high",
                category=self._categorize_file(file_node.name),
                description=self._describe_file(file_node.name),
                size=file_node.size
            ))
        
        return highlights
    
    def _categorize_file(self, filename: str) -> str:
        """Categorize file based on name."""
        filename_lower = filename.lower()
        
        if "train" in filename_lower:
            return "training"
        elif "infer" in filename_lower or "predict" in filename_lower:
            return "inference"
        elif "model" in filename_lower:
            return "model"
        elif "config" in filename_lower or filename_lower.endswith((".yaml", ".yml", ".json")):
            return "configuration"
        elif filename_lower == "requirements.txt":
            return "dependencies"
        elif filename_lower.startswith("readme"):
            return "documentation"
        elif "test" in filename_lower:
            return "testing"
        elif "docker" in filename_lower:
            return "deployment"
        else:
            return "other"
    
    def _describe_file(self, filename: str) -> str:
        """Generate description for file."""
        filename_lower = filename.lower()
        
        descriptions = {
            "train.py": "Main training script for model training",
            "infer.py": "Inference script for model predictions",
            "model.py": "Model architecture definition",
            "requirements.txt": "Python dependencies and packages",
            "readme.md": "Project documentation and overview",
            "config.yaml": "Configuration file for project settings",
            "dockerfile": "Docker container configuration",
            "setup.py": "Package installation configuration"
        }
        
        # Check exact matches
        if filename_lower in descriptions:
            return descriptions[filename_lower]
        
        # Check partial matches
        if "train" in filename_lower:
            return "Training-related script or module"
        elif "infer" in filename_lower or "predict" in filename_lower:
            return "Inference or prediction script"
        elif "model" in filename_lower:
            return "Model definition or architecture"
        elif "config" in filename_lower:
            return "Configuration file"
        elif "test" in filename_lower:
            return "Test file or test suite"
        else:
            return f"Project file: {filename}"
    
    def _create_classification_summary(
        self,
        intelligence: UnifiedRepositoryIntelligence
    ) -> Dict[str, Any]:
        """Create classification summary for frontend."""
        return {
            "primary_type": intelligence.classification.primary_type,
            "secondary_types": intelligence.classification.secondary_types,
            "confidence": intelligence.classification.confidence,
            "is_medical_ai": intelligence.medical_context.is_medical_ai,
            "medical_confidence": intelligence.medical_context.confidence
        }
    
    def _create_statistics_summary(
        self,
        intelligence: UnifiedRepositoryIntelligence
    ) -> Dict[str, Any]:
        """Create statistics summary for frontend."""
        return {
            "total_files": intelligence.structure.total_files,
            "filtered_files": intelligence.structure.filtered_files,
            "python_files": intelligence.statistics.total_python_files,
            "notebook_files": intelligence.statistics.total_notebook_files,
            "config_files": intelligence.statistics.total_config_files,
            "has_requirements": intelligence.statistics.has_requirements,
            "has_dockerfile": intelligence.statistics.has_dockerfile,
            "has_readme": intelligence.statistics.has_readme,
            "has_tests": intelligence.statistics.has_tests,
            "has_ci_cd": intelligence.statistics.has_ci_cd
        }
    
    def _create_ai_reasoning(
        self,
        intelligence: UnifiedRepositoryIntelligence
    ) -> Optional[Dict[str, Any]]:
        """Create AI reasoning data for frontend."""
        if not intelligence.ai_reasoning:
            return None
        
        reasoning = intelligence.ai_reasoning
        return {
            "classification_reasoning": [
                {
                    "category": step.category,
                    "title": step.title,
                    "explanation": step.explanation,
                    "evidence": step.evidence,
                    "confidence_impact": step.confidence_impact
                }
                for step in reasoning.classification_reasoning
            ],
            "framework_reasoning": [
                {
                    "category": step.category,
                    "title": step.title,
                    "explanation": step.explanation,
                    "evidence": step.evidence,
                    "confidence_impact": step.confidence_impact
                }
                for step in reasoning.framework_reasoning
            ],
            "workflow_reasoning": [
                {
                    "category": step.category,
                    "title": step.title,
                    "explanation": step.explanation,
                    "evidence": step.evidence,
                    "confidence_impact": step.confidence_impact
                }
                for step in reasoning.workflow_reasoning
            ],
            "medical_reasoning": [
                {
                    "category": step.category,
                    "title": step.title,
                    "explanation": step.explanation,
                    "evidence": step.evidence,
                    "confidence_impact": step.confidence_impact
                }
                for step in reasoning.medical_reasoning
            ],
            "summary": reasoning.summary
        }
    
    def _create_maturity_badge(
        self,
        intelligence: UnifiedRepositoryIntelligence
    ) -> Optional[MaturityBadge]:
        """Create maturity badge for frontend."""
        if not intelligence.maturity:
            return None
        
        maturity = intelligence.maturity
        
        # Map maturity levels to colors and labels
        level_config = {
            "production_ready": {
                "label": "Production Ready",
                "color": "#10B981",
                "description": "Enterprise-grade, production-ready repository"
            },
            "enterprise_scale": {
                "label": "Enterprise Scale",
                "color": "#3B82F6",
                "description": "Scalable architecture suitable for enterprise use"
            },
            "research_grade": {
                "label": "Research Grade",
                "color": "#8B5CF6",
                "description": "Well-structured research repository"
            },
            "prototype": {
                "label": "Prototype",
                "color": "#F59E0B",
                "description": "Functional prototype with room for improvement"
            },
            "experimental": {
                "label": "Experimental",
                "color": "#6B7280",
                "description": "Early-stage experimental project"
            }
        }
        
        config = level_config.get(maturity.level, level_config["experimental"])
        
        return MaturityBadge(
            level=maturity.level,
            score=maturity.score,
            label=config["label"],
            color=config["color"],
            description=config["description"]
        )
    
    def _create_maturity_indicators(
        self,
        intelligence: UnifiedRepositoryIntelligence
    ) -> List[Dict[str, Any]]:
        """Create maturity indicators for frontend."""
        if not intelligence.maturity:
            return []
        
        return [
            {
                "name": indicator.name,
                "status": indicator.status,
                "impact": indicator.impact,
                "description": indicator.description
            }
            for indicator in intelligence.maturity.indicators
        ]
    
    def _create_architecture_insights(
        self,
        intelligence: UnifiedRepositoryIntelligence
    ) -> List[ArchitectureInsightCard]:
        """Create architecture insight cards for frontend."""
        if not intelligence.architecture:
            return []
        
        # Icon mapping for insight types
        icon_map = {
            "modularity": "cube",
            "configuration": "settings",
            "scalability": "trending-up",
            "deployment": "rocket",
            "research": "flask",
            "data_pipeline": "database"
        }
        
        return [
            ArchitectureInsightCard(
                insight_type=insight.insight_type,
                title=insight.title,
                description=insight.description,
                evidence=insight.evidence,
                significance=insight.significance,
                icon=icon_map.get(insight.insight_type, "info")
            )
            for insight in intelligence.architecture.insights
        ]
    
    def _create_executive_summary_dict(
        self,
        intelligence: UnifiedRepositoryIntelligence
    ) -> Optional[Dict[str, Any]]:
        """Create executive summary dictionary for frontend."""
        if not intelligence.executive_summary:
            return None
        
        summary = intelligence.executive_summary
        return {
            "headline": summary.headline,
            "overview": summary.overview,
            "key_highlights": summary.key_highlights,
            "technical_profile": summary.technical_profile,
            "use_cases": summary.use_cases,
            "target_audience": summary.target_audience
        }


# Singleton instance
_transformer_service: Optional[FrontendTransformerService] = None


def get_frontend_transformer() -> FrontendTransformerService:
    """Get singleton instance of frontend transformer service."""
    global _transformer_service
    if _transformer_service is None:
        _transformer_service = FrontendTransformerService()
    return _transformer_service


# Made with Bob