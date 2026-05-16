# GitHub Repository Metadata Fetcher Service

A lightweight, efficient service for fetching GitHub repository metadata using the GitHub REST API v3. Designed for NeuroCode AI with a focus on low RAM usage, hackathon MVP simplicity, and scalability.

## 🚀 Features

- **No Repository Cloning**: Fetches metadata via REST API only - extremely lightweight
- **Comprehensive Metadata**: Returns 20+ data points including stars, language, topics, and more
- **Clean Architecture**: Modular service design with proper separation of concerns
- **Type Safety**: Full Pydantic models for request/response validation
- **Error Handling**: Comprehensive error handling with specific exception types
- **Rate Limit Management**: Built-in rate limit checking and informative error messages
- **Authentication Support**: Optional GitHub token for higher rate limits (5000/hr vs 60/hr)
- **FastAPI Integration**: Three RESTful endpoints with OpenAPI documentation
- **Test Coverage**: Comprehensive unit and integration tests

## 📋 Architecture

```
backend/
├── app/
│   ├── models/
│   │   └── github.py              # Pydantic models for requests/responses
│   ├── services/
│   │   └── github_service.py      # Core GitHub API service
│   ├── utils/
│   │   └── github_parser.py       # URL parsing utilities
│   ├── api/
│   │   └── routes/
│   │       └── github.py          # FastAPI endpoints
│   └── core/
│       └── config.py              # Configuration management
└── tests/
    ├── test_github_service.py     # Service tests
    └── test_github_parser.py      # Parser tests
```

## 🔧 Installation

1. **Install Dependencies**:

```bash
cd backend
pip install -r requirements.txt
```

2. **Configure Environment** (Optional but recommended):

```bash
# Create .env file
echo "GITHUB_TOKEN=your_github_personal_access_token" > .env
```

To get a GitHub token:

- Go to GitHub Settings → Developer settings → Personal access tokens
- Generate new token (classic)
- No special scopes needed for public repositories
- Copy the token to your .env file

## 🎯 API Endpoints

### 1. Parse GitHub URL

**POST** `/api/parse-github-url`

Parse a GitHub URL and extract owner/repo information.

**Request**:

```json
{
  "url": "https://github.com/octocat/Hello-World"
}
```

**Response**:

```json
{
  "owner": "octocat",
  "repo": "Hello-World",
  "url": "https://github.com/octocat/Hello-World"
}
```

### 2. Fetch Repository Metadata (POST)

**POST** `/api/fetch-repo-metadata`

Fetch complete repository metadata from a GitHub URL.

**Request**:

```json
{
  "url": "https://github.com/octocat/Hello-World"
}
```

**Response**:

```json
{
  "name": "Hello-World",
  "full_name": "octocat/Hello-World",
  "description": "My first repository on GitHub!",
  "owner": {
    "login": "octocat",
    "type": "User",
    "avatar_url": "https://github.com/images/error/octocat_happy.gif"
  },
  "stars": 1500,
  "forks": 500,
  "watchers": 1500,
  "open_issues": 10,
  "primary_language": "Python",
  "topics": ["python", "fastapi", "api"],
  "default_branch": "main",
  "created_at": "2011-01-26T19:01:12Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "pushed_at": "2024-01-15T10:30:00Z",
  "size": 180,
  "is_fork": false,
  "is_archived": false,
  "is_private": false,
  "html_url": "https://github.com/octocat/Hello-World",
  "clone_url": "https://github.com/octocat/Hello-World.git",
  "ssh_url": "git@github.com:octocat/Hello-World.git",
  "homepage": "https://example.com",
  "license": "MIT"
}
```

### 3. Fetch Repository Metadata (GET)

**GET** `/api/repo-metadata/{owner}/{repo}`

Fetch metadata directly using owner and repo name.

**Example**:

```bash
curl http://localhost:8000/api/repo-metadata/octocat/Hello-World
```

### 4. Check Rate Limit

**GET** `/api/rate-limit`

Check current GitHub API rate limit status.

**Response**:

```json
{
  "status": "success",
  "rate_limit": {
    "limit": 5000,
    "remaining": 4999,
    "reset": 1234567890,
    "used": 1
  }
}
```

## 💻 Usage Examples

### Python Client Example

```python
import requests

# Fetch repository metadata
response = requests.post(
    "http://localhost:8000/api/fetch-repo-metadata",
    json={"url": "https://github.com/fastapi/fastapi"}
)

metadata = response.json()
print(f"Repository: {metadata['full_name']}")
print(f"Stars: {metadata['stars']}")
print(f"Language: {metadata['primary_language']}")
print(f"Topics: {', '.join(metadata['topics'])}")
```

### cURL Example

```bash
# Fetch metadata
curl -X POST "http://localhost:8000/api/fetch-repo-metadata" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://github.com/octocat/Hello-World"}'

# Check rate limit
curl "http://localhost:8000/api/rate-limit"
```

### JavaScript/TypeScript Example

```typescript
async function fetchRepoMetadata(url: string) {
  const response = await fetch(
    "http://localhost:8000/api/fetch-repo-metadata",
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url }),
    },
  );

  const metadata = await response.json();
  return metadata;
}

// Usage
const metadata = await fetchRepoMetadata(
  "https://github.com/octocat/Hello-World",
);
console.log(`${metadata.full_name} has ${metadata.stars} stars`);
```

## 🧪 Testing

### Run All Tests

```bash
cd backend
pytest tests/test_github_service.py -v
```

### Run Unit Tests Only

```bash
pytest tests/test_github_service.py -v -m "not integration"
```

### Run Integration Tests (requires internet)

```bash
pytest tests/test_github_service.py -v -m integration
```

### Test Coverage

```bash
pytest tests/test_github_service.py --cov=app.services.github_service --cov-report=html
```

## 🔒 Rate Limits

GitHub API has different rate limits based on authentication:

| Authentication | Rate Limit         | Reset Period |
| -------------- | ------------------ | ------------ |
| No Token       | 60 requests/hour   | 1 hour       |
| With Token     | 5000 requests/hour | 1 hour       |

**Recommendations**:

- Use a GitHub token for production
- Implement caching for frequently accessed repositories
- Monitor rate limit using the `/api/rate-limit` endpoint
- Handle `429 Too Many Requests` errors gracefully

## 🏗️ Service Architecture

### GitHubService Class

The core service class that handles all GitHub API interactions:

```python
from app.services.github_service import GitHubService

# Initialize service
service = GitHubService(token="optional_github_token")

# Fetch metadata
metadata = service.fetch_repository_metadata("owner", "repo")

# Check rate limit
rate_info = service.get_rate_limit_info()
```

### Singleton Pattern

The service uses a singleton pattern for efficient connection pooling:

```python
from app.services.github_service import get_github_service

# Always returns the same instance
service = get_github_service()
```

## 📊 Metadata Fields

The service returns the following metadata fields:

| Field              | Type    | Description                             |
| ------------------ | ------- | --------------------------------------- |
| `name`             | string  | Repository name                         |
| `full_name`        | string  | Full name (owner/repo)                  |
| `description`      | string? | Repository description                  |
| `owner`            | object  | Owner information (login, type, avatar) |
| `stars`            | integer | Number of stars                         |
| `forks`            | integer | Number of forks                         |
| `watchers`         | integer | Number of watchers                      |
| `open_issues`      | integer | Number of open issues                   |
| `primary_language` | string? | Primary programming language            |
| `topics`           | array   | Repository topics/tags                  |
| `default_branch`   | string  | Default branch name                     |
| `created_at`       | string  | Creation timestamp (ISO 8601)           |
| `updated_at`       | string  | Last update timestamp                   |
| `pushed_at`        | string  | Last push timestamp                     |
| `size`             | integer | Repository size in KB                   |
| `is_fork`          | boolean | Whether it's a fork                     |
| `is_archived`      | boolean | Whether it's archived                   |
| `is_private`       | boolean | Whether it's private                    |
| `html_url`         | string  | Web URL                                 |
| `clone_url`        | string  | HTTPS clone URL                         |
| `ssh_url`          | string  | SSH clone URL                           |
| `homepage`         | string? | Project homepage                        |
| `license`          | string? | License name                            |

## 🚨 Error Handling

The service provides specific exception types for different error scenarios:

```python
from app.services.github_service import (
    GitHubServiceError,          # Base exception
    RepositoryNotFoundError,     # 404 errors
    RateLimitError              # Rate limit exceeded
)

try:
    metadata = service.fetch_repository_metadata("owner", "repo")
except RepositoryNotFoundError:
    print("Repository not found or is private")
except RateLimitError:
    print("Rate limit exceeded - wait or use a token")
except GitHubServiceError as e:
    print(f"GitHub API error: {e}")
```

## 🎨 Supported URL Formats

The service supports multiple GitHub URL formats:

- `https://github.com/owner/repo`
- `https://github.com/owner/repo/`
- `https://github.com/owner/repo.git`
- `http://github.com/owner/repo`
- `git@github.com:owner/repo.git`

## 🔄 Integration with NeuroCode AI

This service is designed to integrate seamlessly with NeuroCode AI's codebase analysis pipeline:

1. **URL Input**: User provides GitHub repository URL
2. **Metadata Fetch**: Service fetches repository metadata (no cloning)
3. **Analysis Decision**: Use metadata to decide analysis strategy
4. **Selective Cloning**: Only clone if needed based on metadata
5. **Resource Optimization**: Metadata helps estimate resource requirements

## 📈 Performance Characteristics

- **Memory Usage**: < 50MB (no repository cloning)
- **Response Time**: 200-500ms (network dependent)
- **Concurrent Requests**: Supports multiple simultaneous requests
- **Connection Pooling**: Reuses HTTP connections for efficiency
- **Scalability**: Stateless design allows horizontal scaling

## 🛠️ Development

### Adding New Metadata Fields

1. Update `GitHubRepoMetadata` model in `app/models/github.py`
2. Update parsing logic in `github_service.py`
3. Add tests in `test_github_service.py`
4. Update documentation

### Extending Functionality

The service can be extended to support:

- Repository file tree fetching
- Commit history analysis
- Contributor information
- Branch and tag listing
- Release information
- Issue and PR statistics

## 📝 License

Part of NeuroCode AI project.

## 🤝 Contributing

When contributing to this service:

1. Maintain low memory footprint
2. Add comprehensive tests
3. Update documentation
4. Follow existing code style
5. Handle errors gracefully

---

**Made with Bob** 🤖

For questions or issues, please refer to the main NeuroCode AI documentation.
