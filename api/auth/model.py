from pydantic import BaseModel


class Token(BaseModel):
    jwt: str
    object: str


class LoginResponse(BaseModel):
    token: str
    user_id: str
    username: str
    image_url: str
