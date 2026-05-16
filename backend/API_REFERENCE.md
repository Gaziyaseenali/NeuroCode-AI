# NeuroCode AI Backend API Reference

## Base URL

```
http://localhost:8000
```

## Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Authentication

Currently, no authentication is required for API endpoints. GitHub API rate limits apply based on backend configuration.

## Endpoints Overview

### Frontend-Optimized Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/frontend/repository-intelligence` | Get frontend-optimized repository intelligence |
| GET | `/api/frontend/repository-intelligence/{owner}/{repo}` | Get intelligence by owner/repo |

### Standard Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/parse-github-url` | Parse GitHub URL |
| POST | `/api/fetch-repo-metadata` | Fetch repository metadata |
| GET | `/api/repo-metadata/{owner}/{repo}` | Get metadata by owner/repo |
| POST | `/api/fetch-repo-tree` | Fetch repository tree structure |
| GET | `/api/repo-tree/{owner}/{repo}` | Get tree by owner/repo |
| POST | `/api/analyze-repository` | Analyze repository structure |
| GET | `/api/analyze-repository/{owner}/{repo}` | Analyze by owner/repo |
| POST | `/api/repository-intelligence` | Get unified intelligence |
| GET | `/api/repository-intelligence/{owner}/{repo}` | Get intelligence by owner/repo |
| GET | `/api/rate-limit` | Check GitHub API rate limit |
| GET | `/api/health` | Health check |

---

## Frontend-Optimized Endpoints

### POST /api/frontend/repository-intelligence

Get repository intelligence optimized for dynamic frontend rendering.

**Request Body:**

```json
{
  "url": "https://github.com/Project-MONAI/MONAI",
  "branch": "main",
  "include_filtered": false,
  "max_depth": null
}
```

**Parameters:**

- `url` (string, required): GitHub repository URL
- `branch` (string, optional): Branch name (defaults to default branch)
- `include_filtered` (boolean, optional): Include filtered files (default: false)
- `max_depth` (integer, optional): Maximum tree depth (default: unlimited)

**Response (200 OK):**

```json
{
  "loading_state": "success",
  "processing_progress": {
    "stage": "complete",
    "progress": 100,
    "message": "Analysis complete",
    "estimated_time_remaining": 0
  },
  "owner": "Project-MONAI",
  "repo": "MONAI",
  "branch": "main",
  "metadata_card": {
    "name": "MONAI",
    "owner": "Project-MONAI",
    "description": "AI Toolkit for Healthcare Imaging",
    "stars": 5000,
    "forks": 800,
    "language": "Python",
    "topics": ["medical-imaging", "deep-learning"],
    "html_url": "https://github.com/Project-MONAI/MONAI",
    "updated_at": "2024-01-15T10:30:00Z"
  },
  "frameworks": [
    {
      "name": "PyTorch",
      "confidence": "high",
      "category": "ml",
      "icon": "pytorch",
      "color": "#EE4C2C",
      "evidence_count": 15
    }
  ],
  "workflow_nodes": [
    {
      "id": "training",
      "label": "Model Training",
      "type": "training",
      "confidence": "high",
      "files": ["train.py", "trainer.py"],
      "has_implementation": true
    }
  ],
  "medical_signals": [
    {
      "signal_type": "MRI PROCESSING",
      "confidence": "high",
      "description": "MRI image processing detected",
      "evidence": ["mri_preprocess.py"],
      "icon": "brain-scan"
    }
  ],
  "important_files": [
    {
      "path": "train.py",
      "name": "train.py",
      "importance": "critical",
      "category": "training",
      "description": "Main training script for model training",
      "size": 15420
    }
  ],
  "classification": {
    "primary_type": "medical_imaging",
    "secondary_types": ["machine_learning"],
    "confidence": "high",
    "is_medical_ai": true,
    "medical_confidence": "high"
  },
  "statistics": {
    "total_files": 500,
    "filtered_files": 450,
    "python_files": 150,
    "notebook_files": 10,
    "config_files": 5,
    "has_requirements": true,
    "has_dockerfile": true,
    "has_readme": true,
    "has_tests": true,
    "has_ci_cd": true
  },
  "llm_summary": "Medical imaging repository using PyTorch and MONAI...",
  "analyzed_at": "2024-01-15T10:30:00Z",
  "processing_time_ms": 3500
}
```

**Error Responses:**

**400 Bad Request** - Invalid GitHub URL:
```json
{
  "loading_state": "error",
  "error": {
    "error_type": "InvalidGitHubURL",
    "message": "Invalid GitHub URL format",
    "stage": "parsing",
    "retry_possible": false,
    "suggestions": [
      "Check the GitHub URL format",
      "Ensure URL is a valid GitHub repository URL"
    ]
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

**404 Not Found** - Repository not found:
```json
{
  "loading_state": "error",
  "error": {
    "error_type": "RepositoryNotFound",
    "message": "Repository not found or inaccessible",
    "stage": "fetching_metadata",
    "retry_possible": false,
    "suggestions": [
      "Verify the repository exists",
      "Check if repository is public"
    ]
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

**429 Too Many Requests** - Rate limit exceeded:
```json
{
  "loading_state": "error",
  "error": {
    "error_type": "RateLimitExceeded",
    "message": "GitHub API rate limit exceeded",
    "stage": "fetching_metadata",
    "retry_possible": true,
    "suggestions": [
      "Wait for rate limit to reset",
      "Add GITHUB_TOKEN environment variable"
    ]
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

### GET /api/frontend/repository-intelligence/{owner}/{repo}

Get repository intelligence by owner and repo name.

**Path Parameters:**

- `owner` (string, required): Repository owner username or organization
- `repo` (string, required): Repository name

**Query Parameters:**

- `branch` (string, optional): Branch name
- `include_filtered` (boolean, optional): Include filtered files
- `max_depth` (integer, optional): Maximum tree depth

**Example:**

```bash
GET /api/frontend/repository-intelligence/Project-MONAI/MONAI?branch=main
```

**Response:** Same as POST endpoint

---

## Standard Endpoints

### POST /api/parse-github-url

Parse a GitHub repository URL and extract owner and repo name.

**Request Body:**

```json
{
  "url": "https://github.com/owner/repo"
}
```

**Response (200 OK):**

```json
{
  "owner": "owner",
  "repo": "repo",
  "url": "https://github.com/owner/repo"
}
```

---

### POST /api/fetch-repo-metadata

Fetch complete repository metadata from GitHub API.

**Request Body:**

```json
{
  "url": "https://github.com/owner/repo"
}
```

**Response (200 OK):**

```json
{
  "name": "repo",
  "full_name": "owner/repo",
  "description": "Repository description",
  "owner": {
    "login": "owner",
    "type": "User",
    "avatar_url": "https://..."
  },
  "stars": 1500,
  "forks": 500,
  "watchers": 1500,
  "open_issues": 10,
  "primary_language": "Python",
  "topics": ["python", "fastapi"],
  "default_branch": "main",
  "created_at": "2020-01-01T00:00:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "pushed_at": "2024-01-15T10:30:00Z",
  "size": 180,
  "is_fork": false,
  "is_archived": false,
  "is_private": false,
  "html_url": "https://github.com/owner/repo",
  "clone_url": "https://github.com/owner/repo.git",
  "ssh_url": "git@github.com:owner/repo.git",
  "homepage": "https://example.com",
  "license": "MIT"
}
```

---

### POST /api/fetch-repo-tree

Fetch complete repository tree structure.

**Request Body:**

```json
{
  "url": "https://github.com/owner/repo",
  "branch": "main",
  "max_depth": null,
  "include_filtered": false
}
```

**Response (200 OK):**

```json
{
  "owner": "owner",
  "repo": "repo",
  "branch": "main",
  "total_files": 150,
  "total_directories": 25,
  "filtered_files": 120,
  "filtered_directories": 20,
  "files": [
    {
      "path": "train.py",
      "name": "train.py",
      "type": "file",
      "size": 15420,
      "sha": "abc123",
      "url": "https://api.github.com/...",
      "importance": "critical"
    }
  ],
  "directories": [
    {
      "path": "src",
      "name": "src",
      "type": "directory",
      "importance": "none"
    }
  ],
  "important_files": {
    "critical": [...],
    "high": [...],
    "medium": [...]
  },
  "truncated": false
}
```

---

### POST /api/analyze-repository

Analyze repository structure and generate intelligence report.

**Request Body:**

```json
{
  "url": "https://github.com/owner/repo",
  "branch": "main"
}
```

**Response (200 OK):**

```json
{
  "owner": "owner",
  "repo": "repo",
  "repository_types": [
    {
      "type": "medical_imaging",
      "confidence": "high",
      "evidence": ["MONAI framework", "medical imaging files"]
    }
  ],
  "workflow_components": [
    {
      "component": "training",
      "confidence": "high",
      "evidence": ["train.py", "trainer.py"]
    }
  ],
  "frameworks": [
    {
      "framework": "pytorch",
      "confidence": "high",
      "evidence": ["torch imports", "model.py"]
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
    "models": ["model.py"]
  },
  "total_python_files": 150,
  "total_notebook_files": 10,
  "total_config_files": 5,
  "has_requirements": true,
  "has_dockerfile": true,
  "has_readme": true,
  "summary": "Medical imaging repository using PyTorch..."
}
```

---

### POST /api/repository-intelligence

Get unified repository intelligence (combines metadata, tree, and analysis).

**Request Body:**

```json
{
  "url": "https://github.com/owner/repo",
  "branch": "main",
  "include_filtered": false,
  "max_depth": null
}
```

**Response (200 OK):**

```json
{
  "owner": "owner",
  "repo": "repo",
  "branch": "main",
  "metadata": {
    "name": "repo",
    "full_name": "owner/repo",
    "description": "...",
    "stars": 5000,
    "forks": 800,
    "primary_language": "Python",
    "topics": ["medical-imaging"],
    "created_at": "2020-01-01T00:00:00Z",
    "updated_at": "2024-01-15T10:30:00Z",
    "size": 50000,
    "license": "Apache-2.0",
    "html_url": "https://github.com/owner/repo"
  },
  "structure": {
    "total_files": 500,
    "total_directories": 50,
    "filtered_files": 450,
    "filtered_directories": 45,
    "important_files_count": {
      "critical": 5,
      "high": 10,
      "medium": 20
    },
    "critical_files": [...],
    "high_importance_files": [...]
  },
  "classification": {
    "primary_type": "medical_imaging",
    "secondary_types": ["machine_learning"],
    "confidence": "high",
    "all_detections": [...]
  },
  "workflow": {
    "has_training": true,
    "has_inference": true,
    "has_preprocessing": true,
    "has_evaluation": true,
    "has_deployment": false,
    "components": [...]
  },
  "technology": {
    "primary_frameworks": ["pytorch", "monai"],
    "all_frameworks": [...],
    "medical_frameworks": ["monai", "simpleitk"]
  },
  "medical_context": {
    "is_medical_ai": true,
    "confidence": "high",
    "detected_signals": [...],
    "modalities": ["MRI", "CT", "DICOM"],
    "tasks": ["segmentation", "classification"]
  },
  "statistics": {
    "total_python_files": 150,
    "total_notebook_files": 10,
    "total_config_files": 5,
    "has_requirements": true,
    "has_dockerfile": true,
    "has_readme": true,
    "has_tests": true,
    "has_ci_cd": true
  },
  "llm_context": {
    "repository_overview": "Medical imaging repository...",
    "technical_summary": "Primary language: Python...",
    "key_capabilities": ["Model training", "Inference"],
    "important_files_summary": "Training: train.py...",
    "suggested_entry_points": ["README.md", "train.py"]
  },
  "analyzed_at": "2024-01-15T10:30:00Z"
}
```

---

### GET /api/rate-limit

Check GitHub API rate limit status.

**Response (200 OK):**

```json
{
  "status": "success",
  "rate_limit": {
    "limit": 5000,
    "remaining": 4950,
    "reset": 1705320600,
    "used": 50
  }
}
```

---

### GET /api/health

Health check endpoint.

**Response (200 OK):**

```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

## Data Models

### LoadingState

```typescript
type LoadingState = 'idle' | 'loading' | 'success' | 'error';
```

### ProcessingStage

```typescript
type ProcessingStage = 
  | 'parsing'
  | 'fetching_metadata'
  | 'analyzing_structure'
  | 'detecting_frameworks'
  | 'generating_intelligence'
  | 'complete';
```

### Confidence Level

```typescript
type Confidence = 'high' | 'medium' | 'low';
```

### Repository Type

```typescript
type RepositoryType = 
  | 'machine_learning'
  | 'medical_imaging'
  | 'segmentation'
  | 'research'
  | 'inference'
  | 'general';
```

### Framework Category

```typescript
type FrameworkCategory = 'ml' | 'medical' | 'data' | 'other';
```

### File Importance

```typescript
type Importance = 'critical' | 'high' | 'medium' | 'low' | 'none';
```

---

## Rate Limits

### GitHub API Limits

- **Without token**: 60 requests/hour
- **With token**: 5000 requests/hour

### Setting GitHub Token

Add to backend `.env` file:

```bash
GITHUB_TOKEN=your_github_personal_access_token
```

---

## CORS Configuration

Allowed origins:
- `http://localhost:3000`
- `http://localhost:3001`
- `http://127.0.0.1:3000`
- `http://127.0.0.1:3001`

All HTTP methods and headers are allowed.

---

## Error Codes

| Code | Description |
|------|-------------|
| 400 | Bad Request - Invalid input |
| 404 | Not Found - Repository not found |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error - Server error |

---

## Best Practices

1. **Use frontend-optimized endpoints** for UI applications
2. **Handle rate limits** gracefully with retry logic
3. **Cache responses** to reduce API calls
4. **Use query parameters** for GET endpoints when possible
5. **Check rate limit status** before making many requests
6. **Implement error handling** for all error types
7. **Use TypeScript types** for type safety
8. **Test with Swagger UI** before implementing

---

## Examples

### cURL Examples

**Fetch frontend intelligence:**

```bash
curl -X POST "http://localhost:8000/api/frontend/repository-intelligence" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://github.com/Project-MONAI/MONAI",
    "branch": "main"
  }'
```

**Check rate limit:**

```bash
curl "http://localhost:8000/api/rate-limit"
```

### JavaScript/TypeScript Examples

**Using fetch:**

```typescript
const response = await fetch('http://localhost:8000/api/frontend/repository-intelligence', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    url: 'https://github.com/Project-MONAI/MONAI',
    branch: 'main'
  })
});

const data = await response.json();
```

**Using axios:**

```typescript
import axios from 'axios';

const { data } = await axios.post(
  'http://localhost:8000/api/frontend/repository-intelligence',
  {
    url: 'https://github.com/Project-MONAI/MONAI',
    branch: 'main'
  }
);
```

---

**Made with Bob** 🤖

Last Updated: 2026-05-16