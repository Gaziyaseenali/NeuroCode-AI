# Frontend Integration Guide

## Overview

This guide explains how to integrate the NeuroCode AI backend with a Next.js frontend for dynamic repository intelligence visualization.

## Backend Configuration

### CORS Setup

The backend is configured to accept requests from Next.js development servers:

```python
# Allowed origins
- http://localhost:3000  # Next.js default
- http://localhost:3001  # Alternative port
- http://127.0.0.1:3000
- http://127.0.0.1:3001
```

All HTTP methods and headers are allowed for development convenience.

## API Endpoints

### Frontend-Optimized Endpoint

**Primary Endpoint:** `POST /api/frontend/repository-intelligence`

This endpoint returns data optimized for dynamic UI rendering with progressive loading support.

#### Request Format

```typescript
interface IntelligenceRequest {
  url: string;              // GitHub repository URL
  branch?: string;          // Optional branch name
  include_filtered?: boolean; // Include filtered files (default: false)
  max_depth?: number;       // Maximum tree depth (default: unlimited)
}
```

#### Example Request

```typescript
const response = await fetch('http://localhost:8000/api/frontend/repository-intelligence', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    url: 'https://github.com/Project-MONAI/MONAI',
    branch: 'main',
    include_filtered: false,
    max_depth: null
  })
});

const data = await response.json();
```

#### Response Structure

```typescript
interface FrontendRepositoryIntelligence {
  // Loading state
  loading_state: 'idle' | 'loading' | 'success' | 'error';
  processing_progress?: {
    stage: ProcessingStage;
    progress: number;        // 0-100
    message: string;
    estimated_time_remaining?: number; // seconds
  };
  
  // Basic info
  owner: string;
  repo: string;
  branch: string;
  
  // Metadata card (for hero section)
  metadata_card?: {
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
  };
  
  // Framework visualization
  frameworks: Array<{
    name: string;
    confidence: 'high' | 'medium' | 'low';
    category: 'ml' | 'medical' | 'data' | 'other';
    icon?: string;
    color?: string;
    evidence_count: number;
  }>;
  
  // Workflow graph nodes
  workflow_nodes: Array<{
    id: string;
    label: string;
    type: string;
    confidence: 'high' | 'medium' | 'low';
    files: string[];
    has_implementation: boolean;
  }>;
  
  // Medical AI signals
  medical_signals: Array<{
    signal_type: string;
    confidence: 'high' | 'medium' | 'low';
    description: string;
    evidence: string[];
    icon?: string;
  }>;
  
  // Important files
  important_files: Array<{
    path: string;
    name: string;
    importance: 'critical' | 'high' | 'medium' | 'low';
    category: string;
    description: string;
    size?: number;
  }>;
  
  // Classification
  classification: {
    primary_type: string;
    secondary_types: string[];
    confidence: string;
    is_medical_ai: boolean;
    medical_confidence: string;
  };
  
  // Statistics
  statistics: {
    total_files: number;
    filtered_files: number;
    python_files: number;
    notebook_files: number;
    config_files: number;
    has_requirements: boolean;
    has_dockerfile: boolean;
    has_readme: boolean;
    has_tests: boolean;
    has_ci_cd: boolean;
  };
  
  // LLM summary
  llm_summary?: string;
  
  // Metadata
  analyzed_at: string;
  processing_time_ms?: number;
}
```

### Alternative GET Endpoint

**Endpoint:** `GET /api/frontend/repository-intelligence/{owner}/{repo}`

Query parameters:
- `branch` (optional): Branch name
- `include_filtered` (optional): Include filtered files
- `max_depth` (optional): Maximum tree depth

```typescript
const response = await fetch(
  'http://localhost:8000/api/frontend/repository-intelligence/Project-MONAI/MONAI?branch=main'
);
```

## Processing Stages

The backend processes repositories in stages, useful for progressive loading UI:

1. **`parsing`**: Parsing repository URL
2. **`fetching_metadata`**: Fetching repository metadata from GitHub
3. **`analyzing_structure`**: Analyzing file structure and tree
4. **`detecting_frameworks`**: Detecting frameworks and technologies
5. **`generating_intelligence`**: Generating final intelligence report
6. **`complete`**: Analysis complete

## Error Handling

### Error Response Format

```typescript
interface FrontendErrorResponse {
  loading_state: 'error';
  error: {
    error_type: string;
    message: string;
    stage?: ProcessingStage;
    retry_possible: boolean;
    suggestions: string[];
  };
  timestamp: string;
}
```

### Common Error Types

1. **InvalidGitHubURL** (400)
   - Invalid repository URL format
   - Not retryable
   - Suggestions: Check URL format

2. **RepositoryNotFound** (404)
   - Repository doesn't exist or is private
   - Not retryable
   - Suggestions: Verify repository exists and is public

3. **RateLimitExceeded** (429)
   - GitHub API rate limit exceeded
   - Retryable after waiting
   - Suggestions: Add GITHUB_TOKEN, wait for reset

4. **IntelligenceServiceError** (500)
   - Internal processing error
   - Retryable
   - Suggestions: Try again, check logs

### Error Handling Example

```typescript
try {
  const response = await fetch(endpoint, options);
  
  if (!response.ok) {
    const errorData = await response.json();
    
    // Handle specific error types
    if (errorData.error.error_type === 'RateLimitExceeded') {
      // Show rate limit message with suggestions
      showRateLimitError(errorData.error.suggestions);
    } else if (errorData.error.retry_possible) {
      // Show retry button
      showRetryableError(errorData.error.message);
    } else {
      // Show permanent error
      showError(errorData.error.message);
    }
  }
  
  const data = await response.json();
  // Process successful response
} catch (error) {
  // Handle network errors
  showNetworkError();
}
```

## Progressive Loading Pattern

### Staged Data Reveal

The response structure supports progressive UI updates:

```typescript
// Stage 1: Show metadata card immediately
if (data.metadata_card) {
  renderMetadataCard(data.metadata_card);
}

// Stage 2: Render frameworks
if (data.frameworks.length > 0) {
  renderFrameworkVisualization(data.frameworks);
}

// Stage 3: Render workflow graph
if (data.workflow_nodes.length > 0) {
  renderWorkflowGraph(data.workflow_nodes);
}

// Stage 4: Show medical AI signals
if (data.medical_signals.length > 0) {
  renderMedicalSignals(data.medical_signals);
}

// Stage 5: Display important files
if (data.important_files.length > 0) {
  renderImportantFiles(data.important_files);
}
```

### Loading State Management

```typescript
const [loadingState, setLoadingState] = useState<LoadingState>('idle');
const [progress, setProgress] = useState(0);
const [currentStage, setCurrentStage] = useState<string>('');

// Simulate progressive loading (actual implementation would use SSE or polling)
const analyzeRepository = async (url: string) => {
  setLoadingState('loading');
  setProgress(0);
  setCurrentStage('Parsing repository...');
  
  try {
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url })
    });
    
    const data = await response.json();
    
    if (data.loading_state === 'success') {
      setLoadingState('success');
      setProgress(100);
      return data;
    }
  } catch (error) {
    setLoadingState('error');
    throw error;
  }
};
```

## UI Component Mapping

### 1. Repository Metadata Card

```typescript
interface MetadataCardProps {
  data: FrontendRepositoryIntelligence['metadata_card'];
}

const MetadataCard: React.FC<MetadataCardProps> = ({ data }) => (
  <div className="metadata-card">
    <h1>{data.name}</h1>
    <p>{data.description}</p>
    <div className="stats">
      <span>⭐ {data.stars}</span>
      <span>🔱 {data.forks}</span>
      <span>💻 {data.language}</span>
    </div>
    <div className="topics">
      {data.topics.map(topic => (
        <span key={topic} className="topic-badge">{topic}</span>
      ))}
    </div>
  </div>
);
```

### 2. Framework Visualization

```typescript
const FrameworkBadge: React.FC<{ framework: Framework }> = ({ framework }) => (
  <div 
    className="framework-badge"
    style={{ borderColor: framework.color }}
  >
    <span className="icon">{framework.icon}</span>
    <span className="name">{framework.name}</span>
    <span className={`confidence ${framework.confidence}`}>
      {framework.confidence}
    </span>
  </div>
);
```

### 3. Workflow Graph

```typescript
const WorkflowGraph: React.FC<{ nodes: WorkflowNode[] }> = ({ nodes }) => {
  // Use a graph library like react-flow or d3
  return (
    <div className="workflow-graph">
      {nodes.map(node => (
        <div key={node.id} className={`workflow-node ${node.type}`}>
          <h3>{node.label}</h3>
          <span className={`confidence ${node.confidence}`}>
            {node.confidence}
          </span>
          {node.has_implementation && (
            <ul className="files">
              {node.files.map(file => (
                <li key={file}>{file}</li>
              ))}
            </ul>
          )}
        </div>
      ))}
    </div>
  );
};
```

### 4. Medical AI Signals

```typescript
const MedicalSignalCard: React.FC<{ signal: MedicalAISignalCard }> = ({ signal }) => (
  <div className="medical-signal-card">
    <div className="icon">{signal.icon}</div>
    <h3>{signal.signal_type}</h3>
    <p>{signal.description}</p>
    <span className={`confidence ${signal.confidence}`}>
      {signal.confidence} confidence
    </span>
    <details>
      <summary>Evidence ({signal.evidence.length} files)</summary>
      <ul>
        {signal.evidence.map(file => (
          <li key={file}>{file}</li>
        ))}
      </ul>
    </details>
  </div>
);
```

### 5. Important Files List

```typescript
const ImportantFilesList: React.FC<{ files: ImportantFileHighlight[] }> = ({ files }) => {
  const groupedFiles = files.reduce((acc, file) => {
    if (!acc[file.importance]) acc[file.importance] = [];
    acc[file.importance].push(file);
    return acc;
  }, {} as Record<string, ImportantFileHighlight[]>);
  
  return (
    <div className="important-files">
      {Object.entries(groupedFiles).map(([importance, fileList]) => (
        <div key={importance} className={`file-group ${importance}`}>
          <h3>{importance.toUpperCase()} Files</h3>
          {fileList.map(file => (
            <div key={file.path} className="file-item">
              <span className="name">{file.name}</span>
              <span className="category">{file.category}</span>
              <p className="description">{file.description}</p>
            </div>
          ))}
        </div>
      ))}
    </div>
  );
};
```

## Performance Optimization

### 1. Caching Strategy

```typescript
// Cache responses to avoid repeated API calls
const cache = new Map<string, FrontendRepositoryIntelligence>();

const fetchWithCache = async (url: string) => {
  const cacheKey = url;
  
  if (cache.has(cacheKey)) {
    return cache.get(cacheKey);
  }
  
  const data = await fetchRepositoryIntelligence(url);
  cache.set(cacheKey, data);
  
  return data;
};
```

### 2. Debounced Search

```typescript
import { useMemo } from 'react';
import debounce from 'lodash/debounce';

const useRepositorySearch = () => {
  const debouncedSearch = useMemo(
    () => debounce(async (url: string) => {
      return await fetchRepositoryIntelligence(url);
    }, 500),
    []
  );
  
  return debouncedSearch;
};
```

### 3. Lazy Loading Components

```typescript
import dynamic from 'next/dynamic';

const WorkflowGraph = dynamic(() => import('./WorkflowGraph'), {
  loading: () => <div>Loading workflow graph...</div>,
  ssr: false
});

const MedicalSignals = dynamic(() => import('./MedicalSignals'), {
  loading: () => <div>Loading medical signals...</div>
});
```

## Environment Configuration

### Backend URL Configuration

```typescript
// .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
```

```typescript
// lib/api.ts
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const fetchRepositoryIntelligence = async (url: string) => {
  const response = await fetch(`${API_URL}/api/frontend/repository-intelligence`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url })
  });
  
  if (!response.ok) {
    throw new Error('Failed to fetch repository intelligence');
  }
  
  return response.json();
};
```

## Testing

### Example Test

```typescript
import { render, screen, waitFor } from '@testing-library/react';
import { rest } from 'msw';
import { setupServer } from 'msw/node';
import RepositoryAnalysis from './RepositoryAnalysis';

const server = setupServer(
  rest.post('http://localhost:8000/api/frontend/repository-intelligence', (req, res, ctx) => {
    return res(ctx.json({
      loading_state: 'success',
      owner: 'test',
      repo: 'repo',
      metadata_card: {
        name: 'Test Repo',
        stars: 100,
        // ... other fields
      },
      frameworks: [],
      workflow_nodes: [],
      medical_signals: [],
      important_files: []
    }));
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

test('renders repository analysis', async () => {
  render(<RepositoryAnalysis url="https://github.com/test/repo" />);
  
  await waitFor(() => {
    expect(screen.getByText('Test Repo')).toBeInTheDocument();
  });
});
```

## Rate Limiting

The backend uses GitHub API which has rate limits:
- **Without token**: 60 requests/hour
- **With token**: 5000 requests/hour

To increase limits, set `GITHUB_TOKEN` in backend `.env` file.

## Best Practices

1. **Always handle errors gracefully** with user-friendly messages
2. **Show loading states** during API calls
3. **Cache responses** to reduce API calls
4. **Debounce search inputs** to avoid excessive requests
5. **Use progressive loading** to improve perceived performance
6. **Display retry options** for retryable errors
7. **Show rate limit warnings** proactively
8. **Implement proper TypeScript types** for type safety
9. **Use React Query or SWR** for better data fetching
10. **Test with various repository types** (ML, medical, general)

## Troubleshooting

### CORS Issues

If you encounter CORS errors:
1. Verify backend is running on port 8000
2. Check frontend is on allowed origin (localhost:3000)
3. Ensure CORS middleware is properly configured
4. Check browser console for specific CORS errors

### Rate Limit Issues

If hitting rate limits:
1. Add `GITHUB_TOKEN` to backend `.env`
2. Implement request caching
3. Show rate limit status to users
4. Add retry logic with exponential backoff

### Slow Response Times

If responses are slow:
1. Use `max_depth` parameter to limit tree depth
2. Set `include_filtered: false` to skip unnecessary files
3. Implement loading states and progress indicators
4. Consider server-side caching

## Support

For issues or questions:
- Check backend logs for detailed error messages
- Review API documentation at `http://localhost:8000/docs`
- Test endpoints using the interactive Swagger UI
- Check GitHub API status if experiencing issues

---

**Made with Bob** 🤖

Last Updated: 2026-05-16