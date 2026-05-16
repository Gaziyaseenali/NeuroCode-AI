from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import health, github, frontend

app = FastAPI(
    title="NeuroCode AI Backend",
    version="0.1.0",
    description="Backend API for NeuroCode AI - Repository Intelligence Analysis"
)

# Configure CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

app.include_router(health.router)
app.include_router(github.router)
app.include_router(frontend.router)

@app.get("/")
async def root():
    return {
        "status": "running",
        "message": "NeuroCode AI Backend Active",
        "version": "0.1.0",
        "docs_url": "/docs"
    }
    