# Repository Intelligence Aggregation Service

## Overview

The **Repository Intelligence Aggregation Service** is a lightweight orchestration layer that combines three existing services to provide unified, comprehensive repository analysis. It generates structured intelligence optimized for LLM consumption without using embeddings, vector databases, or LLM inference.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│         Repository Intelligence Service (Orchestrator)       │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│   Metadata   │   │     Tree     │   │   Analyzer   │
│   Service    │   │   Service    │   │   Service    │
└──────────────┘   └──────────────┘   └──────────────┘
        │                   │                   │
        └───────────────────┴───────────────────┘
                            │
                            ▼
              ┌─────────────────────────┐
              │  Unified Intelligence   │
              │  (Structured Output)    │
              └─────────────────────────┘
```

## Features

### 🎯 Core Capabilities

- **Metadata Aggregation**: Repository stars, forks, language, topics, license
- **Structure Analysis**: File tree, important files, directory organization
- **Type Detection**: ML, medical imaging, segmentation, research, inference
- **Framework Detection**: PyTorch, TensorFlow, MONAI, SimpleITK, etc.
- **Workflow Identification**: Training, inference, preprocessing, evaluation, deployment
- **Medical AI Signals**: MRI, CT, DICOM, segmentation, volumetric processing
- **LLM-Optimized Output**: Structured summaries ready for LLM context

### ⚡ Performance

- **Lightweight**: No embeddings or vector databases
- **Low RAM**: Optimized for hackathon MVP simplicity
- **Fast**: No repository cloning required
- **Scalable**: Singleton pattern with connection pooling

## Installation

Already included in the NeuroCode AI backend. No additional dependencies required.

## Quick Start

### Using the Service Directly

```python
from app.services.intelligence_service import get_intelligence_service

# Get service instance
service = get_intelligence_service()

# Analyze repository
intelligence = service.analyze_repository(
    url="https://github.com/Project-MONAI/MONAI",
    branch=None,  # Use default branch
    include_filtered=False,
    max_depth=None
)

# Access results
print(f"Type: {intelligence.classification.primary_type}")
print(f"Frameworks: {intelligence.technology.primary_frameworks}")
print(f"Medical AI: {intelligence.medical_context.is_medical_ai}")
```

### Using the API Endpoint

#### POST Request

```bash
curl -X POST "http://localhost:8000/api/repository-intelligence" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://github.com/Project-MONAI/MONAI",
    "branch": null,
    "include_filtered": false,
    "max_depth": null
  }'
```

#### GET Request

```bash
curl "http://localhost:8000/api/repository-intelligence/Project-MONAI/MONAI"
```

## Output Structure

### Unified Repository Intelligence

```json
{
  "owner": "Project-MONAI",
  "repo": "MONAI",
  "branch": "main",

  "metadata": {
    "name": "MONAI",
    "stars": 5000,
    "language": "Python",
    "topics": ["medical-imaging", "deep-learning"],
    "license": "Apache-2.0"
  },

  "structure": {
    "total_files": 500,
    "filtered_files": 450,
    "critical_files": [...],
    "high_importance_files": [...]
  },

  "classification": {
    "primary_type": "medical_imaging",
    "secondary_types": ["machine_learning"],
    "confidence": "high"
  },

  "workflow": {
    "has_training": true,
    "has_inference": true,
    "has_preprocessing": true,
    "components": [...]
  },

  "technology": {
    "primary_frameworks": ["pytorch", "monai"],
    "medical_frameworks": ["monai", "simpleitk"]
  },

  "medical_context": {
    "is_medical_ai": true,
    "confidence": "high",
    "modalities": ["MRI", "CT", "DICOM"],
    "tasks": ["segmentation", "volumetric"]
  },

  "statistics": {
    "total_python_files": 150,
    "total_notebook_files": 10,
    "has_requirements": true,
    "has_dockerfile": true
  },

  "llm_context": {
    "repository_overview": "Medical Imaging repository...",
    "technical_summary": "Primary language: Python...",
    "key_capabilities": ["Model training", "Inference"],
    "important_files_summary": "Training: train.py...",
    "suggested_entry_points": ["README.md", "train.py"]
  }
}
```

## API Endpoints

### POST /api/repository-intelligence

Analyze repository using URL.

**Request Body:**

```json
{
  "url": "https://github.com/owner/repo",
  "branch": "main",
  "include_filtered": false,
  "max_depth": null
}
```

**Response:** `UnifiedRepositoryIntelligence` object

### GET /api/repository-intelligence/{owner}/{repo}

Analyze repository using owner and repo name.

**Query Parameters:**

- `branch` (optional): Branch name
- `include_filtered` (optional): Include filtered files
- `max_depth` (optional): Maximum tree depth

**Response:** `UnifiedRepositoryIntelligence` object

## Use Cases

### 1. Repository Understanding

Quickly understand what a repository does, its technology stack, and key files.

```python
intelligence = service.analyze_repository(url="...")
print(intelligence.llm_context.repository_overview)
print(intelligence.llm_context.suggested_entry_points)
```

### 2. Medical AI Detection

Identify medical AI repositories and their characteristics.

```python
if intelligence.medical_context.is_medical_ai:
    print(f"Modalities: {intelligence.medical_context.modalities}")
    print(f"Tasks: {intelligence.medical_context.tasks}")
```

### 3. Technology Stack Analysis

Detect frameworks and tools used in a project.

```python
print(f"Frameworks: {intelligence.technology.primary_frameworks}")
print(f"Language: {intelligence.metadata.primary_language}")
```

### 4. LLM Context Preparation

Generate structured summaries for LLM consumption.

```python
context = intelligence.llm_context
prompt = f"""
Repository: {context.repository_overview}
Technical: {context.technical_summary}
Capabilities: {', '.join(context.key_capabilities)}
Entry Points: {', '.join(context.suggested_entry_points)}
"""
```

### 5. Repository Classification

Categorize repositories by type and purpose.

```python
classification = intelligence.classification
print(f"Type: {classification.primary_type}")
print(f"Confidence: {classification.confidence}")
```

## Testing

### Run Unit Tests

```bash
cd backend
pytest tests/test_intelligence_service.py -v
```

### Run Example Script

```bash
cd backend
python examples/fetch_repository_intelligence.py
```

### Test API Endpoint

```bash
# Start server
cd backend
uvicorn app.main:app --reload

# In another terminal
python test_intelligence_api.py
```

## Configuration

### Environment Variables

Set `GITHUB_TOKEN` for higher rate limits:

```bash
# .env file
GITHUB_TOKEN=your_github_personal_access_token
```

**Rate Limits:**

- Without token: 60 requests/hour
- With token: 5000 requests/hour

## Implementation Details

### Service Components

1. **GitHub Service**: Fetches repository metadata
2. **Tree Service**: Fetches repository file structure
3. **Analyzer Service**: Analyzes structure and detects patterns
4. **Intelligence Service**: Orchestrates all services and aggregates results

### Data Flow

```
URL Input
    ↓
Parse URL (owner, repo)
    ↓
Fetch Metadata (stars, language, topics)
    ↓
Fetch Tree (files, directories, structure)
    ↓
Analyze Structure (types, frameworks, workflows)
    ↓
Aggregate Intelligence (combine all data)
    ↓
Generate LLM Context (optimize for LLM usage)
    ↓
Return Unified Intelligence
```

### Key Design Decisions

1. **No Cloning**: Uses GitHub API to avoid heavy disk/RAM usage
2. **Rule-Based**: Pattern matching instead of ML for explainability
3. **Lightweight**: Minimal dependencies, optimized for speed
4. **Modular**: Each service can be used independently
5. **Singleton**: Connection pooling for better performance
6. **Structured Output**: Pydantic models for type safety

## Error Handling

The service handles various error scenarios:

```python
try:
    intelligence = service.analyze_repository(url="...")
except IntelligenceServiceError as e:
    if "not found" in str(e).lower():
        # Repository not found
    elif "rate limit" in str(e).lower():
        # Rate limit exceeded
    else:
        # Other API errors
```

## Performance Considerations

### Memory Usage

- **Metadata**: ~5-10 KB per repository
- **Tree**: ~50-500 KB depending on repository size
- **Analysis**: ~10-50 KB for detections
- **Total**: ~100-600 KB per repository

### Response Time

- **Small repos** (<100 files): 1-3 seconds
- **Medium repos** (100-1000 files): 3-10 seconds
- **Large repos** (>1000 files): 10-30 seconds

### Optimization Tips

1. Use `max_depth` to limit tree traversal
2. Set `include_filtered=False` to skip unnecessary files
3. Cache results for frequently accessed repositories
4. Use GitHub token for higher rate limits

## Limitations

1. **No File Content Analysis**: Only analyzes file paths and names
2. **Rule-Based Detection**: May miss custom patterns
3. **GitHub API Dependent**: Requires GitHub API access
4. **Rate Limits**: Subject to GitHub API rate limits
5. **Public Repos Only**: Private repos require authentication

## Future Enhancements

Potential improvements (not implemented in MVP):

1. **Caching Layer**: Redis/memory cache for results
2. **Batch Processing**: Analyze multiple repositories
3. **Custom Patterns**: User-defined detection rules
4. **File Content Analysis**: Parse key files for deeper insights
5. **Dependency Analysis**: Parse requirements.txt, package.json
6. **Code Quality Metrics**: Detect code smells, complexity
7. **Commit History**: Analyze development patterns
8. **Contributor Analysis**: Team size, activity patterns

## Examples

### Example 1: Medical Imaging Repository

```python
intelligence = service.analyze_repository(
    url="https://github.com/Project-MONAI/MONAI"
)

# Output:
# Type: medical_imaging
# Frameworks: pytorch, monai
# Medical: True (MRI, CT, DICOM)
# Workflow: training, inference, preprocessing
```

### Example 2: ML Framework

```python
intelligence = service.analyze_repository(
    url="https://github.com/pytorch/pytorch"
)

# Output:
# Type: machine_learning
# Frameworks: pytorch
# Medical: False
# Workflow: training, inference, deployment
```

### Example 3: Research Repository

```python
intelligence = service.analyze_repository(
    url="https://github.com/facebookresearch/detectron2"
)

# Output:
# Type: research, machine_learning
# Frameworks: pytorch
# Medical: False
# Workflow: training, inference, evaluation
```

## Troubleshooting

### Issue: Rate Limit Exceeded

**Solution**: Set `GITHUB_TOKEN` environment variable

### Issue: Repository Not Found

**Solution**: Check URL format and repository accessibility

### Issue: Slow Response

**Solution**: Use `max_depth` parameter to limit tree depth

### Issue: Missing Detections

**Solution**: Check if patterns match your use case, may need custom rules

## Contributing

To add new detection patterns:

1. Update patterns in `app/services/repository_analyzer.py`
2. Add tests in `tests/test_intelligence_service.py`
3. Update documentation

## License

Part of NeuroCode AI project. See main project license.

## Support

For issues or questions:

- Check existing documentation
- Review test cases for examples
- Open an issue in the main repository

---

**Made with Bob** 🤖

Last Updated: 2026-05-15
