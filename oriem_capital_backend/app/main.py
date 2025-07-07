from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from sqlalchemy.orm import Session
from sqlalchemy import text
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from datetime import datetime
from time import time
import logging
import traceback

from app.config import settings
from app.database import get_db
from app.router_registry import ROUTERS
from slowapi.util import get_remote_address


# ===========================================
# 🔧 Logging Configuration
# ===========================================
logging.basicConfig(
    level=logging.INFO if settings.APP_ENV == "production" else logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ===========================================
# ✅ API Metadata Tags
# ===========================================
tags_metadata = [
    {"name": "Auth", "description": "User authentication endpoints"},
    {"name": "Users", "description": "Customer account management"},
    {"name": "Accounts", "description": "Bank account operations"},
    {"name": "Transactions", "description": "Transfer, deposit, withdrawal"},
    {"name": "Loans", "description": "Loan application, approval, repayment"},
    {"name": "Investments", "description": "Investment plans (future)"},
    {"name": "Admin", "description": "Admin controls and system insights"},
    {"name": "Audit Logs", "description": "System activity logs"},
    {"name": "Bill Payments", "description": "Utility and service bills"},
    {"name": "Profile", "description": "User preferences and personal info"},
    {"name": "Card Services", "description": "Debit/credit/virtual card ops"},
    {"name": "System", "description": "Health check and root info"},
]

# ===========================================
# 🚀 App Initialization
# ===========================================
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="A secure digital banking and investment backend platform.",
    docs_url=None if settings.APP_ENV == "production" else "/docs",
    redoc_url=settings.REDOC_URL if settings.APP_ENV != "production" else None,
    openapi_url="/openapi.json",
    openapi_tags=tags_metadata,
)

# ===========================================
# 🗂️ Static Files
# ===========================================
app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")

# ===========================================
# 🌐 CORS Middleware
# ===========================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===========================================
# 🛡️ Security Headers Middleware
# ===========================================
@app.middleware("http")
async def set_secure_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response

# ===========================================
# 📊 Request Logging Middleware
# ===========================================
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time()
    response = await call_next(request)
    duration = round(time() - start_time, 3)
    logger.info(f"{request.method} {request.url.path} - {duration}s")
    return response

# ===========================================
# 🧊 Rate Limiting Setup (Per User/IP)
# ===========================================
def get_user_id_or_ip(request: Request):
    user = getattr(request.state, "user", None)
    return str(user.id) if user and hasattr(user, "id") else get_remote_address(request)

limiter = Limiter(key_func=get_user_id_or_ip)
app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
def custom_rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={
            "error": "Too Many Requests",
            "detail": "Rate limit exceeded. Please wait before retrying.",
            "retry_after_seconds": exc.detail.get("remaining", 60),
            "limit": exc.detail.get("limit", "unknown"),
        },
        headers={"Retry-After": str(exc.detail.get("remaining", 60))}
    )

# ===========================================
# 🚨 Global Exception Handler
# ===========================================
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {str(exc)}")
    traceback.print_exc()
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "detail": str(exc),
            "path": request.url.path
        },
    )

# ===========================================
# ✅ Health Check Route (Fixed for Limiter)
# ===========================================
@app.get("/health", tags=["System"])
@limiter.limit("5/minute")
async def health_check(request: Request, db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {
            "status": "ok",
            "database": "connected",
            "time": datetime.utcnow().isoformat()
        }
    except Exception:
        return {
            "status": "error",
            "database": "unavailable"
        }

# ===========================================
# 👋 Welcome Route
# ===========================================
@app.get("/", tags=["System"])
def welcome():
    return {"message": "👋 Welcome to ORiem Capital Backend API"}

# ===========================================
# 🔢 Version Route
# ===========================================
@app.get("/version", tags=["System"])
def get_version():
    return {
        "version": settings.VERSION,
        "environment": settings.APP_ENV,
        "timestamp": datetime.utcnow().isoformat()
    }

# ===========================================
# 🔌 Register All Routers
# ===========================================
for router, prefix, tag in ROUTERS:
    app.include_router(router, prefix=prefix, tags=[tag])
