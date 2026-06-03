from sqlalchemy.orm import Session
from fastapi import APIRouter , Depends , status , HTTPException

from database import get_db
from models import User
from schemas import UserCreate , UserLogin , Token
from auth import hash_password , verify_password , create_access_token

# API router instance
router = APIRouter()


#POST / register
@router.post("/register" , response_model=Token)
def register(user: UserCreate , db: Session = Depends(get_db)):

    username = user.username
    email = user.email
    password = user.password
    hashed_password = hash_password(password=password)

    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(
            status_code=401 ,
            detail="Email already exists"
        )

    new_user = User(username=username , email=email , password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)


    my_dict = {
        "sub" : email
    }

    #token type tells the client how to use the token
    #bearer is the standard convention 
    return {"access_token" : create_access_token(my_dict) , "token_type" : "bearer"}



# POST / login
@router.post("/login", response_model=Token)
#userLogin tells that the request should be in the form of UserLogin
def login(user: UserLogin, db: Session = Depends(get_db)):

    email = user.email
    password = user.password

    #stores the entire user object
    email_exists = db.query(User).filter(User.email == email).first()

    if not email_exists:
        raise HTTPException(
            status_code=401 , 
            detail= "email doesn't exist"
        )
    
    passWord_in_database = email_exists.password

    password_verification = verify_password(password , passWord_in_database)

    if not password_verification:
        raise HTTPException(
            status_code=401 , 
            detail= "wrong password"
        )
    
    return {"access_token" : create_access_token({"sub": email}), "token_type": "bearer"}
    
