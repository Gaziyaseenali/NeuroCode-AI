# NeuroCode AI Backend - Frontend Integration

## Overview

The NeuroCode AI backend has been prepared for dynamic frontend integration with Next.js. This document provides a quick start guide for frontend developers.

## What's New

### ✅ CORS Configuration
- Configured for `localhost:3000` and `localhost:3001` (Next.js default ports)
- All HTTP methods and headers allowed
- Ready for development

### ✅ Frontend-Optimized API Endpoints
- New `/api/frontend/repository-intelligence` endpoint
- Response structure optimized for dynamic UI rendering
- Progressive loading support with stage indicators
- Frontend-friendly error responses

### ✅ Response Structure
Responses are structured for easy UI component mapping:
- **Metadata Card**: Repository info for hero section
- **Framework Visualization**: Detected frameworks with colors and icons
- **Workflow Graph**: Workflow nodes for graph rendering
- **Medical AI Signals**: Medical AI capabilities with descriptions
- **Important Files**: Key files with categories and context

### ✅ Loading States
- `idle`: Not started
- `loading`: In progress
- `success`: Completed successfully
- `error`: Failed with detailed error info

### ✅ Processing Stages
1. `parsing`: Parsing repository URL
2. `fetching_metadata`: Fetching from GitHub
3. `analyzing_structure`: Analyzing files
4. `detecting_frameworks`: Detecting technologies
5. `generating_intelligence`: Generating report
6. `complete`: Analysis complete

## Quick Start

### 1. Start Backend Server

```bash
cd backend
# Activate virtual environment
.\bobenv\Scripts\activate  # Windows
source bobenv/bin/activate  # Linux/Mac

# Start server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Server will be available at: `http://localhost:8000`

### 2. Test API

Visit the interactive documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Or run the test script:
```bash
python test_frontend_api.py
```

### 3. Frontend Integration

#### Install Dependencies (Next.js)

```bash
npm install axios
# or
npm install swr
```

#### Create API Client

```typescript
// lib/api.ts
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface RepositoryIntelligenceRequest {
  url: string;
  branch?: string;
  include_filtered?: boolean;
  max_depth?: number;
}

export async function fetchRepositoryIntelligence(
  request: RepositoryIntelligenceRequest
) {
  const response = await fetch(
    `${API_URL}/api/frontend/repository-intelligence`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    }
  );

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error?.message || 'Failed to fetch intelligence');
  }

  return response.json();
}
```

#### Use in Component

```typescript
// components/RepositoryAnalysis.tsx
'use client';

import { useState } from 'react';
import { fetchRepositoryIntelligence } from '@/lib/api';

export default function RepositoryAnalysis() {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  const analyzeRepository = async (url: string) => {
    setLoading(true);
    setError(null);
    
    try {
      const result = await fetchRepositoryIntelligence({ url });
      setData(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      {/* Your UI components here */}
      {data?.metadata_card && (
        <div className="metadata-card">
          <h1>{data.metadata_card.name}</h1>
          <p>{data.metadata_card.description}</p>
          <div>⭐ {data.metadata_card.stars}</div>
        </div>
      )}
    </div>
  );
}
```

## API Endpoint

### POST /api/frontend/repository-intelligence

**Request:**
```json
{
  "url": "https://github.com/Project-MONAI/MONAI",
  "branch": "main",
  "include_filtered": false,
  "max_depth": null
}
```

**Response:**
```json
{
  "loading_state": "success",
  "owner": "Project-MONAI",
  "repo": "MONAI",
  "branch": "main",
  "metadata_card": {
    "name": "MONAI",
    "stars": 5000,
    "language": "Python",
    ...
  },
  "frameworks": [...],
  "workflow_nodes": [...],
  "medical_signals": [...],
  "important_files": [...],
  "classification": {...},
  "statistics": {...}
}
```

## UI Component Mapping

### 1. Metadata Card
```typescript
{data.metadata_card && (
  <Card>
    <h1>{data.metadata_card.name}</h1>
    <p>{data.metadata_card.description}</p>
    <div>⭐ {data.metadata_card.stars}</div>
    <div>🔱 {data.metadata_card.forks}</div>
  </Card>
)}
```

### 2. Framework Badges
```typescript
{data.frameworks.map(fw => (
  <Badge 
    key={fw.name}
    style={{ borderColor: fw.color }}
  >
    {fw.name} ({fw.confidence})
  </Badge>
))}
```

### 3. Workflow Graph
```typescript
{data.workflow_nodes.map(node => (
  <WorkflowNode key={node.id}>
    <h3>{node.label}</h3>
    <span>{node.confidence}</span>
    {node.files.map(file => <li>{file}</li>)}
  </WorkflowNode>
))}
```

### 4. Medical Signals
```typescript
{data.medical_signals.map(signal => (
  <SignalCard key={signal.signal_type}>
    <h3>{signal.signal_type}</h3>
    <p>{signal.description}</p>
    <span>{signal.confidence}</span>
  </SignalCard>
))}
```

### 5. Important Files
```typescript
{data.important_files.map(file => (
  <FileItem key={file.path}>
    <span>{file.name}</span>
    <span>{file.category}</span>
    <p>{file.description}</p>
  </FileItem>
))}
```

## Error Handling

```typescript
try {
  const data = await fetchRepositoryIntelligence({ url });
  // Handle success
} catch (error) {
  // Error response includes:
  // - error_type: Type of error
  // - message: Human-readable message
  // - stage: Where error occurred
  // - retry_possible: Whether to show retry button
  // - suggestions: Array of suggestions
}
```

## Environment Variables

Create `.env.local` in your Next.js project:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Documentation

- **Full Integration Guide**: `FRONTEND_INTEGRATION_GUIDE.md`
- **API Reference**: `API_REFERENCE.md`
- **Interactive Docs**: http://localhost:8000/docs

## Testing

Run the test script to verify backend is ready:

```bash
cd backend
python test_frontend_api.py
```

This will test:
- ✅ Health check
- ✅ CORS configuration
- ✅ Frontend intelligence endpoint
- ✅ Error handling
- ✅ GET endpoint

## Features

### Progressive Loading
The response structure supports staged UI updates:
1. Show metadata card immediately
2. Render frameworks
3. Display workflow graph
4. Show medical signals
5. List important files

### Cinematic Experience
- Loading states for smooth transitions
- Processing stages for progress indicators
- Estimated time remaining
- Detailed error messages with suggestions

### Optimized for Performance
- Lightweight responses
- No unnecessary data
- Structured for easy rendering
- Low RAM usage
- Fast processing

## Rate Limits

- **Without GitHub token**: 60 requests/hour
- **With GitHub token**: 5000 requests/hour

To increase limits, add `GITHUB_TOKEN` to backend `.env` file.

## Support

For issues:
1. Check backend logs
2. Visit http://localhost:8000/docs
3. Run `python test_frontend_api.py`
4. Review `FRONTEND_INTEGRATION_GUIDE.md`

## Next Steps

1. ✅ Backend is configured and ready
2. 📝 Review `FRONTEND_INTEGRATION_GUIDE.md` for detailed examples
3. 📝 Check `API_REFERENCE.md` for complete API documentation
4. 🚀 Start building your Next.js frontend
5. 🎨 Create beautiful UI components
6. 🎬 Implement cinematic loading experience

---

**Made with Bob** 🤖

Backend is ready for frontend integration! 🎉