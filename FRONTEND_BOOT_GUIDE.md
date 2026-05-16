# NeuroCode AI - Frontend Boot Verification Guide

## 🎯 Overview
This guide provides step-by-step instructions to verify frontend-backend communication for NeuroCode AI.

## ✅ What Has Been Implemented

### Frontend Structure
```
frontend/
├── src/
│   ├── app/
│   │   ├── page.tsx              # ✅ Verification page with status checks
│   │   ├── layout.tsx            # ✅ Updated with NeuroCode branding
│   │   └── globals.css           # ✅ Tailwind CSS styles
│   ├── components/
│   │   └── StatusIndicator.tsx   # ✅ Status display component
│   └── lib/
│       └── api/
│           ├── types.ts          # ✅ TypeScript type definitions
│           ├── client.ts         # ✅ API client with health checks
│           └── index.ts          # ✅ Module exports
├── .env.local                    # ✅ Environment variables
├── tsconfig.json                 # ✅ TypeScript configuration
└── VERIFICATION_README.md        # ✅ Detailed documentation
```

### API Utilities Created
- ✅ `checkRootEndpoint()` - Tests GET /
- ✅ `checkDocsEndpoint()` - Tests GET /docs
- ✅ `checkHealthEndpoint()` - Tests GET /api/health
- ✅ `checkBackendStatus()` - Comprehensive status check
- ✅ `getApiUrl()` - Returns configured API URL

### Backend Verification
- ✅ CORS properly configured in `backend/app/main.py`
- ✅ Allows origins: localhost:3000, localhost:3001
- ✅ All HTTP methods and headers allowed
- ✅ Health endpoint available at `/api/health`

## 🚀 Quick Start Commands

### Step 1: Start Backend (Terminal 1)
```powershell
# Navigate to backend directory
cd backend

# Activate virtual environment
.\bobenv\Scripts\activate

# Start FastAPI server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Step 2: Install Frontend Dependencies (Terminal 2)
```powershell
# Navigate to frontend directory
cd frontend

# Install dependencies (if not already installed)
npm install
```

### Step 3: Start Frontend (Same Terminal 2)
```powershell
# Start Next.js development server
npm run dev
```

**Expected Output:**
```
  ▲ Next.js 14.2.35
  - Local:        http://localhost:3000
  - Ready in 2.5s
```

### Step 4: Open Browser
Navigate to: **http://localhost:3000**

## 🎨 What You'll See

### Success State (All Systems Operational)
- ✅ **Green badge**: "All Systems Operational"
- ✅ **Root Endpoint (GET /)**: OK
- ✅ **API Docs (GET /docs)**: OK
- ✅ **Health Check (GET /api/health)**: OK
- ✅ Backend API URL displayed: `http://localhost:8000`
- ✅ Last checked timestamp

### Failure State (Connection Issues)
- ❌ **Red badge**: "Connection Issues Detected"
- ❌ Failed endpoints marked with red indicators
- ❌ Error message explaining the issue
- 🔄 **Refresh button** to retry connection

## 🧪 Manual Backend Testing

### Test Endpoints Directly
```powershell
# Test root endpoint
curl http://localhost:8000/

# Test health endpoint
curl http://localhost:8000/api/health

# Open API docs in browser
start http://localhost:8000/docs
```

### Expected Responses

**GET /** Response:
```json
{
  "status": "running",
  "message": "NeuroCode AI Backend Active",
  "version": "0.1.0",
  "docs_url": "/docs"
}
```

**GET /api/health** Response:
```json
{
  "status": "healthy",
  "message": "NeuroCode AI Backend is running",
  "timestamp": "2026-05-16T08:45:00.000Z"
}
```

## 🔧 Troubleshooting

### Issue: PowerShell Script Execution Disabled
If you see: `running scripts is disabled on this system`

**Solution:**
```powershell
# Run PowerShell as Administrator and execute:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then retry npm commands
```

### Issue: Backend Not Responding
**Check if backend is running:**
```powershell
# Test with curl
curl http://localhost:8000/

# Or open in browser
start http://localhost:8000/
```

**If not running, start it:**
```powershell
cd backend
.\bobenv\Scripts\activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Issue: Port Already in Use
**Frontend (port 3000):**
```powershell
# Use alternative port
npm run dev -- -p 3001

# Update .env.local if needed
```

**Backend (port 8000):**
```powershell
# Use alternative port
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001

# Update frontend/.env.local:
# NEXT_PUBLIC_API_URL=http://localhost:8001
```

### Issue: CORS Errors in Browser Console
**Verify CORS configuration in `backend/app/main.py`:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue: Module Not Found Errors
**Frontend:**
```powershell
cd frontend
npm install
```

**Backend:**
```powershell
cd backend
.\bobenv\Scripts\activate
pip install -r requirements.txt
```

## 📋 Verification Checklist

Before proceeding to build UI components, verify:

- [ ] Backend running on http://localhost:8000
- [ ] Frontend running on http://localhost:3000
- [ ] All three endpoints show **OK** status
- [ ] No CORS errors in browser console
- [ ] "All Systems Operational" badge displayed
- [ ] Refresh button works correctly
- [ ] No TypeScript errors in terminal
- [ ] No console errors in browser DevTools

## 🎯 Next Steps

After successful verification:

1. ✅ **Frontend-Backend Communication**: Verified
2. ✅ **CORS Configuration**: Working
3. ✅ **API Utilities**: Ready to use
4. ✅ **TypeScript Types**: Defined
5. 🚀 **Ready to build**: Dashboard UI components
6. 🚀 **Ready to integrate**: GitHub API features
7. 🚀 **Ready to add**: Intelligence features

## 📁 Key Files Reference

### Configuration
- `frontend/.env.local` - API URL configuration
- `frontend/tsconfig.json` - TypeScript settings
- `backend/app/main.py` - CORS and routes

### API Layer
- `frontend/src/lib/api/client.ts` - API functions
- `frontend/src/lib/api/types.ts` - TypeScript types

### UI Components
- `frontend/src/app/page.tsx` - Verification page
- `frontend/src/components/StatusIndicator.tsx` - Status display

### Documentation
- `frontend/VERIFICATION_README.md` - Detailed docs
- `FRONTEND_BOOT_GUIDE.md` - This file

## 🛠️ Technology Stack

- **Frontend**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Backend**: FastAPI (Python)
- **API Client**: Native Fetch API
- **State**: React Hooks

## 💡 Tips

1. **Keep both terminals open** - One for backend, one for frontend
2. **Check browser console** - For detailed error messages
3. **Use the refresh button** - To retry connection without page reload
4. **Monitor backend logs** - To see incoming requests
5. **Test endpoints manually** - Using curl or browser

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all prerequisites are installed
3. Ensure ports 3000 and 8000 are available
4. Check firewall settings if needed

---

**Status**: ✅ Frontend Boot Verification Complete
**Ready for**: Dashboard UI Development
**Focus**: Lightweight, modular, hackathon-ready MVP