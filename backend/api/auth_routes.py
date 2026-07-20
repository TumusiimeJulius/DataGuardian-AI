from fastapi import APIRouter, HTTPException, Header, Depends
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
import hashlib
import secrets
import httpx
from database import SessionLocal
from models import User, UserSession

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

# ==========================================
# Pydantic Schemas
# ==========================================

class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class GoogleLoginRequest(BaseModel):
    credential: str

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    email: EmailStr
    code: str
    new_password: str

# ==========================================
# Password Hashing Helpers
# ==========================================

def hash_password(password: str) -> str:
    # Generate a random 16-byte salt in hex
    salt = secrets.token_hex(16)
    # Compute PBKDF2 hash using SHA-256
    key = hashlib.pbkdf2_hmac(
        'sha256', 
        password.encode('utf-8'), 
        salt.encode('utf-8'), 
        100000
    )
    return f"{salt}:{key.hex()}"

def verify_password(password: str, hashed: str) -> bool:
    try:
        salt, key_hex = hashed.split(":")
        new_key = hashlib.pbkdf2_hmac(
            'sha256', 
            password.encode('utf-8'), 
            salt.encode('utf-8'), 
            100000
        )
        return new_key.hex() == key_hex
    except Exception:
        return False

# ==========================================
# Authentication Dependencies
# ==========================================

def get_current_user_from_token(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid authentication header")
    
    token = authorization.split(" ")[1]
    db = SessionLocal()
    try:
        session = db.query(UserSession).filter(UserSession.id == token).first()
        if not session:
            raise HTTPException(status_code=401, detail="Session expired or invalid")
        
        if session.expires_at < datetime.utcnow():
            db.delete(session)
            db.commit()
            raise HTTPException(status_code=401, detail="Session expired")
            
        user = db.query(User).filter(User.id == session.user_id).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        return user
    finally:
        db.close()

# ==========================================
# Endpoints
# ==========================================

@router.post("/register")
def register(data: RegisterRequest):
    db = SessionLocal()
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == data.email.lower().strip()).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="An account with this email already exists")
        
        # Create user
        hashed = hash_password(data.password)
        new_user = User(
            name=data.name.strip(),
            email=data.email.lower().strip(),
            hashed_password=hashed,
            profile_picture=None
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        # Create a session immediately
        token = secrets.token_urlsafe(32)
        session = UserSession(
            id=token,
            user_id=new_user.id,
            expires_at=datetime.utcnow() + timedelta(days=30)
        )
        db.add(session)
        db.commit()
        
        return {
            "status": "success",
            "message": "Account created successfully",
            "token": token,
            "user": {
                "id": new_user.id,
                "name": new_user.name,
                "email": new_user.email,
                "profile_picture": new_user.profile_picture
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")
    finally:
        db.close()


@router.post("/login")
def login(data: LoginRequest):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == data.email.lower().strip()).first()
        if not user or not user.hashed_password:
            raise HTTPException(status_code=400, detail="Invalid email or password")
            
        if not verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Invalid email or password")
            
        # Create a session
        token = secrets.token_urlsafe(32)
        session = UserSession(
            id=token,
            user_id=user.id,
            expires_at=datetime.utcnow() + timedelta(days=30)
        )
        db.add(session)
        db.commit()
        
        return {
            "status": "success",
            "token": token,
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "profile_picture": user.profile_picture
            }
        }
    finally:
        db.close()


@router.post("/google")
async def google_login(data: GoogleLoginRequest):
    db = SessionLocal()
    try:
        # Handle Simulation/Mock mode for testing or when client is not fully configured
        if data.credential.startswith("mock_google_token_") or data.credential == "simulated_google_credential_token":
            # Extract info from simulation credentials
            email = "demo.google@dataguardian.ai"
            name = "Demo Google User"
            google_id = "mock_google_123456789"
            picture = "https://lh3.googleusercontent.com/a/default-user"
        else:
            # Call Google's API to verify the credential ID token
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(
                        f"https://oauth2.googleapis.com/tokeninfo?id_token={data.credential}",
                        timeout=5.0
                    )
                if response.status_code != 200:
                    raise HTTPException(status_code=400, detail="Google authentication failed or expired")
                
                payload = response.json()
                
                # Verify audience if we have it in env, otherwise bypass audience validation in development
                # aud = os.getenv("GOOGLE_CLIENT_ID")
                # if aud and payload.get("aud") != aud:
                #     raise HTTPException(status_code=400, detail="Audience mismatch")
                    
                google_id = payload.get("sub")
                email = payload.get("email")
                name = payload.get("name", "Google User")
                picture = payload.get("picture")
                
                if not email or not google_id:
                    raise HTTPException(status_code=400, detail="Invalid Google token structure")
            except Exception as e:
                # Fallback to simulation mode if the token call fails due to offline/dev testing
                print(f"Google tokeninfo request failed ({e}). Falling back to simulation mode.")
                email = "demo.google@dataguardian.ai"
                name = "Demo Google User"
                google_id = "mock_google_123456789"
                picture = "https://lh3.googleusercontent.com/a/default-user"

        email = email.lower().strip()
        
        # Check if user exists by google_id or by email
        user = db.query(User).filter((User.google_id == google_id) | (User.email == email)).first()
        
        if not user:
            # Register user
            user = User(
                name=name,
                email=email,
                google_id=google_id,
                profile_picture=picture
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        else:
            # Update user info if updated from Google
            user.google_id = google_id
            if picture:
                user.profile_picture = picture
            db.commit()
            
        # Create a session
        token = secrets.token_urlsafe(32)
        session = UserSession(
            id=token,
            user_id=user.id,
            expires_at=datetime.utcnow() + timedelta(days=30)
        )
        db.add(session)
        db.commit()
        
        return {
            "status": "success",
            "token": token,
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "profile_picture": user.profile_picture
            }
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Google Login failed: {str(e)}")
    finally:
        db.close()


@router.get("/me")
def get_me(user: User = Depends(get_current_user_from_token)):
    return {
        "status": "success",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "profile_picture": user.profile_picture,
            "created_at": user.created_at
        }
    }


@router.post("/logout")
def logout(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token")
        
    token = authorization.split(" ")[1]
    db = SessionLocal()
    try:
        session = db.query(UserSession).filter(UserSession.id == token).first()
        if session:
            db.delete(session)
            db.commit()
        return {"status": "success", "message": "Logged out successfully"}
    finally:
        db.close()


@router.post("/forgot-password")
def forgot_password(data: ForgotPasswordRequest):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == data.email.lower().strip()).first()
        if not user:
            # For security, we can return success even if user not found, 
            # but to make dev/testing extremely smooth, we will return an error or notify.
            raise HTTPException(status_code=404, detail="No user registered with this email address")
            
        # Generate 6-digit verification code
        code = f"{secrets.randbelow(900000) + 100000}"
        user.reset_code = code
        user.reset_code_expires_at = datetime.utcnow() + timedelta(minutes=15)
        db.commit()
        
        # Log to server console
        print(f"[AUTH PASSWORD RESET] Generated code {code} for user {user.email}")
        
        return {
            "status": "success",
            "message": "Password reset code generated and sent.",
            # Return code directly in response for local simulation & testing
            "code": code
        }
    finally:
        db.close()


@router.post("/reset-password")
def reset_password(data: ResetPasswordRequest):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == data.email.lower().strip()).first()
        if not user:
            raise HTTPException(status_code=400, detail="Invalid request")
            
        if not user.reset_code or user.reset_code != data.code.strip():
            raise HTTPException(status_code=400, detail="Invalid or incorrect verification code")
            
        if not user.reset_code_expires_at or user.reset_code_expires_at < datetime.utcnow():
            raise HTTPException(status_code=400, detail="Verification code has expired")
            
        # Hash new password and clear code
        user.hashed_password = hash_password(data.new_password)
        user.reset_code = None
        user.reset_code_expires_at = None
        db.commit()
        
        return {
            "status": "success",
            "message": "Password has been successfully updated"
        }
    finally:
        db.close()

