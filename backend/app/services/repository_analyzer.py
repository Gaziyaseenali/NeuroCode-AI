"""
Lightweight repository structure analyzer service with weighted multi-domain classification.
Uses rule-based analysis with evidence scoring to detect repository type, frameworks, and workflow components.
Optimized for low RAM usage and hackathon MVP simplicity.
"""
import re
from typing import List, Dict, Set, Tuple, Optional
from app.models.github import RepositoryTree, TreeNode
from app.models.analyzer import (
    RepositoryIntelligence,
    RepositoryType,
    RepositoryTypeDetection,
    WorkflowComponent,
    WorkflowDetection,
    Framework,
    FrameworkDetection,
    MedicalSignal,
    MedicalSignalDetection,
    DetectionConfidence
)


class RepositoryAnalyzer:
    """
    Lightweight rule-based repository analyzer with weighted multi-domain scoring.
    
    Features:
    - Weighted evidence scoring for accurate classification
    - Multi-domain detection (NLP, CV, Medical, etc.)
    - Primary and secondary category support
    - Confidence calibration based on evidence strength
    - Medical imaging requires strong medical evidence
    - Identifies AI/ML frameworks (PyTorch, TensorFlow, MONAI, etc.)
    - Detects workflow components (training, inference, evaluation, etc.)
    - Uses only file paths and names (no file content analysis)
    - Optimized for low RAM usage
    """
    
    # Framework detection patterns
    FRAMEWORK_PATTERNS = {
        Framework.PYTORCH: {
            'files': ['torch', 'pytorch'],
            'imports': ['torch', 'pytorch'],
            'extensions': ['.pth', '.pt'],
            'keywords': ['torch', 'pytorch', 'nn.module']
        },
        Framework.TENSORFLOW: {
            'files': ['tensorflow', 'tf_'],
            'imports': ['tensorflow', 'tf.'],
            'extensions': ['.pb', '.h5', '.tflite'],
            'keywords': ['tensorflow', 'keras', 'tf.keras']
        },
        Framework.MONAI: {
            'files': ['monai'],
            'imports': ['monai'],
            'keywords': ['monai', 'medical', 'imaging']
        },
        Framework.SIMPLEITK: {
            'files': ['simpleitk', 'sitk'],
            'imports': ['simpleitk', 'sitk'],
            'keywords': ['simpleitk', 'sitk']
        },
        Framework.NIBABEL: {
            'files': ['nibabel', 'nib'],
            'imports': ['nibabel', 'nib'],
            'extensions': ['.nii', '.nii.gz'],
            'keywords': ['nibabel', 'nifti']
        },
        Framework.KERAS: {
            'files': ['keras'],
            'imports': ['keras'],
            'keywords': ['keras', 'model.fit']
        },
        Framework.SCIKIT_LEARN: {
            'files': ['sklearn', 'scikit'],
            'imports': ['sklearn', 'scikit'],
            'keywords': ['sklearn', 'scikit-learn']
        },
        Framework.OPENCV: {
            'files': ['cv2', 'opencv'],
            'imports': ['cv2', 'opencv'],
            'keywords': ['opencv', 'cv2']
        }
    }
    
    # Weak evidence patterns to filter out (documentation, assets, etc.)
    WEAK_EVIDENCE_PATTERNS = [
        r'/docs?/',
        r'/documentation/',
        r'/examples?/',
        r'/tutorials?/',
        r'/assets?/',
        r'/images?/',
        r'/screenshots?/',
        r'\.md$',
        r'\.txt$',
        r'\.rst$',
        r'/readme',
        r'/changelog',
        r'/license',
        r'\.png$',
        r'\.jpg$',
        r'\.jpeg$',
        r'\.gif$',
        r'\.svg$',
        r'/static/',
        r'/public/',
        r'/__pycache__/',
        r'/\.git/',
        r'/node_modules/',
        r'/dist/',
        r'/build/'
    ]
    
    # Strong evidence patterns (actual code/config files)
    STRONG_EVIDENCE_PATTERNS = [
        r'requirements\.txt$',
        r'setup\.py$',
        r'pyproject\.toml$',
        r'package\.json$',
        r'Pipfile$',
        r'environment\.yml$',
        r'conda\.yml$',
        r'\.py$',
        r'\.ipynb$',
        r'/src/',
        r'/lib/',
        r'/models?/',
        r'/train',
        r'/inference'
    ]
    
    # RL-specific contextual requirements
    RL_CONTEXT_REQUIREMENTS = {
        'frameworks': ['gym', 'gymnasium', 'stable_baselines', 'stable-baselines3', 'ray', 'rllib'],
        'strong_keywords': [r'\bgym\b', r'\bgymnasium\b', r'\bstable.baselines\b', r'\breplay.buffer\b',
                           r'\bppo\b', r'\bdqn\b', r'\bsac\b', r'\ba3c\b', r'\bddpg\b', r'\btd3\b',
                           r'\benvironment\.step\b', r'\benvironment\.reset\b', r'\bagent\.train\b'],
        'files': ['replay_buffer', 'environment', 'agent_train', 'rl_train', 'policy_network'],
        'min_matches': 3  # Require at least 3 strong RL indicators
    }
    
    # Workflow component patterns
    WORKFLOW_PATTERNS = {
        WorkflowComponent.PREPROCESSING: {
            'files': ['preprocess', 'preprocessing', 'data_prep', 'augment', 'transform'],
            'keywords': ['preprocess', 'augment', 'transform', 'normalize']
        },
        WorkflowComponent.TRAINING: {
            'files': ['train', 'trainer', 'training', 'fit'],
            'keywords': ['train', 'fit', 'epoch', 'optimizer']
        },
        WorkflowComponent.INFERENCE: {
            'files': ['infer', 'inference', 'predict', 'prediction', 'test'],
            'keywords': ['infer', 'predict', 'test', 'evaluate']
        },
        WorkflowComponent.EVALUATION: {
            'files': ['eval', 'evaluate', 'evaluation', 'metric', 'metrics', 'validate', 'validation'],
            'keywords': ['evaluate', 'metric', 'accuracy', 'loss', 'score']
        },
        WorkflowComponent.DEPLOYMENT: {
            'files': ['deploy', 'deployment', 'serve', 'api', 'app', 'docker'],
            'keywords': ['deploy', 'serve', 'api', 'docker', 'kubernetes']
        }
    }
    
    # Medical AI signal patterns with weighted evidence scoring
    # HIGH VALUE: Strong medical imaging indicators
    # MEDIUM VALUE: Medical context indicators
    # LOW VALUE: Weak/generic indicators
    MEDICAL_EVIDENCE_WEIGHTS = {
        # HIGH VALUE EVIDENCE (+10 points)
        'high': {
            'keywords': [r'\bdicom\b', r'\bpydicom\b', r'\bnibabel\b', r'\bmonai\b',
                        r'\bnifti\b', r'\bnii\.gz\b', r'\bradiology\b', r'\bradiomics\b',
                        r'\bmedical\s+imaging\b', r'\bct\s+scan\b', r'\bmri\s+scan\b'],
            'weight': 10
        },
        # MEDIUM VALUE EVIDENCE (+5 points)
        'medium': {
            'keywords': [r'\bsegmentation\b', r'\bvolumetric\b', r'\bmedical\s+dataset\b',
                        r'\b3d\s+imaging\b', r'\bmedical\s+image\b', r'\bclinical\b'],
            'weight': 5
        },
        # LOW VALUE EVIDENCE (+2 points)
        'low': {
            'keywords': [r'\bmask\b', r'\bslice\b', r'\bscan\b', r'\bvolume\b'],
            'weight': 2
        }
    }
    
    # Specific signal requirements with corroborating evidence
    MEDICAL_SIGNAL_REQUIREMENTS = {
        MedicalSignal.MRI: {
            'primary_patterns': [r'\bmri\b', r'\bfmri\b', r'\bmagnetic\s+resonance\b'],
            'corroborating': [r'\bnifti\b', r'\bnibabel\b', r'\bmonai\b', r'\bt1\b', r'\bt2\b',
                            r'\bflair\b', r'\bmedical\s+imaging\b', r'\bradiology\b', r'\bbrain\b',
                            r'\.nii\b', r'\bnii\.gz\b'],
            'min_score': 12
        },
        MedicalSignal.CT: {
            'primary_patterns': [r'\bct\s+scan\b', r'\bcomputed\s+tomography\b', r'\bct\b'],
            'corroborating': [r'\bdicom\b', r'\bradiology\b', r'\bhounsfield\b',
                            r'\bmedical\s+imaging\b', r'\bpydicom\b', r'\bsegmentation\b'],
            'min_score': 12
        },
        MedicalSignal.DICOM: {
            'primary_patterns': [r'\bdicom\b', r'\bpydicom\b', r'\.dcm\b'],
            'corroborating': [r'\bradiology\b', r'\bmedical\b', r'\bclinical\b', r'\bct\b', r'\bmri\b'],
            'min_score': 10
        },
        MedicalSignal.NIFTI: {
            'primary_patterns': [r'\bnifti\b', r'\bnii\.gz\b', r'\.nii\b', r'\bnibabel\b'],
            'corroborating': [r'\bmedical\b', r'\bmri\b', r'\bbrain\b', r'\bneuroimaging\b'],
            'min_score': 10
        },
        MedicalSignal.VOLUMETRIC: {
            'primary_patterns': [r'\bvolumetric\b', r'\b3d\s+medical\b', r'\b3d\s+imaging\b'],
            'corroborating': [r'\bnifti\b', r'\bmedical\b', r'\bct\b', r'\bmri\b', r'\bmonai\b'],
            'min_score': 10
        },
        MedicalSignal.SEGMENTATION: {
            'primary_patterns': [r'\bsegmentation\b', r'\bunet\b'],
            'corroborating': [r'\bmedical\b', r'\bdicom\b', r'\bnifti\b', r'\bmonai\b',
                            r'\bradiology\b', r'\bclinical\b'],
            'min_score': 10
        },
        MedicalSignal.MEDICAL_IMAGING: {
            'primary_patterns': [r'\bmedical\s+imaging\b', r'\bradiology\b', r'\bclinical\s+imaging\b'],
            'corroborating': [r'\bdicom\b', r'\bnifti\b', r'\bmonai\b', r'\bct\b', r'\bmri\b'],
            'min_score': 15
        }
    }
    
    # NLP/Foundation model indicators for negative filtering
    NLP_INDICATORS = [
        r'\btransformers\b', r'\btokenizer\b', r'\bllm\b', r'\blanguage\s+model\b',
        r'\bbert\b', r'\bgpt\b', r'\bcausal\s*lm\b', r'\bseq2seq\b', r'\bhuggingface\b',
        r'\bnlp\b', r'\btext\s+generation\b', r'\bsentence\b', r'\bembedding\b'
    ]
    
    # Domain-specific detection patterns with weighted scoring
    DOMAIN_PATTERNS = {
        RepositoryType.NLP: {
            'strong_keywords': ['transformer', 'bert', 'gpt', 'llm', 'tokenizer', 'nlp'],
            'frameworks': ['transformers', 'huggingface'],
            'files': ['tokenizer', 'embedding', 'attention', 'language_model'],
            'weight_multiplier': 1.5,
            'requires_ml_framework': True,  # Must have ML framework
            'min_score_threshold': 10.0
        },
        RepositoryType.FOUNDATION_MODELS: {
            'strong_keywords': ['foundation', 'pretrained', 'large-scale', 'transformer', 'bert', 'gpt', 'llama', 'clip'],
            'frameworks': ['transformers', 'huggingface'],
            'files': ['pretrain', 'foundation', 'large_model'],
            'weight_multiplier': 1.3,
            'requires_ml_framework': True,
            'min_score_threshold': 12.0
        },
        RepositoryType.MULTIMODAL_AI: {
            'strong_keywords': ['multimodal', 'vision-language', 'clip', 'cross-modal', 'image-text'],
            'files': ['multimodal', 'vision_language', 'cross_modal'],
            'weight_multiplier': 1.4,
            'requires_ml_framework': True,
            'min_score_threshold': 10.0
        },
        RepositoryType.COMPUTER_VISION: {
            'strong_keywords': ['vision', 'cnn', 'resnet', 'vit', 'yolo', 'detection'],
            'frameworks': ['opencv', 'torchvision', 'timm'],
            'files': ['vision', 'cnn', 'detection', 'segmentation'],
            'weight_multiplier': 1.0,
            'requires_ml_framework': True,  # Must have CV framework
            'min_score_threshold': 10.0
        },
        RepositoryType.OBJECT_DETECTION: {
            'strong_keywords': ['detection', 'yolo', 'rcnn', 'faster-rcnn', 'ssd', 'retinanet', 'bbox', 'bounding'],
            'files': ['detect', 'detection', 'yolo', 'rcnn', 'bbox'],
            'weight_multiplier': 1.3,
            'requires_ml_framework': True,
            'min_score_threshold': 12.0
        },
        RepositoryType.SEGMENTATION: {
            'strong_keywords': ['segment', 'segmentation', 'unet', 'mask', 'semantic', 'instance'],
            'files': ['segment', 'segmentation', 'unet', 'mask'],
            'weight_multiplier': 1.0,
            'requires_ml_framework': True,
            'min_score_threshold': 10.0
        },
        RepositoryType.MEDICAL_IMAGING: {
            'strong_keywords': ['dicom', 'monai', 'nifti', 'radiology', 'ct scan', 'mri scan', 'medical imaging', 'healthcare', 'clinical'],
            'frameworks': ['monai', 'simpleitk', 'nibabel', 'pydicom'],
            'files': ['dicom', 'nifti', 'medical', 'clinical', 'radiology'],
            'extensions': ['.dcm', '.nii', '.nii.gz'],
            'weight_multiplier': 2.0,  # Requires strong evidence
            'min_score_threshold': 15.0  # High threshold to prevent false positives
        },
        RepositoryType.REINFORCEMENT_LEARNING: {
            'strong_keywords': ['reinforcement', 'q-learning', 'dqn', 'ppo', 'sac', 'a3c', 'ddpg', 'td3'],
            'frameworks': ['gym', 'stable_baselines', 'stable-baselines3', 'ray', 'rllib'],
            'files': ['environment', 'replay_buffer', 'agent_train', 'rl_train'],
            'weight_multiplier': 1.5,
            'requires_rl_context': True,  # Special RL validation
            'min_score_threshold': 15.0  # High threshold - RL is often misclassified
        },
        RepositoryType.ROBOTICS: {
            'strong_keywords': ['robot', 'robotics', 'ros', 'manipulation', 'navigation', 'control'],
            'files': ['robot', 'manipulation', 'navigation', 'control'],
            'weight_multiplier': 1.3
        },
        RepositoryType.DATA_SCIENCE: {
            'strong_keywords': ['pandas', 'numpy', 'analysis', 'visualization', 'jupyter', 'notebook'],
            'files': ['analysis', 'visualization', 'eda', 'exploratory'],
            'weight_multiplier': 0.8
        }
    }
    
    def __init__(self):
        """Initialize the repository analyzer."""
        pass
    
    def analyze(self, tree: RepositoryTree) -> RepositoryIntelligence:
        """
        Analyze repository tree structure and generate intelligence.
        
        Args:
            tree: RepositoryTree object from GitHub tree service
            
        Returns:
            RepositoryIntelligence with complete analysis
        """
        # Extract file paths for analysis
        file_paths = [node.path.lower() for node in tree.files]
        file_names = [node.name.lower() for node in tree.files]
        
        # Detect frameworks
        frameworks = self._detect_frameworks(file_paths, file_names)
        
        # Detect workflow components
        workflow_components = self._detect_workflow_components(file_paths, file_names)
        
        # Detect medical signals
        medical_signals = self._detect_medical_signals(file_paths, file_names)
        
        # Detect repository types with weighted scoring
        repository_types = self._detect_repository_types_weighted(
            frameworks, workflow_components, medical_signals, file_paths, file_names
        )
        
        # Extract key files
        key_files = self._extract_key_files(tree.files)
        
        # Calculate statistics
        stats = self._calculate_statistics(tree.files)
        
        # Generate summary
        summary = self._generate_summary(
            repository_types, frameworks, workflow_components, medical_signals
        )
        
        return RepositoryIntelligence(
            owner=tree.owner,
            repo=tree.repo,
            repository_types=repository_types,
            workflow_components=workflow_components,
            frameworks=frameworks,
            medical_signals=medical_signals,
            key_files=key_files,
            total_python_files=stats['python_files'],
            total_notebook_files=stats['notebook_files'],
            total_config_files=stats['config_files'],
            has_requirements=stats['has_requirements'],
            has_dockerfile=stats['has_dockerfile'],
            has_readme=stats['has_readme'],
            summary=summary
        )
    
    def _detect_frameworks(
        self, file_paths: List[str], file_names: List[str]
    ) -> List[FrameworkDetection]:
        """Detect AI/ML frameworks used in the repository."""
        detections = []
        
        for framework, patterns in self.FRAMEWORK_PATTERNS.items():
            evidence = []
            score = 0
            
            # Check file names
            for pattern in patterns.get('files', []):
                matches = [p for p in file_paths if pattern in p]
                if matches:
                    evidence.extend(matches[:3])  # Limit evidence
                    score += len(matches)
            
            # Check file extensions
            for ext in patterns.get('extensions', []):
                matches = [p for p in file_paths if p.endswith(ext)]
                if matches:
                    evidence.extend(matches[:2])
                    score += len(matches) * 2
            
            # Check keywords in paths
            for keyword in patterns.get('keywords', []):
                matches = [p for p in file_paths if keyword in p]
                if matches:
                    evidence.extend(matches[:2])
                    score += len(matches)
            
            # Determine confidence
            if score > 0:
                if score >= 10:
                    confidence = DetectionConfidence.HIGH
                elif score >= 5:
                    confidence = DetectionConfidence.MEDIUM
                else:
                    confidence = DetectionConfidence.LOW
                
                detections.append(FrameworkDetection(
                    framework=framework,
                    confidence=confidence,
                    evidence=list(set(evidence[:5]))  # Unique, limited evidence
                ))
        
        return sorted(detections, key=lambda x: (x.confidence.value, len(x.evidence)), reverse=True)
    
    def _detect_workflow_components(
        self, file_paths: List[str], file_names: List[str]
    ) -> List[WorkflowDetection]:
        """Detect workflow components in the repository."""
        detections = []
        
        for component, patterns in self.WORKFLOW_PATTERNS.items():
            evidence = []
            score = 0
            
            # Check file names
            for pattern in patterns.get('files', []):
                matches = [p for p in file_paths if pattern in p]
                if matches:
                    evidence.extend(matches[:3])
                    score += len(matches)
            
            # Check keywords
            for keyword in patterns.get('keywords', []):
                matches = [p for p in file_paths if keyword in p]
                if matches:
                    evidence.extend(matches[:2])
                    score += len(matches) * 0.5
            
            # Determine confidence
            if score > 0:
                if score >= 5:
                    confidence = DetectionConfidence.HIGH
                elif score >= 2:
                    confidence = DetectionConfidence.MEDIUM
                else:
                    confidence = DetectionConfidence.LOW
                
                detections.append(WorkflowDetection(
                    component=component,
                    confidence=confidence,
                    evidence=list(set(evidence[:5]))
                ))
        
        return sorted(detections, key=lambda x: (x.confidence.value, len(x.evidence)), reverse=True)
    
    def _detect_medical_signals(
        self, file_paths: List[str], file_names: List[str]
    ) -> List[MedicalSignalDetection]:
        """
        Detect medical AI signals with strict contextual validation.
        Uses weighted scoring and requires corroborating evidence.
        """
        # Combine all text for analysis
        all_text = ' '.join(file_paths).lower()
        
        # Calculate NLP score for negative filtering
        nlp_score = self._calculate_nlp_score(all_text)
        
        # Calculate overall medical evidence score
        medical_score = self._calculate_medical_evidence_score(all_text)
        
        # Apply negative filtering: suppress medical signals if strong NLP presence
        if nlp_score > medical_score * 2:
            # Strong NLP/Foundation model repository - suppress medical signals
            return []
        
        # Minimum threshold check
        if medical_score < 15:
            # Insufficient medical evidence
            return []
        
        # Detect specific medical signals with corroborating evidence
        detections = []
        
        for signal, requirements in self.MEDICAL_SIGNAL_REQUIREMENTS.items():
            result = self._detect_specific_medical_signal(
                signal, requirements, all_text, file_paths
            )
            if result:
                detections.append(result)
        
        return sorted(detections, key=lambda x: (x.confidence.value, len(x.evidence)), reverse=True)
    
    def _calculate_nlp_score(self, text: str) -> float:
        """Calculate NLP/Foundation model score for negative filtering."""
        score = 0.0
        for pattern in self.NLP_INDICATORS:
            matches = re.findall(pattern, text, re.IGNORECASE)
            score += len(matches) * 5.0
        return score
    
    def _calculate_medical_evidence_score(self, text: str) -> float:
        """Calculate weighted medical evidence score."""
        total_score = 0.0
        
        for level, config in self.MEDICAL_EVIDENCE_WEIGHTS.items():
            for pattern in config['keywords']:
                matches = re.findall(pattern, text, re.IGNORECASE)
                total_score += len(matches) * config['weight']
        
        return total_score
    
    def _detect_specific_medical_signal(
        self,
        signal: MedicalSignal,
        requirements: Dict,
        all_text: str,
        file_paths: List[str]
    ) -> Optional[MedicalSignalDetection]:
        """
        Detect a specific medical signal with corroborating evidence requirement.
        Returns None if requirements not met.
        """
        evidence = []
        score = 0.0
        explanation_parts = []
        
        # Check primary patterns (required)
        primary_matches = []
        for pattern in requirements['primary_patterns']:
            matches = re.findall(pattern, all_text, re.IGNORECASE)
            if matches:
                primary_matches.extend(matches)
                score += len(matches) * 10.0
                explanation_parts.append(f"Found primary pattern '{pattern}' ({len(matches)}x)")
        
        # Must have at least one primary match
        if not primary_matches:
            return None
        
        # Check corroborating evidence
        corroborating_matches = []
        for pattern in requirements['corroborating']:
            matches = re.findall(pattern, all_text, re.IGNORECASE)
            if matches:
                corroborating_matches.extend(matches)
                score += len(matches) * 5.0
                explanation_parts.append(f"Corroborating: '{pattern}' ({len(matches)}x)")
        
        # Require corroborating evidence for most signals
        if signal not in [MedicalSignal.DICOM, MedicalSignal.NIFTI]:
            if not corroborating_matches:
                return None
        
        # Check minimum score threshold
        if score < requirements['min_score']:
            return None
        
        # Collect evidence from actual file paths (limit to avoid clutter)
        for path in file_paths[:100]:  # Check first 100 files
            path_lower = path.lower()
            for pattern in requirements['primary_patterns'] + requirements['corroborating']:
                if re.search(pattern, path_lower):
                    evidence.append(path)
                    if len(evidence) >= 5:
                        break
            if len(evidence) >= 5:
                break
        
        # Determine confidence based on score
        if score >= 30:
            confidence = DetectionConfidence.HIGH
        elif score >= 15:
            confidence = DetectionConfidence.MEDIUM
        else:
            confidence = DetectionConfidence.LOW
        
        # Build explanation
        explanation = f"Score: {score:.1f}; " + "; ".join(explanation_parts[:3])
        
        return MedicalSignalDetection(
            signal=signal,
            confidence=confidence,
            evidence=list(set(evidence[:5])),
            explanation=explanation
        )
    
    def _is_weak_evidence(self, path: str) -> bool:
        """Check if a file path represents weak evidence (docs, assets, etc.)."""
        path_lower = path.lower()
        for pattern in self.WEAK_EVIDENCE_PATTERNS:
            if re.search(pattern, path_lower):
                return True
        return False
    
    def _is_strong_evidence(self, path: str) -> bool:
        """Check if a file path represents strong evidence (code, config, etc.)."""
        path_lower = path.lower()
        for pattern in self.STRONG_EVIDENCE_PATTERNS:
            if re.search(pattern, path_lower):
                return True
        return False
    
    def _filter_weak_evidence(self, paths: List[str]) -> List[str]:
        """Filter out weak evidence paths, prioritize strong evidence."""
        strong_paths = [p for p in paths if self._is_strong_evidence(p)]
        if strong_paths:
            return strong_paths
        # If no strong evidence, filter out weak evidence
        return [p for p in paths if not self._is_weak_evidence(p)]
    
    def _has_ml_framework(self, frameworks: List[FrameworkDetection]) -> bool:
        """Check if repository has any ML framework."""
        ml_frameworks = [
            Framework.PYTORCH, Framework.TENSORFLOW, Framework.KERAS,
            Framework.SCIKIT_LEARN, Framework.OPENCV
        ]
        return any(f.framework in ml_frameworks for f in frameworks)
    
    def _has_cv_framework(self, frameworks: List[FrameworkDetection]) -> bool:
        """Check if repository has computer vision framework."""
        cv_frameworks = [Framework.OPENCV, Framework.PYTORCH, Framework.TENSORFLOW]
        return any(f.framework in cv_frameworks for f in frameworks)
    
    def _has_nlp_framework(self, frameworks: List[FrameworkDetection], file_paths: List[str]) -> bool:
        """Check if repository has NLP framework or strong NLP indicators."""
        # Check for transformers/huggingface in paths
        nlp_indicators = ['transformers', 'huggingface', 'tokenizer', 'bert', 'gpt']
        return any(indicator in ' '.join(file_paths) for indicator in nlp_indicators)
    
    def _validate_rl_context(self, file_paths: List[str], frameworks: List[FrameworkDetection]) -> bool:
        """Validate reinforcement learning context with strict requirements."""
        all_text = ' '.join(file_paths).lower()
        matches = 0
        
        # Check for RL frameworks
        rl_framework_names = self.RL_CONTEXT_REQUIREMENTS['frameworks']
        has_rl_framework = any(
            fw_name in all_text for fw_name in rl_framework_names
        )
        if has_rl_framework:
            matches += 2
        
        # Check for strong RL keywords
        for pattern in self.RL_CONTEXT_REQUIREMENTS['strong_keywords']:
            if re.search(pattern, all_text, re.IGNORECASE):
                matches += 1
        
        # Check for RL-specific files
        for file_pattern in self.RL_CONTEXT_REQUIREMENTS['files']:
            if any(file_pattern in path for path in file_paths):
                matches += 1
        
        # Require minimum matches
        return matches >= self.RL_CONTEXT_REQUIREMENTS['min_matches']
    
    def _detect_repository_types_weighted(
        self,
        frameworks: List[FrameworkDetection],
        workflow_components: List[WorkflowDetection],
        medical_signals: List[MedicalSignalDetection],
        file_paths: List[str],
        file_names: List[str]
    ) -> List[RepositoryTypeDetection]:
        """
        Detect repository types using weighted multi-domain scoring.
        Prevents aggressive medical imaging classification.
        Implements strict validation for AI categories.
        """
        # Filter file paths to remove weak evidence
        filtered_paths = self._filter_weak_evidence(file_paths)
        
        # Check if repository has ML frameworks
        has_ml_framework = self._has_ml_framework(frameworks)
        has_cv_framework = self._has_cv_framework(frameworks)
        has_nlp_framework = self._has_nlp_framework(frameworks, filtered_paths)
        
        domain_scores = {}
        domain_evidence = {}
        domain_explanations = {}
        
        # Score each domain
        for domain, patterns in self.DOMAIN_PATTERNS.items():
            score = 0.0
            evidence = []
            explanation_parts = []
            
            # Apply domain-level validation BEFORE scoring
            requires_ml = patterns.get('requires_ml_framework', False)
            requires_rl_context = patterns.get('requires_rl_context', False)
            
            # Skip AI domains if no ML framework detected
            if requires_ml and not has_ml_framework:
                continue
            
            # Special validation for specific domains
            if domain == RepositoryType.NLP and not has_nlp_framework:
                continue
            
            if domain == RepositoryType.COMPUTER_VISION and not has_cv_framework:
                continue
            
            if domain == RepositoryType.REINFORCEMENT_LEARNING:
                if not self._validate_rl_context(filtered_paths, frameworks):
                    continue
            
            # Strong keywords (high weight) - only from filtered paths
            for keyword in patterns.get('strong_keywords', []):
                matches = [p for p in filtered_paths if keyword in p]
                if matches:
                    weight = 5.0 * patterns.get('weight_multiplier', 1.0)
                    score += len(matches) * weight
                    evidence.extend(matches[:2])
                    explanation_parts.append(f"Found '{keyword}' keyword ({len(matches)} occurrences)")
            
            # Framework detection (HIGHEST WEIGHT - actual imports/dependencies)
            framework_names = patterns.get('frameworks', [])
            for fw in frameworks:
                if fw.framework.value in framework_names:
                    weight = 15.0 * patterns.get('weight_multiplier', 1.0)  # Increased from 10.0
                    if fw.confidence == DetectionConfidence.HIGH:
                        score += weight
                    elif fw.confidence == DetectionConfidence.MEDIUM:
                        score += weight * 0.7  # Increased from 0.6
                    else:
                        score += weight * 0.4  # Increased from 0.3
                    evidence.append(f"{fw.framework.value} framework")
                    explanation_parts.append(f"Uses {fw.framework.value} framework ({fw.confidence.value} confidence)")
            
            # File patterns - only from filtered paths
            for file_pattern in patterns.get('files', []):
                matches = [p for p in filtered_paths if file_pattern in p]
                if matches:
                    # Higher weight for strong evidence files
                    strong_matches = [p for p in matches if self._is_strong_evidence(p)]
                    if strong_matches:
                        weight = 4.0 * patterns.get('weight_multiplier', 1.0)  # Increased from 2.0
                        score += len(strong_matches) * weight
                        evidence.extend(strong_matches[:2])
                    else:
                        weight = 2.0 * patterns.get('weight_multiplier', 1.0)
                        score += len(matches) * weight
                        evidence.extend(matches[:2])
            
            # Extension patterns (HIGH WEIGHT - actual model/data files)
            for ext in patterns.get('extensions', []):
                matches = [p for p in filtered_paths if p.endswith(ext)]
                if matches:
                    weight = 12.0 * patterns.get('weight_multiplier', 1.0)  # Increased from 8.0
                    score += len(matches) * weight
                    evidence.extend(matches[:2])
                    explanation_parts.append(f"Contains {ext} files ({len(matches)} files)")
            
            # Apply minimum threshold for medical imaging
            min_threshold = patterns.get('min_score_threshold', 0.0)
            if score < min_threshold:
                continue
            
            if score > 0:
                domain_scores[domain] = score
                domain_evidence[domain] = list(set(evidence[:5]))
                domain_explanations[domain] = "; ".join(explanation_parts[:3]) if explanation_parts else "Pattern matching"
        
        # Special handling for medical imaging - require strong evidence
        if RepositoryType.MEDICAL_IMAGING in domain_scores:
            medical_frameworks = [f for f in frameworks if f.framework in [
                Framework.MONAI, Framework.SIMPLEITK, Framework.NIBABEL
            ]]
            has_dicom = any('.dcm' in p or 'dicom' in p for p in file_paths)
            has_nifti = any('.nii' in p or 'nifti' in p for p in file_paths)
            has_medical_keywords = any(
                kw in ' '.join(file_paths) 
                for kw in ['radiology', 'clinical', 'patient', 'diagnosis', 'medical imaging']
            )
            
            # Require at least one strong medical indicator
            if not (medical_frameworks or has_dicom or has_nifti or has_medical_keywords):
                # Downgrade to segmentation or computer vision instead
                del domain_scores[RepositoryType.MEDICAL_IMAGING]
                del domain_evidence[RepositoryType.MEDICAL_IMAGING]
                del domain_explanations[RepositoryType.MEDICAL_IMAGING]
        
        # Convert scores to detections
        detections = []
        for domain, score in sorted(domain_scores.items(), key=lambda x: x[1], reverse=True):
            # Calibrate confidence based on score
            if score >= 30.0:
                confidence = DetectionConfidence.HIGH
            elif score >= 15.0:
                confidence = DetectionConfidence.MEDIUM
            else:
                confidence = DetectionConfidence.LOW
            
            detections.append(RepositoryTypeDetection(
                type=domain,
                confidence=confidence,
                evidence=domain_evidence[domain],
                score=score,
                explanation=domain_explanations[domain]
            ))
        
        # Add legacy machine learning detection if ML frameworks present
        ml_frameworks = [f for f in frameworks if f.framework in [
            Framework.PYTORCH, Framework.TENSORFLOW, Framework.KERAS, Framework.SCIKIT_LEARN
        ]]
        if ml_frameworks and RepositoryType.MACHINE_LEARNING not in domain_scores:
            detections.append(RepositoryTypeDetection(
                type=RepositoryType.MACHINE_LEARNING,
                confidence=DetectionConfidence.MEDIUM,
                evidence=[f.framework.value for f in ml_frameworks],
                score=10.0,
                explanation=f"Uses ML frameworks: {', '.join([f.framework.value for f in ml_frameworks])}"
            ))
        
        # Fallback to general if no specific domain detected
        if not detections:
            detections.append(RepositoryTypeDetection(
                type=RepositoryType.GENERAL,
                confidence=DetectionConfidence.HIGH,
                evidence=["No specific domain patterns detected"],
                score=1.0,
                explanation="General purpose repository without specific AI/ML domain indicators"
            ))
        
        return detections[:5]  # Return top 5 classifications
    
    def _extract_key_files(self, files: List[TreeNode]) -> Dict[str, List[str]]:
        """Extract and categorize key files."""
        key_files = {
            'training': [],
            'inference': [],
            'models': [],
            'configs': [],
            'notebooks': [],
            'data': []
        }
        
        for file in files:
            path = file.path.lower()
            name = file.name.lower()
            
            # Training files
            if any(x in name for x in ['train', 'trainer', 'training']):
                key_files['training'].append(file.path)
            
            # Inference files
            if any(x in name for x in ['infer', 'inference', 'predict', 'test']):
                key_files['inference'].append(file.path)
            
            # Model files
            if any(x in name for x in ['model', 'network', 'architecture', 'unet', 'resnet']):
                key_files['models'].append(file.path)
            
            # Config files
            if any(x in name for x in ['config', 'settings', 'params']):
                key_files['configs'].append(file.path)
            
            # Notebooks
            if path.endswith('.ipynb'):
                key_files['notebooks'].append(file.path)
            
            # Data files
            if any(x in path for x in ['data', 'dataset', 'preprocess']):
                key_files['data'].append(file.path)
        
        # Limit to top files
        return {k: v[:10] for k, v in key_files.items() if v}
    
    def _calculate_statistics(self, files: List[TreeNode]) -> Dict:
        """Calculate repository statistics."""
        stats = {
            'python_files': 0,
            'notebook_files': 0,
            'config_files': 0,
            'has_requirements': False,
            'has_dockerfile': False,
            'has_readme': False
        }
        
        for file in files:
            path = file.path.lower()
            name = file.name.lower()
            
            if path.endswith('.py'):
                stats['python_files'] += 1
            
            if path.endswith('.ipynb'):
                stats['notebook_files'] += 1
            
            if any(x in name for x in ['config', 'settings', '.yml', '.yaml', '.json', '.toml']):
                stats['config_files'] += 1
            
            if name == 'requirements.txt':
                stats['has_requirements'] = True
            
            if 'dockerfile' in name:
                stats['has_dockerfile'] = True
            
            if name.startswith('readme'):
                stats['has_readme'] = True
        
        return stats
    
    def _generate_summary(
        self,
        repository_types: List[RepositoryTypeDetection],
        frameworks: List[FrameworkDetection],
        workflow_components: List[WorkflowDetection],
        medical_signals: List[MedicalSignalDetection]
    ) -> str:
        """Generate human-readable summary."""
        parts = []
        
        # Repository type
        if repository_types:
            primary_type = repository_types[0].type.value.replace('_', ' ').title()
            parts.append(f"{primary_type} repository")
        
        # Frameworks
        if frameworks:
            fw_names = [f.framework.value.replace('_', ' ').title() for f in frameworks[:2]]
            parts.append(f"using {' and '.join(fw_names)}")
        
        # Workflow
        if workflow_components:
            wf_names = [w.component.value for w in workflow_components[:2]]
            parts.append(f"with {' and '.join(wf_names)} components")
        
        # Medical signals (only if medical imaging is primary)
        if repository_types and repository_types[0].type == RepositoryType.MEDICAL_IMAGING and medical_signals:
            med_names = [m.signal.value.replace('_', ' ') for m in medical_signals[:2]]
            parts.append(f"focused on {' and '.join(med_names)}")
        
        return ' '.join(parts) if parts else "General repository"


# Singleton instance
_analyzer_instance = None


def get_repository_analyzer() -> RepositoryAnalyzer:
    """Get or create singleton RepositoryAnalyzer instance."""
    global _analyzer_instance
    if _analyzer_instance is None:
        _analyzer_instance = RepositoryAnalyzer()
    return _analyzer_instance

# Made with Bob
