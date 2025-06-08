from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from app.database import get_db
from app.models.user import User
from app.core.config import settings
from typing import Optional

# For required authentication - auto_error=True (default)
security = HTTPBearer(
    scheme_name="JWT",
    description="Enter JWT access token in format: 'Bearer <token>'",
    auto_error=True
)

# For optional authentication - auto_error=False
optional_security = HTTPBearer(
    scheme_name="JWT",
    description="Enter JWT access token in format: 'Bearer <token>'",
    auto_error=False
)

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency that requires valid authentication credentials.
    Raises 401 Unauthorized if credentials are missing or invalid.
    """
    return _get_user_from_credentials(credentials, db)

def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(optional_security),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Dependency that provides the current user if valid credentials are provided,
    otherwise returns None. Used for endpoints that have optional authentication.
    """
    if credentials is None:
        return None
    return _get_user_from_credentials(credentials, db, raise_error=False)

def _get_user_from_credentials(
    credentials: HTTPAuthorizationCredentials,
    db: Session,
    raise_error: bool = True
) -> Optional[User]:
    """
    Internal helper function to validate credentials and return user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": f"Bearer"},
    )
    
    try:
        # Verify token prefix
        if credentials.scheme.lower() != "bearer":
            if raise_error:
                raise credentials_exception
            return None
            
        token = credentials.credentials
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if not user_id:
            if raise_error:
                raise credentials_exception
            return None
    except JWTError:
        if raise_error:
            raise credentials_exception
        return None

    user = db.query(User).filter(User.id == user_id).first()
    
    # Check if user exists and is active
    if not user or not user.is_active:
        if raise_error:
            raise credentials_exception
        return None
        
    return user

# Role-based access dependency
def require_role(roles: list):
    """
    Dependency that requires the user to have one of the specified roles.
    """
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user
    return role_checker