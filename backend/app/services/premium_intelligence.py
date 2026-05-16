"""
Premium intelligence service for advanced repository analysis.
Generates AI reasoning, maturity assessment, architecture insights, and executive summaries.
Uses lightweight heuristics without external LLM APIs.
"""
from typing import List, Dict, Optional
from app.models.intelligence import (
    AIReasoning,
    ReasoningStep,
    RepositoryMaturity,
    MaturityIndicator,
    ArchitectureAnalysis,
    ArchitectureInsight,
    ExecutiveSummary,
    UnifiedRepositoryIntelligence
)
from app.models.analyzer import DetectionConfidence


class PremiumIntelligenceService:
    """
    Service for generating premium intelligence features.
    
    Features:
    - AI Reasoning: Explains WHY classifications were made
    - Maturity Assessment: Evaluates repository production-readiness
    - Architecture Insights: Identifies architectural patterns
    - Executive Summary: Generates investor/demo-ready summaries
    """
    
    def enhance_intelligence(
        self,
        intelligence: UnifiedRepositoryIntelligence
    ) -> UnifiedRepositoryIntelligence:
        """
        Enhance intelligence with premium features.
        
        Args:
            intelligence: Base intelligence from intelligence service
            
        Returns:
            Enhanced intelligence with premium features
        """
        # Generate AI reasoning
        intelligence.ai_reasoning = self._generate_ai_reasoning(intelligence)
        
        # Assess repository maturity
        intelligence.maturity = self._assess_maturity(intelligence)
        
        # Analyze architecture
        intelligence.architecture = self._analyze_architecture(intelligence)
        
        # Generate executive summary
        intelligence.executive_summary = self._generate_executive_summary(intelligence)
        
        return intelligence
    
    def _generate_ai_reasoning(
        self,
        intelligence: UnifiedRepositoryIntelligence
    ) -> AIReasoning:
        """Generate AI reasoning explaining detection decisions."""
        classification_steps = []
        framework_steps = []
        workflow_steps = []
        medical_steps = []
        
        # Classification reasoning
        if intelligence.classification.all_detections:
            primary = intelligence.classification.all_detections[0]
            
            # Primary classification
            classification_steps.append(ReasoningStep(
                category="classification",
                title=f"Primary Classification: {primary.type.value.replace('_', ' ').title()}",
                explanation=primary.explanation if hasattr(primary, 'explanation') else f"Detected as {primary.type.value} based on file patterns and framework usage",
                evidence=primary.evidence[:3],
                confidence_impact="positive" if primary.confidence == DetectionConfidence.HIGH else "neutral"
            ))
            
            # Score explanation
            if hasattr(primary, 'score') and primary.score:
                classification_steps.append(ReasoningStep(
                    category="classification",
                    title="Confidence Score Analysis",
                    explanation=f"Classification score: {primary.score:.1f}. High scores indicate strong pattern matches across multiple indicators.",
                    evidence=[],
                    confidence_impact="positive" if primary.score >= 30 else "neutral"
                ))
            
            # Secondary classifications
            if len(intelligence.classification.all_detections) > 1:
                secondary = intelligence.classification.all_detections[1]
                classification_steps.append(ReasoningStep(
                    category="classification",
                    title=f"Secondary Pattern: {secondary.type.value.replace('_', ' ').title()}",
                    explanation=f"Also shows characteristics of {secondary.type.value}, indicating multi-domain capabilities",
                    evidence=secondary.evidence[:2],
                    confidence_impact="neutral"
                ))
        
        # Framework reasoning
        high_conf_frameworks = [
            f for f in intelligence.technology.all_frameworks
            if f.confidence == DetectionConfidence.HIGH
        ]
        
        if high_conf_frameworks:
            fw = high_conf_frameworks[0]
            framework_steps.append(ReasoningStep(
                category="framework",
                title=f"Primary Framework: {fw.framework.value.title()}",
                explanation=f"Strong {fw.framework.value} presence detected through imports, file patterns, and model artifacts",
                evidence=fw.evidence[:3],
                confidence_impact="positive"
            ))
        
        if len(intelligence.technology.all_frameworks) > 1:
            framework_steps.append(ReasoningStep(
                category="framework",
                title="Multi-Framework Architecture",
                explanation=f"Uses {len(intelligence.technology.all_frameworks)} frameworks, indicating a flexible tech stack",
                evidence=[f.framework.value for f in intelligence.technology.all_frameworks[:3]],
                confidence_impact="neutral"
            ))
        
        # Workflow reasoning
        workflow_components = intelligence.workflow.components
        if workflow_components:
            high_conf_workflow = [w for w in workflow_components if w.confidence == DetectionConfidence.HIGH]
            
            if high_conf_workflow:
                wf = high_conf_workflow[0]
                workflow_steps.append(ReasoningStep(
                    category="workflow",
                    title=f"{wf.component.value.title()} Pipeline Detected",
                    explanation=f"Complete {wf.component.value} implementation found with dedicated files and structure",
                    evidence=wf.evidence[:3],
                    confidence_impact="positive"
                ))
            
            # Complete pipeline check
            has_training = intelligence.workflow.has_training
            has_inference = intelligence.workflow.has_inference
            
            if has_training and has_inference:
                workflow_steps.append(ReasoningStep(
                    category="workflow",
                    title="End-to-End ML Pipeline",
                    explanation="Repository contains both training and inference capabilities, indicating production-ready workflow",
                    evidence=["training pipeline", "inference pipeline"],
                    confidence_impact="positive"
                ))
        
        # Medical AI reasoning
        if intelligence.medical_context.is_medical_ai:
            medical_steps.append(ReasoningStep(
                category="medical",
                title="Medical AI Repository Confirmed",
                explanation=f"Strong medical imaging indicators with {intelligence.medical_context.confidence} confidence",
                evidence=intelligence.medical_context.modalities[:3],
                confidence_impact="positive"
            ))
            
            if intelligence.medical_context.detected_signals:
                signal = intelligence.medical_context.detected_signals[0]
                medical_steps.append(ReasoningStep(
                    category="medical",
                    title=f"{signal.signal.value.upper()} Processing Detected",
                    explanation=signal.explanation if hasattr(signal, 'explanation') else f"Specialized {signal.signal.value} handling capabilities",
                    evidence=signal.evidence[:3],
                    confidence_impact="positive"
                ))
        
        # Generate summary
        summary_parts = []
        if classification_steps:
            summary_parts.append(f"Classified as {intelligence.classification.primary_type.replace('_', ' ')}")
        if high_conf_frameworks:
            summary_parts.append(f"using {high_conf_frameworks[0].framework.value}")
        if intelligence.workflow.has_training and intelligence.workflow.has_inference:
            summary_parts.append("with complete ML pipeline")
        
        summary = " ".join(summary_parts) if summary_parts else "General repository analysis"
        
        return AIReasoning(
            classification_reasoning=classification_steps,
            framework_reasoning=framework_steps,
            workflow_reasoning=workflow_steps,
            medical_reasoning=medical_steps,
            summary=summary
        )
    
    def _assess_maturity(
        self,
        intelligence: UnifiedRepositoryIntelligence
    ) -> RepositoryMaturity:
        """Assess repository maturity level."""
        indicators = []
        score = 0.0
        strengths = []
        gaps = []
        
        # Check tests
        if intelligence.statistics.has_tests:
            indicators.append(MaturityIndicator(
                name="Test Suite",
                status="present",
                impact="high",
                description="Automated testing infrastructure in place"
            ))
            score += 20
            strengths.append("Comprehensive test coverage")
        else:
            indicators.append(MaturityIndicator(
                name="Test Suite",
                status="absent",
                impact="high",
                description="No test files detected"
            ))
            gaps.append("Add automated tests")
        
        # Check CI/CD
        if intelligence.statistics.has_ci_cd:
            indicators.append(MaturityIndicator(
                name="CI/CD Pipeline",
                status="present",
                impact="high",
                description="Continuous integration and deployment configured"
            ))
            score += 20
            strengths.append("Automated CI/CD pipeline")
        else:
            gaps.append("Implement CI/CD automation")
        
        # Check Docker
        if intelligence.statistics.has_dockerfile:
            indicators.append(MaturityIndicator(
                name="Containerization",
                status="present",
                impact="high",
                description="Docker support for consistent deployment"
            ))
            score += 15
            strengths.append("Containerized deployment")
        else:
            gaps.append("Add Docker support")
        
        # Check documentation
        if intelligence.statistics.has_readme:
            indicators.append(MaturityIndicator(
                name="Documentation",
                status="present",
                impact="medium",
                description="README documentation available"
            ))
            score += 10
            strengths.append("Well-documented")
        else:
            gaps.append("Add comprehensive documentation")
        
        # Check requirements
        if intelligence.statistics.has_requirements:
            indicators.append(MaturityIndicator(
                name="Dependency Management",
                status="present",
                impact="medium",
                description="Dependencies clearly specified"
            ))
            score += 10
        else:
            gaps.append("Specify dependencies")
        
        # Check deployment capability
        has_deployment = intelligence.workflow.has_deployment
        if has_deployment:
            indicators.append(MaturityIndicator(
                name="Deployment Ready",
                status="present",
                impact="high",
                description="Deployment infrastructure detected"
            ))
            score += 15
            strengths.append("Deployment-ready architecture")
        
        # Check configuration management
        if intelligence.statistics.total_config_files > 0:
            indicators.append(MaturityIndicator(
                name="Configuration Management",
                status="present",
                impact="medium",
                description="Structured configuration files"
            ))
            score += 10
        
        # Determine maturity level
        if score >= 80:
            level = "production_ready"
            confidence = "high"
        elif score >= 60:
            level = "enterprise_scale"
            confidence = "high"
        elif score >= 40:
            level = "research_grade"
            confidence = "medium"
        elif score >= 20:
            level = "prototype"
            confidence = "medium"
        else:
            level = "experimental"
            confidence = "low"
        
        # Generate summary
        summary = f"{level.replace('_', ' ').title()} repository with {len(strengths)} key strengths"
        if gaps:
            summary += f" and {len(gaps)} improvement areas"
        
        return RepositoryMaturity(
            level=level,
            score=score,
            confidence=confidence,
            indicators=indicators,
            strengths=strengths[:5],
            gaps=gaps[:5],
            summary=summary
        )
    
    def _analyze_architecture(
        self,
        intelligence: UnifiedRepositoryIntelligence
    ) -> ArchitectureAnalysis:
        """Analyze repository architecture patterns."""
        insights = []
        patterns = []
        
        # Check for modular architecture
        if intelligence.statistics.total_python_files > 10:
            insights.append(ArchitectureInsight(
                insight_type="modularity",
                title="Modular Architecture",
                description=f"Well-structured codebase with {intelligence.statistics.total_python_files} Python modules",
                evidence=[f"{intelligence.statistics.total_python_files} Python files"],
                significance="high"
            ))
            patterns.append("Modular Design")
        
        # Check for config-driven approach
        if intelligence.statistics.total_config_files > 3:
            insights.append(ArchitectureInsight(
                insight_type="configuration",
                title="Config-Driven Pipeline",
                description="Extensive use of configuration files for flexible parameter management",
                evidence=[f"{intelligence.statistics.total_config_files} config files"],
                significance="medium"
            ))
            patterns.append("Configuration-Driven")
        
        # Check for distributed training support
        has_training = intelligence.workflow.has_training
        if has_training and intelligence.statistics.total_python_files > 20:
            insights.append(ArchitectureInsight(
                insight_type="scalability",
                title="Distributed Training Support",
                description="Architecture suggests support for scalable training workflows",
                evidence=["training pipeline", "modular structure"],
                significance="high"
            ))
            patterns.append("Distributed Training")
        
        # Check for deployment readiness
        if intelligence.workflow.has_deployment:
            insights.append(ArchitectureInsight(
                insight_type="deployment",
                title="Deployment-Ready Structure",
                description="Contains deployment infrastructure and serving capabilities",
                evidence=["deployment components"],
                significance="high"
            ))
            patterns.append("Production Deployment")
        
        # Check for research orientation
        if intelligence.statistics.total_notebook_files > 5:
            insights.append(ArchitectureInsight(
                insight_type="research",
                title="Research-Oriented Repository",
                description=f"Extensive use of notebooks ({intelligence.statistics.total_notebook_files}) for experimentation",
                evidence=[f"{intelligence.statistics.total_notebook_files} notebooks"],
                significance="medium"
            ))
            patterns.append("Research & Experimentation")
        
        # Check for preprocessing pipeline
        if intelligence.workflow.has_preprocessing:
            insights.append(ArchitectureInsight(
                insight_type="data_pipeline",
                title="Data Preprocessing Pipeline",
                description="Dedicated data preprocessing and transformation infrastructure",
                evidence=["preprocessing components"],
                significance="medium"
            ))
            patterns.append("Data Pipeline")
        
        # Generate summary
        if patterns:
            summary = f"Architecture follows {', '.join(patterns[:3])} patterns"
        else:
            summary = "Standard repository structure"
        
        return ArchitectureAnalysis(
            insights=insights[:6],
            patterns=patterns[:5],
            summary=summary
        )
    
    def _generate_executive_summary(
        self,
        intelligence: UnifiedRepositoryIntelligence
    ) -> ExecutiveSummary:
        """Generate executive-style summary."""
        # Generate headline
        repo_type = intelligence.classification.primary_type.replace('_', ' ').title()
        primary_framework = ""
        if intelligence.technology.primary_frameworks:
            primary_framework = intelligence.technology.primary_frameworks[0].title()
        
        if primary_framework:
            headline = f"{repo_type} Platform Built with {primary_framework}"
        else:
            headline = f"Advanced {repo_type} Solution"
        
        # Generate overview
        overview_parts = []
        overview_parts.append(f"This repository implements a {repo_type.lower()} solution")
        
        if intelligence.medical_context.is_medical_ai:
            modalities = ", ".join(intelligence.medical_context.modalities[:2])
            overview_parts.append(f"specialized in {modalities} processing")
        
        if intelligence.workflow.has_training and intelligence.workflow.has_inference:
            overview_parts.append("with complete end-to-end ML pipeline capabilities")
        
        if intelligence.metadata.stars > 100:
            overview_parts.append(f"Backed by strong community support ({intelligence.metadata.stars} stars)")
        
        overview = ". ".join(overview_parts) + "."
        
        # Key highlights
        highlights = []
        
        if intelligence.maturity and intelligence.maturity.level in ["production_ready", "enterprise_scale"]:
            highlights.append(f"{intelligence.maturity.level.replace('_', ' ').title()} maturity level")
        
        if intelligence.technology.primary_frameworks:
            frameworks_str = ", ".join(intelligence.technology.primary_frameworks[:2])
            highlights.append(f"Built on {frameworks_str}")
        
        if intelligence.workflow.has_training:
            highlights.append("Complete training pipeline")
        
        if intelligence.workflow.has_deployment:
            highlights.append("Production deployment ready")
        
        if intelligence.statistics.has_tests:
            highlights.append("Comprehensive test coverage")
        
        # Technical profile
        tech_parts = []
        if intelligence.metadata.primary_language:
            tech_parts.append(f"Primary language: {intelligence.metadata.primary_language}")
        
        if intelligence.technology.primary_frameworks:
            tech_parts.append(f"Frameworks: {', '.join(intelligence.technology.primary_frameworks[:3])}")
        
        if intelligence.statistics.total_python_files > 0:
            tech_parts.append(f"{intelligence.statistics.total_python_files} Python modules")
        
        technical_profile = ". ".join(tech_parts) if tech_parts else "Modern technology stack"
        
        # Use cases
        use_cases = []
        
        if intelligence.medical_context.is_medical_ai:
            use_cases.append("Medical image analysis and diagnosis support")
            use_cases.append("Clinical research and healthcare AI applications")
        elif "nlp" in intelligence.classification.primary_type.lower():
            use_cases.append("Natural language processing and text analysis")
            use_cases.append("Language model development and fine-tuning")
        elif "computer_vision" in intelligence.classification.primary_type.lower():
            use_cases.append("Image recognition and visual analysis")
            use_cases.append("Computer vision model development")
        else:
            use_cases.append("Machine learning research and development")
            use_cases.append("AI model training and deployment")
        
        # Target audience
        if intelligence.maturity and intelligence.maturity.level == "production_ready":
            target_audience = "Enterprise teams and production ML engineers"
        elif intelligence.statistics.total_notebook_files > 5:
            target_audience = "Researchers and data scientists"
        else:
            target_audience = "ML practitioners and developers"
        
        return ExecutiveSummary(
            headline=headline,
            overview=overview,
            key_highlights=highlights[:5],
            technical_profile=technical_profile,
            use_cases=use_cases[:3],
            target_audience=target_audience
        )


# Singleton instance
_premium_intelligence_service: Optional[PremiumIntelligenceService] = None


def get_premium_intelligence_service() -> PremiumIntelligenceService:
    """Get or create singleton PremiumIntelligenceService instance."""
    global _premium_intelligence_service
    if _premium_intelligence_service is None:
        _premium_intelligence_service = PremiumIntelligenceService()
    return _premium_intelligence_service


# Made with Bob