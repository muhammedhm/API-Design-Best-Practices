from sqlalchemy.orm import Session
from src.users.models import UserModel
from src.utils.settings import settings
from fastapi import HTTPException, Request,status,Depends
import jwt
from jwt.exceptions import InvalidTokenError
from src.utils.db import get_db




def is_authenticated(request: Request, db: Session = Depends(get_db)):
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