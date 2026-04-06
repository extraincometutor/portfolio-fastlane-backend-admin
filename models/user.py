from pydantic import BaseModel, Field

class UserLogin(BaseModel):
    username: str = Field(..., alias="username")
    password: str = Field(..., alias="password")
