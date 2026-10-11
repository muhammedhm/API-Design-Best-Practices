from webbrowser import get

from fastapi import APIRouter, Request,status,Depends, BackgroundTasks
from src.users import controller
from src.utils.db import get_db
from sqlalchemy.orm import Session
from src.users.dtos import UserResponseSchema, UserSchema, LoginSchema



user_router = APIRouter(prefix="/user", tags=["Users"])


@user_router.post("/register",response_model=UserResponseSchema,status_code=status.HTTP_201_CREATED,summary="register a new user", description="register a new user with the information provided")
async def register(body: UserSchema, bg_task: BackgroundTasks,db: Session = Depends(get_db)):
    return await controller.register(body,db,bg_task)

@user_router.post("/login",status_code=status.HTTP_200_OK,summary="login a user", description="login a user with the information provided")
def login(body: LoginSchema, db: Session = Depends(get_db)):
    return controller.login_user(body,db)

@user_router.get("/is_auth",response_model=UserResponseSchema,status_code=status.HTTP_200_OK,summary="check if user is authenticated", description="check if user is authenticated with the information provided")
def is_auth(request: Request,db: Session = Depends(get_db)):
    return controller.is_authenticated(request,db)