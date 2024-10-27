from pydantic import BaseModel, Field
from typing import Optional

class Blog(BaseModel):
    title: str = Field(...)
    content: str = Field(...)
    author: str = Field(...)
    views: int = Field(default=0)

class UpdateBlog(BaseModel):
    title: Optional[str]
    content: Optional[str]
    author: Optional[str]
    views: Optional[int]