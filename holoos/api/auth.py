"""
HoloOS JWT Authentication
=========================
JWT token-based authentication.
"""

import jwt
import time
from typing import Optional, Dict, Any
from dataclasses import dataclass
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


SECRET_KEY = "holoos-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours


@dataclass
class TokenData:
    user_id: str
    username: str
    roles: list
    exp: int


class JWTManager:
    def __init__(self, secret_key: str = SECRET_KEY, algorithm: str = ALGORITHM):
        self.secret_key = secret_key
        self.algorithm = algorithm
    
    def create_access_token(self, data: Dict[str, Any], expires_delta: Optional[int] = None) -> str:
        to_encode = data.copy()
        
        if expires_delta:
            expire = int(time.time()) + expires_delta
        else:
            expire = int(time.time()) + (ACCESS_TOKEN_EXPIRE_MINUTES * 60)
        
        to_encode.update({"exp": expire})
        
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def verify_token(self, token: str) -> TokenData:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return TokenData(
                user_id=payload.get("sub", ""),
                username=payload.get("username", ""),
                roles=payload.get("roles", []),
                exp=payload.get("exp", 0)
            )
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
    
    def decode_token(self, token: str) -> Optional[Dict[str, Any]]:
        try:
            return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except:
            return None


security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)) -> TokenData:
    jwt_manager = JWTManager()
    return jwt_manager.verify_token(credentials.credentials)


# Example usage
def generate_token(user_id: str, username: str, roles: list = None) -> str:
    jwt_manager = JWTManager()
    data = {
        "sub": user_id,
        "username": username,
        "roles": roles or ["user"]
    }
    return jwt_manager.create_access_token(data)


# Token for testing
TEST_TOKEN = generate_token("user_1", "admin", ["admin", "user"])


__all__ = ["JWTManager", "security", "get_current_user", "generate_token", "TEST_TOKEN", "TokenData"]