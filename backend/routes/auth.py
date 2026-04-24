"""
Authentication routes - OAuth integration with backend-driven flow.
Supports Google, Swiggy, and other OAuth providers.
"""

from fastapi import APIRouter, HTTPException, Response, Cookie, Depends
from pydantic import BaseModel
from typing import Optional
import json
import uuid
from datetime import datetime, timedelta

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    """OAuth login request."""
    provider: str  # "google", "swiggy", etc.


class LoginResponse(BaseModel):
    """OAuth login response with auth URL."""
    auth_url: str
    state: str


class CallbackRequest(BaseModel):
    """OAuth callback with authorization code."""
    code: str
    state: str
    provider: str


class UserInfo(BaseModel):
    """User info response."""
    id: str
    email: str
    name: str
    provider: str


# Mock OAuth configuration
OAUTH_CONFIGS = {
    "google": {
        "client_id": "YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com",
        "client_secret": "YOUR_GOOGLE_CLIENT_SECRET",
        "auth_url": "https://accounts.google.com/o/oauth2/v2/auth",
        "token_url": "https://oauth2.googleapis.com/token",
        "scope": "openid email profile"
    },
    "swiggy": {
        "client_id": "YOUR_SWIGGY_CLIENT_ID",
        "client_secret": "YOUR_SWIGGY_CLIENT_SECRET",
        "auth_url": "https://api.swiggy.com/oauth2/authorize",
        "token_url": "https://api.swiggy.com/oauth2/token",
        "scope": "orders profile"
    }
}

# In-memory session store (in production: Redis)
SESSIONS = {}


@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """
    Initiate OAuth flow.
    Returns authorization URL for frontend redirect.
    """
    provider = request.provider.lower()
    
    if provider not in OAUTH_CONFIGS:
        raise HTTPException(status_code=400, detail=f"Provider {provider} not supported")

    config = OAUTH_CONFIGS[provider]
    state = str(uuid.uuid4())
    
    # Store state in session (in production: secure session store)
    SESSIONS[state] = {
        "provider": provider,
        "created_at": datetime.utcnow().isoformat(),
        "expires_at": (datetime.utcnow() + timedelta(minutes=10)).isoformat()
    }

    # Build authorization URL
    auth_params = {
        "client_id": config["client_id"],
        "redirect_uri": "http://localhost:3000/auth/callback",
        "response_type": "code",
        "scope": config["scope"],
        "state": state
    }
    
    param_string = "&".join([f"{k}={v}" for k, v in auth_params.items()])
    auth_url = f"{config['auth_url']}?{param_string}"

    return LoginResponse(auth_url=auth_url, state=state)


@router.post("/callback")
async def callback(request: CallbackRequest, response: Response):
    """
    OAuth callback handler.
    Exchanges authorization code for access token.
    Sets HTTP-only cookie with session token.
    """
    # Validate state (CRITICAL for CSRF protection)
    if request.state not in SESSIONS:
        raise HTTPException(status_code=400, detail="Invalid or expired state")

    session = SESSIONS[request.state]
    
    # Check expiry
    expires_at = datetime.fromisoformat(session["expires_at"])
    if datetime.utcnow() > expires_at:
        del SESSIONS[request.state]
        raise HTTPException(status_code=400, detail="State expired")

    provider = session["provider"]
    
    if provider != request.provider.lower():
        raise HTTPException(status_code=400, detail="Provider mismatch")

    # In production: Exchange code for access token via HTTPS
    # For mock: Generate user info
    mock_user = {
        "id": str(uuid.uuid4()),
        "email": f"user_{uuid.uuid4().hex[:8]}@example.com",
        "name": "Test User",
        "provider": provider
    }

    # Create session token
    session_token = str(uuid.uuid4())
    SESSIONS[session_token] = {
        "user": mock_user,
        "created_at": datetime.utcnow().isoformat(),
        "expires_at": (datetime.utcnow() + timedelta(days=7)).isoformat()
    }

    # Clean up auth state
    del SESSIONS[request.state]

    # Set HTTP-only cookie
    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        secure=True,  # HTTPS only in production
        samesite="Lax",
        max_age=7 * 24 * 60 * 60  # 7 days
    )

    return {
        "status": "success",
        "user": mock_user,
        "message": "Login successful"
    }


@router.get("/me", response_model=UserInfo)
async def get_current_user(session_token: Optional[str] = Cookie(None)):
    """Get current authenticated user."""
    if not session_token or session_token not in SESSIONS:
        raise HTTPException(status_code=401, detail="Not authenticated")

    session = SESSIONS[session_token]
    user = session.get("user")
    
    if not user:
        raise HTTPException(status_code=401, detail="Session invalid")

    return UserInfo(**user)


@router.post("/logout")
async def logout(response: Response, session_token: Optional[str] = Cookie(None)):
    """Logout and clear session."""
    if session_token and session_token in SESSIONS:
        del SESSIONS[session_token]

    response.delete_cookie("session_token")
    
    return {"status": "success", "message": "Logged out"}


@router.post("/refresh")
async def refresh_token(session_token: Optional[str] = Cookie(None), response: Response = None):
    """
    Refresh session token.
    Extends expiry time.
    """
    if not session_token or session_token not in SESSIONS:
        raise HTTPException(status_code=401, detail="Not authenticated")

    session = SESSIONS[session_token]
    
    # Extend expiry
    new_expiry = datetime.utcnow() + timedelta(days=7)
    session["expires_at"] = new_expiry.isoformat()

    return {
        "status": "success",
        "expires_at": new_expiry.isoformat()
    }
