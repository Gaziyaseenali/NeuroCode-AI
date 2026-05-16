// API Response Types
export interface HealthCheckResponse {
  status: string;
  message: string;
  timestamp: string;
}

export interface ApiError {
  message: string;
  status?: number;
}

export interface BackendStatus {
  isHealthy: boolean;
  rootEndpoint: boolean;
  docsEndpoint: boolean;
  healthEndpoint: boolean;
  error?: string;
}

// Repository Intelligence Types
export type LoadingState = 'idle' | 'loading' | 'success' | 'error';
export type ProcessingStage =
  | 'parsing'
  | 'fetching_metadata'
  | 'analyzing_structure'
  | 'detecting_frameworks'
  | 'generating_intelligence'
  | 'complete';

export interface RepositoryMetadataCard {
  name: string;
  owner: string;
  description?: string;
  stars: number;
  forks: number;
  language?: string;
  topics: string[];
  avatar_url?: string;
  html_url: string;
  updated_at: string;
}

export interface FrameworkVisualization {
  name: string;
  confidence: string;
  category: string;
  icon?: string;
  color?: string;
  evidence_count: number;
}

export interface WorkflowNode {
  id: string;
  label: string;
  type: string;
  confidence: string;
  files: string[];
  has_implementation: boolean;
}

export interface MedicalAISignalCard {
  signal_type: string;
  confidence: string;
  description: string;
  evidence: string[];
  icon?: string;
}

export interface ImportantFileHighlight {
  path: string;
  name: string;
  importance: string;
  category: string;
  description: string;
  size?: number;
}

export interface ProcessingProgress {
  stage: ProcessingStage;
  progress: number;
  message: string;
  estimated_time_remaining?: number;
}

export interface ReasoningStep {
  category: string;
  title: string;
  explanation: string;
  evidence: string[];
  confidence_impact: string;
}

export interface AIReasoning {
  classification_reasoning: ReasoningStep[];
  framework_reasoning: ReasoningStep[];
  workflow_reasoning: ReasoningStep[];
  medical_reasoning: ReasoningStep[];
  summary: string;
}

export interface MaturityBadge {
  level: string;
  score: number;
  label: string;
  color: string;
  description: string;
}

export interface MaturityIndicator {
  name: string;
  status: string;
  impact: string;
  description: string;
}

export interface ArchitectureInsight {
  insight_type: string;
  title: string;
  description: string;
  evidence: string[];
  significance: string;
  icon?: string;
}

export interface ExecutiveSummary {
  headline: string;
  overview: string;
  key_highlights: string[];
  technical_profile: string;
  use_cases: string[];
  target_audience: string;
}

export interface RepositoryIntelligence {
  loading_state: LoadingState;
  processing_progress?: ProcessingProgress;
  owner: string;
  repo: string;
  branch: string;
  metadata_card?: RepositoryMetadataCard;
  frameworks: FrameworkVisualization[];
  workflow_nodes: WorkflowNode[];
  medical_signals: MedicalAISignalCard[];
  important_files: ImportantFileHighlight[];
  classification: Record<string, any>;
  statistics: Record<string, any>;
  ai_reasoning?: AIReasoning;
  maturity_badge?: MaturityBadge;
  maturity_indicators: MaturityIndicator[];
  architecture_insights: ArchitectureInsight[];
  executive_summary?: ExecutiveSummary;
  llm_summary?: string;
  analyzed_at: string;
  processing_time_ms?: number;
}

export interface ErrorDetail {
  error_type: string;
  message: string;
  stage?: ProcessingStage;
  retry_possible: boolean;
  suggestions: string[];
}

export interface RepositoryAnalysisError {
  loading_state: LoadingState;
  error: ErrorDetail;
  timestamp: string;
}

export interface AnalyzeRepositoryRequest {
  url: string;
  branch?: string;
  include_filtered?: boolean;
  max_depth?: number;
}

// Made with Bob
