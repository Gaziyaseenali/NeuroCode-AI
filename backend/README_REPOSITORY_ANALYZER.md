# Repository Structure Analyzer

Lightweight repository structure analyzer service for NeuroCode AI using FastAPI architecture.

## Overview

The Repository Analyzer is a rule-based intelligence system that analyzes GitHub repository structures to detect:

- **Repository types**: Machine learning, medical imaging, segmentation, research, inference
- **Workflow components**: Preprocessing, training, inference, evaluation, deployment
- **AI/ML frameworks**: PyTorch, TensorFlow, MONAI, SimpleITK, nibabel, Keras, scikit-learn, OpenCV
- **Medical AI signals**: Segmentation, MRI, CT, DICOM, volumetric processing, NIfTI

## Key Features

✅ **Lightweight Rule-Based Analysis**

- No embeddings or vector databases
- Fast analysis using file paths and names only
- No file content reading required

✅ **Low RAM Usage**

- Optimized for hackathon MVP simplicity
- Minimal memory footprint
- Efficient pattern matching

✅ **Explainable Intelligence**

- Evidence provided for all detections
- Confidence levels (high, medium, low)
- Human-readable summaries

✅ **Modular Architecture**

- Separate models, services, and routes
- Easy to extend with new patterns
- Reusable components

## Architecture

```
backend/
├── app/
│   ├── models/
│   │   └── analyzer.py          # Pydantic models for analysis output
│   ├── services/
│   │   └── repository_analyzer.py  # Core analysis logic
│   └── api/
│       └── routes/
│           └── github.py         # FastAPI endpoints
├── tests/
│   └── test_repository_analyzer.py  # Unit tests
└── examples/
    └── analyze_repository.py    # Example usage script
```

## Models

### RepositoryIntelligence

Main output model containing complete analysis:

```python
{
    "owner": "Project-MONAI",
    "repo": "MONAI",
    "repository_types": [
        {
            "type": "medical_imaging",
            "confidence": "high",
            "evidence": ["MONAI framework", "medical imaging files"]
        }
    ],
    "frameworks": [
        {
            "framework": "pytorch",
            "confidence": "high",
            "evidence": ["torch imports", "model.py"]
        }
    ],
    "workflow_components": [
        {
            "component": "training",
            "confidence": "high",
            "evidence": ["train.py", "trainer.py"]
        }
    ],
    "medical_signals": [
        {
            "signal": "segmentation",
            "confidence": "high",
            "evidence": ["segmentation in filenames"]
        }
    ],
    "key_files": {
        "training": ["train.py"],
        "models": ["unet.py"]
    },
    "total_python_files": 150,
    "total_notebook_files": 10,
    "has_requirements": true,
    "summary": "Medical imaging repository using PyTorch and MONAI"
}
```

### Detection Types

**Repository Types:**

- `machine_learning`: General ML projects
- `medical_imaging`: Medical imaging projects
- `segmentation`: Image/medical segmentation
- `research`: Research projects with notebooks/papers
- `inference`: Deployment-focused projects
- `general`: Default fallback

**Workflow Components:**

- `preprocessing`: Data preparation and augmentation
- `training`: Model training
- `inference`: Prediction and testing
- `evaluation`: Metrics and validation
- `deployment`: API, Docker, serving

**Frameworks:**

- `pytorch`, `tensorflow`, `keras`
- `monai` (medical imaging)
- `simpleitk`, `nibabel` (medical data)
- `scikit_learn`, `opencv`

**Medical Signals:**

- `segmentation`: Segmentation tasks
- `mri`, `ct`: Imaging modalities
- `dicom`: DICOM format
- `nifti`: NIfTI format
- `volumetric`: 3D processing
- `medical_imaging`: General medical imaging

## API Endpoints

### POST /api/analyze-repository

Analyze repository structure from GitHub URL.

**Request:**

```json
{
  "url": "https://github.com/Project-MONAI/MONAI",
  "branch": "main" // optional
}
```

**Response:** `RepositoryIntelligence` object

**Example:**

```bash
curl -X POST "http://localhost:8000/api/analyze-repository" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://github.com/Project-MONAI/MONAI"}'
```

### GET /api/analyze-repository/{owner}/{repo}

Analyze repository by owner and repo name.

**Parameters:**

- `owner`: Repository owner (path parameter)
- `repo`: Repository name (path parameter)
- `branch`: Branch name (query parameter, optional)

**Example:**

```bash
curl "http://localhost:8000/api/analyze-repository/Project-MONAI/MONAI?branch=main"
```

## Detection Logic

### Framework Detection

Detects frameworks based on:

- File names containing framework keywords
- File extensions (`.pth`, `.pb`, `.h5`, `.nii`)
- Import patterns in file paths
- Framework-specific keywords

**Scoring:**

- High confidence: 10+ matches
- Medium confidence: 5-9 matches
- Low confidence: 1-4 matches

### Workflow Component Detection

Detects components based on:

- File names (train.py, infer.py, preprocess.py)
- Directory names (data/, models/, deployment/)
- Keywords in paths

### Medical Signal Detection

Detects medical AI patterns:

- Medical framework usage (MONAI, SimpleITK)
- Medical file formats (.nii, .dcm)
- Medical keywords (mri, ct, dicom, segmentation)
- Anatomical terms in paths

### Repository Type Classification

Combines all detections to classify:

- Medical imaging: Medical frameworks + signals
- Segmentation: Segmentation files + UNet patterns
- Research: Notebooks + papers
- Inference: Inference files without training
- Machine learning: ML frameworks present

## Usage Examples

### Python Script

```python
from app.utils.github_parser import parse_github_url
from app.services.github_tree_service import get_github_tree_service
from app.services.repository_analyzer import get_repository_analyzer

# Parse URL
owner, repo = parse_github_url("https://github.com/Project-MONAI/MONAI")

# Fetch tree
tree_service = get_github_tree_service()
tree = tree_service.fetch_repository_tree(owner, repo)

# Analyze
analyzer = get_repository_analyzer()
intelligence = analyzer.analyze(tree)

# Print results
print(f"Summary: {intelligence.summary}")
print(f"Repository types: {[rt.type for rt in intelligence.repository_types]}")
print(f"Frameworks: {[f.framework for f in intelligence.frameworks]}")
```

### Command Line

```bash
# Run example script
cd backend
python examples/analyze_repository.py https://github.com/Project-MONAI/MONAI

# Or with branch
python examples/analyze_repository.py https://github.com/pytorch/pytorch main
```

### FastAPI Interactive Docs

1. Start the server:

```bash
cd backend
uvicorn app.main:app --reload
```

2. Open browser: http://localhost:8000/docs

3. Try the `/api/analyze-repository` endpoint

## Testing

Run tests:

```bash
cd backend
pytest tests/test_repository_analyzer.py -v
```

Test coverage includes:

- Framework detection
- Workflow component detection
- Medical signal detection
- Repository type classification
- Key file extraction
- Statistics calculation
- Summary generation
- Confidence levels
- Evidence collection
- Edge cases (empty repos, inference-only, research)

## Configuration

No configuration required! The analyzer uses predefined patterns.

To extend patterns, edit `backend/app/services/repository_analyzer.py`:

```python
# Add new framework
FRAMEWORK_PATTERNS = {
    Framework.YOUR_FRAMEWORK: {
        'files': ['your_framework'],
        'imports': ['your_framework'],
        'extensions': ['.ext'],
        'keywords': ['keyword']
    }
}
```

## Performance

- **Analysis time**: < 1 second for most repositories
- **Memory usage**: < 50 MB
- **API rate limits**:
  - Without token: 60 requests/hour
  - With token: 5000 requests/hour

## Limitations

1. **File path analysis only**: Does not read file contents
2. **Rule-based**: May miss custom patterns
3. **English-centric**: Best for English file names
4. **GitHub API dependent**: Requires GitHub API access

## Future Enhancements

Potential improvements (not in current MVP):

- [ ] Custom pattern configuration via API
- [ ] Multi-language support
- [ ] File content analysis (optional)
- [ ] ML-based classification (optional)
- [ ] Caching for repeated analyses
- [ ] Batch analysis endpoint

## Troubleshooting

**Issue**: No frameworks detected

- **Solution**: Check if file names contain framework keywords

**Issue**: Low confidence detections

- **Solution**: Repository may have non-standard structure

**Issue**: Rate limit errors

- **Solution**: Set `GITHUB_TOKEN` environment variable

**Issue**: Empty analysis results

- **Solution**: Repository may be empty or heavily filtered

## Contributing

To add new detection patterns:

1. Update models in `app/models/analyzer.py`
2. Add patterns to `app/services/repository_analyzer.py`
3. Add tests to `tests/test_repository_analyzer.py`
4. Update documentation

## License

Part of NeuroCode AI project.

---

**Made with Bob** 🤖
