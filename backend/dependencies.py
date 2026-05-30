from auth import decode_access_token
from database import get_db
from models import User

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer

#OAuth2PasswordBearer object grabs the JWT token from the authorization header from route "auth/login"
oauth2_obj = OAuth2PasswordBearer(tokenUrl="auth/login")

#db is our database session that helps in querying the database
#token is extracted from OAuth2 object
def get_current_user(token = Depends(oauth2_obj) , db = Depends(get_db)):

    #we get the decoded string from this function using JWT token
    payload= decode_access_token(token=token)

    #sub is just a key that holds some user's email
    email = payload.get("sub")

    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid credential"
        )
    
    #finding user with the email from the decoded JWT key
    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid credential"
        )
    
    return user
    

