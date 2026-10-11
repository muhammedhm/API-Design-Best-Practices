from datetime import timedelta,datetime,timezone

from src.users.dtos import UserSchema,LoginSchema
from sqlalchemy.orm import Session
from src.users.models import UserModel
from src.utils.settings import settings
from fastapi import HTTPException, Request,status, BackgroundTasks
from pwdlib import PasswordHash
import jwt
from jwt.exceptions import InvalidTokenError
from src.utils.mail import send_email


password_hash = PasswordHash.recommended()

def get_password_hash(password):
    return password_hash.hash(password)


async def register(body : UserSchema,db : Session,bg_task: BackgroundTasks):

    
    is_user_exist = db.query(UserModel).filter((UserModel.username == body.username) | (UserModel.email == body.email)).first()

    if is_user_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="username or email already exists")

    hash_password = get_password_hash(body.password)

    new_user = UserModel(
        username=body.username,
        name = body.name,
        hashed_password=hash_password,
        email=body.email,
        mobile_number=body.mobile_number
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    ## Send Email Confirmation (bg_task will the user register and then execute the email process)

    bg_task.add_task(send_email,[new_user.email])

    return new_user

def login_user(body: LoginSchema, db: Session):
    user = db.query(UserModel).filter(UserModel.username == body.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not password_hash.verify(body.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")

    exp_time = datetime.now(timezone.utc) + timedelta(minutes=settings.EXP_TIME_MINUTES)

    print(exp_time)

    token = jwt.encode({"user_id": user.id, "exp": exp_time}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return {"token": token}


def is_authenticated(request: Request, db: Session):
    try:
        token = request.headers.get("Authorization")  #passed in the header as "Authorization": "Bearer <token>"
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")

        token = token.split(" ")[1]  #get the token from the header
        data = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = data.get("user_id")

        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User id not found")
        return user
    
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Token Expired")

    