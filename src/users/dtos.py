from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):

    email: str
    username: str
    password: str
    name: str 
    mobile_number: str | None = None


class UserResponseSchema(BaseModel):

    email: str
    username: str
    id: int
    name: str 
    mobile_number: str | None = None

class LoginSchema(BaseModel):
    username: str
    password: str
