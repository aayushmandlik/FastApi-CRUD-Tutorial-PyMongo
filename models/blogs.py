from pydantic import BaseModel

class Blogs(BaseModel):
    title: str
    body: str