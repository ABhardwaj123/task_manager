#implementation using JWT
import os
from passlib.context import CryptContext
from dotenv import load_dotenv
from datetime import datetime , timedelta , timezone
from jose import jwt

load_dotenv()

secret_key = os.getenv("jwt_secret_key")
if not secret_key:
    raise ValueError("JWT_SECRET_KEY is missing")

algorithm = os.getenv("algorithm")
access_time_expiration = int(os.getenv("token_expire_time_minutes"))


pwd_context = CryptContext(schemes=["bcrypt"])

#password functions

def hash_password(password) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password ,hashed_password) -> bool:
    return pwd_context.verify(plain_password , hashed_password)


#JWT functions

def create_access_token(data: dict) -> str:
    #exact copy of dict so that we cant modify the original dictionary
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=access_time_expiration
    )

    to_encode.update({"exp" : expire})

    encoded_jwt = jwt.encode(
        to_encode ,
        secret_key,
        algorithm=algorithm
    )

    return encoded_jwt


def decode_access_token(token):
    
    try:
        payload = jwt.decode(
            token,
            secret_key,
            algorithms=[algorithm]
        )

        return payload

    except Exception as e:
        return None