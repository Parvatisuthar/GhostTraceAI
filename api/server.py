from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import time
from .models import AuditRequest, AuditResponse
from .rag_proxy import call_rag_engine

app = FastAPI(
    title="🕵️ GhostTrace AI API",
    description="RAG-powered Contract Risk Auditor",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS for Streamlit localhost:8501
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/audit", response_model=AuditResponse)
async def audit_contract(request: AuditRequest):
    """🔍 Main endpoint: Analyze query against indexed documents"""
    try:
        result = await call_rag_engine(request)
        return AuditResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG Error: {str(e)}")

@app.get("/health")
async def health_check():
    """✅ Health check for production"""
    return {
        "status": "healthy",
        "service": "GhostTrace API",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
    }

@app.get("/")
async def root():
    return {"message": "🚀 GhostTrace AI - POST /audit to start auditing"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

