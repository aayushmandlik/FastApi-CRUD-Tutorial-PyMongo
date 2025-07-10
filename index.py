from fastapi import FastAPI
from routes.user import user
from routes.blogs import blogs
app = FastAPI()
app.include_router(user)
app.include_router(blogs)
