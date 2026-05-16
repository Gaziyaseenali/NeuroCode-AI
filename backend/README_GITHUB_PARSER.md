# GitHub URL Parser API

A lightweight, modular GitHub repository URL parser utility for NeuroCode AI.

## Features

- ✅ Extract repository owner and repository name
- ✅ Support standard GitHub URLs
- ✅ Support trailing slash URLs
- ✅ Support .git URLs
- ✅ Support SSH format URLs
- ✅ Validate invalid URLs
- ✅ Optimized for hackathon MVP simplicity
- ✅ Low RAM usage (regex-based, no heavy dependencies)
- ✅ Structured output with Pydantic models

## Architecture

```
backend/app/
├── models/github.py           # Pydantic request/response models
├── utils/github_parser.py     # Core parsing logic
└── api/routes/github.py       # FastAPI endpoint
```

## API Endpoint

### Parse GitHub URL

**Endpoint:** `POST /api/parse-github-url`

**Request Body:**

```json
{
  "url": "https://github.com/owner/repo"
}
```

**Success Response (200 OK):**

```json
{
  "owner": "octocat",
  "repo": "Hello-World",
  "url": "https://github.com/octocat/Hello-World"
}
```

**Error Response (400 Bad Request):**

```json
{
  "detail": "Invalid GitHub URL format: URL must be a valid GitHub repository URL (e.g., https://github.com/owner/repo or git@github.com:owner/repo.git)"
}
```

## Supported URL Formats

The parser supports the following GitHub URL formats:

1. **Standard HTTPS:**
   - `https://github.com/owner/repo`
   - `http://github.com/owner/repo`

2. **With trailing slash:**
   - `https://github.com/owner/repo/`

3. **With .git extension:**
   - `https://github.com/owner/repo.git`
   - `https://github.com/owner/repo.git/`

4. **SSH format:**
   - `git@github.com:owner/repo.git`
   - `git@github.com:owner/repo`

## Usage Examples

### Using cURL

```bash
# Parse a standard GitHub URL
curl -X POST http://localhost:8000/api/parse-github-url \
  -H "Content-Type: application/json" \
  -d '{"url": "https://github.com/octocat/Hello-World"}'

# Parse a URL with .git extension
curl -X POST http://localhost:8000/api/parse-github-url \
  -H "Content-Type: application/json" \
  -d '{"url": "https://github.com/owner/repo.git"}'

# Parse an SSH URL
curl -X POST http://localhost:8000/api/parse-github-url \
  -H "Content-Type: application/json" \
  -d '{"url": "git@github.com:owner/repo.git"}'
```

### Using Python

```python
import requests

url = "http://localhost:8000/api/parse-github-url"
payload = {"url": "https://github.com/octocat/Hello-World"}

response = requests.post(url, json=payload)
data = response.json()

print(f"Owner: {data['owner']}")
print(f"Repo: {data['repo']}")
```

### Using JavaScript/Fetch

```javascript
const response = await fetch("http://localhost:8000/api/parse-github-url", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    url: "https://github.com/octocat/Hello-World",
  }),
});

const data = await response.json();
console.log(`Owner: ${data.owner}, Repo: ${data.repo}`);
```

## Direct Utility Usage

You can also use the parser utility directly in your Python code:

```python
from app.utils.github_parser import parse_github_url, InvalidGitHubURLError

try:
    owner, repo = parse_github_url("https://github.com/octocat/Hello-World")
    print(f"Owner: {owner}, Repo: {repo}")
except InvalidGitHubURLError as e:
    print(f"Error: {e}")
```

## Testing

Run the comprehensive unit tests:

```bash
# Install pytest if not already installed
pip install pytest

# Run tests
cd backend
python -m pytest tests/test_github_parser.py -v

# Run tests with coverage
python -m pytest tests/test_github_parser.py -v --cov=app.utils.github_parser
```

### Test Coverage

The test suite includes 30+ test cases covering:

- ✅ Standard HTTPS URLs
- ✅ HTTP URLs
- ✅ URLs with trailing slashes
- ✅ URLs with .git extensions
- ✅ SSH format URLs
- ✅ Repository names with hyphens, underscores, dots, and numbers
- ✅ Whitespace handling
- ✅ Invalid URLs (non-GitHub, malformed, missing parts)
- ✅ Edge cases (empty strings, None values, extra paths, query parameters)

## Performance Characteristics

- **Memory Usage:** Minimal - uses compiled regex patterns (cached)
- **Speed:** O(1) regex matching - instant parsing
- **Dependencies:** Zero additional packages beyond FastAPI/Pydantic
- **Scalability:** Stateless function - easily cacheable and horizontally scalable

## Error Handling

The parser validates URLs and provides descriptive error messages:

| Error Case     | Error Message                                                             |
| -------------- | ------------------------------------------------------------------------- |
| Empty string   | "URL cannot be empty or whitespace only"                                  |
| None value     | "URL must be a non-empty string"                                          |
| Non-GitHub URL | "Invalid GitHub URL format: URL must be a valid GitHub repository URL..." |
| Missing repo   | "Invalid GitHub URL format: URL must be a valid GitHub repository URL..." |
| Malformed URL  | "Invalid GitHub URL format: URL must be a valid GitHub repository URL..." |

## API Documentation

Once the server is running, visit:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Integration

The GitHub parser is integrated into the main FastAPI application:

```python
# backend/app/main.py
from app.api.routes import github

app.include_router(github.router)
```

## Future Enhancements

Potential improvements for future iterations:

- Add support for GitHub Enterprise URLs
- Cache parsed results for frequently accessed repositories
- Add rate limiting for production use
- Support for branch/tag/commit references in URLs
- Validation against GitHub API to verify repository existence

## License

Part of NeuroCode AI project.
