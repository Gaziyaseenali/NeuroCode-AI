# GitHub Repository Tree Fetcher Service

A lightweight, efficient service for fetching GitHub repository tree structures using the GitHub REST API without cloning repositories. Optimized for low RAM usage and designed specifically for ML/medical AI project analysis.

## Features

### Core Capabilities
- ✅ **No Repository Cloning** - Uses GitHub REST API exclusively
- ✅ **Recursive Tree Fetching** - Efficiently fetches entire repository structure
- ✅ **Separate Files & Directories** - Organized output with clear categorization
- ✅ **Large Repository Support** - Handles repositories with thousands of files
- ✅ **Low RAM Usage** - Optimized for hackathon MVP and resource constraints

### Intelligent Filtering
Automatically filters out unnecessary files and directories:
- `node_modules`, `.git`, `__pycache__`, `.pytest_cache`
- Virtual environments: `venv`, `env`, `.venv`, `virtualenv`
- Cache folders: `.cache`, `cache`, `tmp`, `temp`
- Build artifacts: `dist`, `build`, `.next`, `.nuxt`
- IDE folders: `.idea`, `.vscode`, `.vs`
- Binary files: `.exe`, `.dll`, `.so`, `.zip`, `.tar`
- Model weights: `.h5`, `.pth`, `.ckpt`, `.pb`, `.onnx`
- Lock files: `package-lock.json`, `yarn.lock`, `poetry.lock`

### ML/Medical AI File Detection
Automatically identifies and categorizes important files:

**Critical Files** (🔴 High Priority):
- Training scripts: `train.py`, `training.py`, `trainer.py`
- Inference scripts: `infer.py`, `inference.py`, `predict.py`
- Model definitions: `model.py`, `models.py`, `network.py`, `architecture.py`
- Entry points: `main.py`, `run.py`, `app.py`

**High Importance** (🟡 Medium Priority):
- Dependencies: `requirements.txt`, `environment.yml`, `conda.yml`
- Documentation: `README.md`, `README.rst`
- Configuration: `config.py`, `config.yaml`, `settings.py`
- Deployment: `Dockerfile`, `docker-compose.yml`
- Setup: `setup.py`, `pyproject.toml`

**Medium Importance** (🟢 Low Priority):
- Jupyter notebooks: `*.ipynb`
- Data processing: `preprocess.py`, `dataset.py`
- Utilities: `utils.py`, `helpers.py`
- Metrics: `metrics.py`, `loss.py`
- Augmentation: `augment.py`, `transforms.py`

**Low Importance** (⚪ Minimal Priority):
- Tests: `test_*.py`, `*_test.py`
- Documentation: `docs/*`
- Examples: `examples/*`, `demo.py`

## Installation

The service is already integrated into the NeuroCode AI backend. No additional installation required.

### Dependencies
```txt
fastapi>=0.136.1
requests>=2.34.2
pydantic>=2.13.4
python-dotenv>=1.2.2
```

## Usage

### 1. FastAPI Endpoints

#### POST `/api/fetch-repo-tree`
Fetch repository tree by providing a GitHub URL.

**Request Body:**
```json
{
  "url": "https://github.com/owner/repo",
  "branch": "main",
  "max_depth": null,
  "include_filtered": false
}
```

**Parameters:**
- `url` (required): GitHub repository URL
- `branch` (optional): Branch name (defaults to repository's default branch)
- `max_depth` (optional): Maximum directory depth to traverse (null = unlimited)
- `include_filtered` (optional): Include filtered files/directories (default: false)

**Example Request:**
```bash
curl -X POST "http://localhost:8000/api/fetch-repo-tree" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://github.com/tensorflow/tensorflow",
    "branch": "master",
    "max_depth": 3,
    "include_filtered": false
  }'
```

#### GET `/api/repo-tree/{owner}/{repo}`
Fetch repository tree directly by owner and repo name.

**Query Parameters:**
- `owner` (required): Repository owner username or organization
- `repo` (required): Repository name
- `branch` (optional): Branch name
- `max_depth` (optional): Maximum depth
- `include_filtered` (optional): Include filtered files

**Example Request:**
```bash
curl "http://localhost:8000/api/repo-tree/tensorflow/tensorflow?branch=master&max_depth=3"
```

### 2. Python Service Usage

```python
from app.services.github_tree_service import get_github_tree_service

# Get service instance
tree_service = get_github_tree_service()

# Fetch repository tree
tree = tree_service.fetch_repository_tree(
    owner="tensorflow",
    repo="tensorflow",
    branch="master",
    max_depth=3,
    include_filtered=False
)

# Access tree data
print(f"Total files: {tree.total_files}")
print(f"Filtered files: {tree.filtered_files}")
print(f"Total directories: {tree.total_directories}")

# Access important files
for file in tree.important_files["critical"]:
    print(f"Critical file: {file.path}")

# Access all files
for file in tree.files:
    print(f"{file.path} - {file.importance.value}")

# Access directories
for directory in tree.directories:
    print(f"Directory: {directory.path}")
```

### 3. Response Structure

```json
{
  "owner": "tensorflow",
  "repo": "tensorflow",
  "branch": "master",
  "total_files": 15420,
  "total_directories": 1250,
  "filtered_files": 8500,
  "filtered_directories": 850,
  "files": [
    {
      "path": "tensorflow/python/training/training.py",
      "name": "training.py",
      "type": "file",
      "size": 45230,
      "sha": "abc123def456",
      "url": "https://api.github.com/repos/tensorflow/tensorflow/contents/...",
      "importance": "critical"
    }
  ],
  "directories": [
    {
      "path": "tensorflow/python",
      "name": "python",
      "type": "directory",
      "sha": "def456ghi789",
      "url": "https://api.github.com/repos/tensorflow/tensorflow/contents/...",
      "importance": "none"
    }
  ],
  "important_files": {
    "critical": [
      {
        "path": "train.py",
        "name": "train.py",
        "type": "file",
        "size": 15420,
        "importance": "critical"
      }
    ],
    "high": [
      {
        "path": "requirements.txt",
        "name": "requirements.txt",
        "type": "file",
        "size": 850,
        "importance": "high"
      }
    ],
    "medium": [],
    "low": []
  },
  "truncated": false
}
```

## Configuration

### GitHub Token (Optional but Recommended)

Set a GitHub personal access token for higher rate limits:

```bash
# .env file
GITHUB_TOKEN=ghp_your_token_here
```

**Rate Limits:**
- Without token: 60 requests/hour
- With token: 5000 requests/hour

### Creating a GitHub Token

1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Select scopes: `public_repo` (for public repositories)
4. Copy token and add to `.env` file

## Architecture

### Service Layer (`github_tree_service.py`)
- `GitHubTreeService`: Main service class
- `fetch_repository_tree()`: Fetches complete tree structure
- `_should_filter_path()`: Applies filtering logic
- `_detect_importance()`: Detects file importance
- `get_github_tree_service()`: Singleton instance getter

### Models (`models/github.py`)
- `TreeNode`: Represents a file or directory node
- `RepositoryTree`: Complete tree structure with metadata
- `TreeFetchRequest`: Request model for tree fetching
- `FileType`: Enum for file/directory types
- `ImportanceLevel`: Enum for importance levels

### API Routes (`api/routes/github.py`)
- `POST /api/fetch-repo-tree`: Fetch tree by URL
- `GET /api/repo-tree/{owner}/{repo}`: Fetch tree by owner/repo

## Performance Optimization

### Memory Efficiency
- Uses streaming API responses
- Processes tree items incrementally
- No repository cloning or file downloads
- Singleton service instance with connection pooling

### API Efficiency
- Single recursive API call for entire tree
- Reuses HTTP session across requests
- Implements proper timeout handling
- Efficient filtering at processing time

### Scalability
- Handles repositories with 10,000+ files
- Supports truncated trees for very large repos
- Optional max_depth parameter for limiting scope
- Lightweight filtering reduces memory footprint

## Error Handling

The service handles various error scenarios:

```python
from app.services.github_tree_service import GitHubTreeServiceError

try:
    tree = tree_service.fetch_repository_tree("owner", "repo")
except GitHubTreeServiceError as e:
    if "not found" in str(e).lower():
        # Repository or branch not found
        print("Repository not found")
    elif "rate limit" in str(e).lower():
        # Rate limit exceeded
        print("Rate limit exceeded")
    else:
        # Other API errors
        print(f"API error: {e}")
```

## Testing

Run the test suite:

```bash
# Run all tree service tests
pytest backend/tests/test_github_tree_service.py -v

# Run specific test
pytest backend/tests/test_github_tree_service.py::TestGitHubTreeService::test_detect_importance_critical_files -v

# Run with coverage
pytest backend/tests/test_github_tree_service.py --cov=app.services.github_tree_service
```

## Use Cases

### 1. ML Project Analysis
Quickly identify training scripts, model architectures, and configuration files in ML repositories.

### 2. Medical AI Research
Find inference scripts, data preprocessing pipelines, and model checkpoints in medical AI projects.

### 3. Code Structure Analysis
Understand repository organization without cloning large codebases.

### 4. Dependency Discovery
Locate requirements files, environment configurations, and setup scripts.

### 5. Documentation Mapping
Find README files, documentation directories, and example code.

## Limitations

1. **Truncated Trees**: Very large repositories (>100,000 files) may return truncated results
2. **Rate Limits**: Unauthenticated requests limited to 60/hour
3. **Private Repositories**: Requires authentication token with appropriate permissions
4. **Binary Content**: Does not fetch file contents, only metadata
5. **Submodules**: Git submodules are not recursively fetched

## Future Enhancements

- [ ] Parallel tree fetching for multiple repositories
- [ ] Caching layer for frequently accessed repositories
- [ ] Custom filtering rules via configuration
- [ ] File content preview for important files
- [ ] Repository comparison and diff analysis
- [ ] Integration with code analysis tools

## Examples

### Example 1: Analyze TensorFlow Repository
```python
tree = tree_service.fetch_repository_tree(
    owner="tensorflow",
    repo="tensorflow",
    branch="master",
    max_depth=2
)

print(f"Found {len(tree.important_files['critical'])} critical files")
for file in tree.important_files['critical']:
    print(f"  - {file.path}")
```

### Example 2: Find All Jupyter Notebooks
```python
tree = tree_service.fetch_repository_tree("owner", "repo")

notebooks = [f for f in tree.files if f.path.endswith('.ipynb')]
print(f"Found {len(notebooks)} notebooks:")
for nb in notebooks:
    print(f"  - {nb.path}")
```

### Example 3: Get Configuration Files
```python
tree = tree_service.fetch_repository_tree("owner", "repo")

config_files = tree.important_files['high']
print("Configuration files:")
for file in config_files:
    if 'config' in file.name.lower() or 'settings' in file.name.lower():
        print(f"  - {file.path}")
```

## Support

For issues, questions, or contributions:
- GitHub Issues: [NeuroCode-AI Repository](https://github.com/your-org/neurocode-ai)
- Documentation: This README
- API Docs: http://localhost:8000/docs (when server is running)

## License

Part of the NeuroCode AI project. See main repository for license information.

---

**Made with Bob** 🤖