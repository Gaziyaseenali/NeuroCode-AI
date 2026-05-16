# NeuroCode AI - Frontend Boot Verification

## Overview
This document provides instructions for verifying that the Next.js frontend can successfully communicate with the FastAPI backend.

## Prerequisites
- Node.js 18+ installed
- Backend running on `http://localhost:8000`
- npm or yarn package manager

## Project Structure
```
frontend/
├── src/
│   ├── app/
│   │   ├── page.tsx          # Main verification page
│   │   ├── layout.tsx        # Root layout
│   │   └── globals.css       # Global styles
│   ├── components/
│   │   └── StatusIndicator.tsx  # Status display component
│   └── lib/
│       └── api/
│           ├── types.ts      # TypeScript types
│           ├── client.ts     # API client utilities
│           └── index.ts      # Exports
├── .env.local                # Environment variables
├── package.json              # Dependencies
└── tsconfig.json             # TypeScript config
```

## Setup Instructions

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Verify Environment Variables
Check that `.env.local` contains:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Start Backend (if not running)
In a separate terminal:
```bash
cd backend
# Activate virtual environment
.\bobenv\Scripts\activate  # Windows
source bobenv/bin/activate  # Linux/Mac

# Start backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Start Frontend
```bash
cd frontend
npm run dev
```

### 5. Open Browser
Navigate to: `http://localhost:3000`

## What Gets Tested

The verification page tests three critical endpoints:

1. **Root Endpoint** (`GET /`)
   - Verifies basic backend connectivity
   - Should return welcome message

2. **API Documentation** (`GET /docs`)
   - Verifies Swagger UI is accessible
   - Confirms API documentation is available

3. **Health Check** (`GET /api/health`)
   - Verifies health endpoint responds
   - Returns status, message, and timestamp

## Expected Results

### ✅ Success State
- All three endpoints show **OK** status
- Green indicators for each endpoint
- "All Systems Operational" badge displayed
- No error messages

### ❌ Failure State
- Red indicators for failed endpoints
- "Connection Issues Detected" badge
- Error message explaining the issue
- Possible causes:
  - Backend not running
  - Wrong port configuration
  - CORS issues
  - Network connectivity problems

## API Utilities

### Client Functions
Located in `src/lib/api/client.ts`:

- `checkRootEndpoint()` - Tests GET /
- `checkDocsEndpoint()` - Tests GET /docs
- `checkHealthEndpoint()` - Tests GET /api/health
- `checkBackendStatus()` - Comprehensive check of all endpoints
- `getApiUrl()` - Returns configured API URL

### TypeScript Types
Located in `src/lib/api/types.ts`:

- `HealthCheckResponse` - Health endpoint response
- `ApiError` - Error structure
- `BackendStatus` - Overall backend status

## Troubleshooting

### Backend Not Responding
```bash
# Check if backend is running
curl http://localhost:8000/

# Check health endpoint
curl http://localhost:8000/api/health
```

### CORS Issues
Verify backend CORS configuration in `backend/app/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Port Conflicts
- Frontend default: `3000`
- Backend default: `8000`

Change frontend port:
```bash
npm run dev -- -p 3001
```

### Environment Variables Not Loading
- Restart the dev server after changing `.env.local`
- Ensure variable names start with `NEXT_PUBLIC_`
- Check for typos in variable names

## Next Steps

After successful verification:
1. ✅ Frontend-Backend communication confirmed
2. ✅ CORS properly configured
3. ✅ API utilities working
4. 🚀 Ready to build UI components
5. 🚀 Ready to integrate GitHub API features
6. 🚀 Ready to add intelligence features

## Commands Reference

### Development
```bash
npm run dev          # Start dev server (port 3000)
npm run build        # Build for production
npm run start        # Start production server
npm run lint         # Run ESLint
```

### Testing Backend Manually
```bash
# Root endpoint
curl http://localhost:8000/

# Health check
curl http://localhost:8000/api/health

# API docs (open in browser)
http://localhost:8000/docs
```

## Technology Stack
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **API Client**: Native Fetch API
- **State Management**: React Hooks (useState, useEffect)

## File Descriptions

### Core Files
- `page.tsx` - Main verification page with status checks
- `StatusIndicator.tsx` - Reusable status display component
- `client.ts` - API client with health check functions
- `types.ts` - TypeScript type definitions

### Configuration
- `.env.local` - Environment variables (not in git)
- `tsconfig.json` - TypeScript configuration
- `next.config.mjs` - Next.js configuration
- `tailwind.config.ts` - Tailwind CSS configuration

## Notes
- This is a lightweight verification setup
- No advanced features yet (graphs, animations, etc.)
- Focus is purely on stable communication
- Ready for hackathon MVP development