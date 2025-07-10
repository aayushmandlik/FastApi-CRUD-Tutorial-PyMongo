# from pymongo import MongoClient

# conn = MongoClient("mongodb://localhost:27017")

from pymongo import MongoClient
import pymongo
# from pymongo.server_api import ServerApi
from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    MONGO_INITDB_DATABASE: str

    JWT_PUBLIC_KEY: str
    JWT_PRIVATE_KEY: str
    REFRESH_TOKEN_EXPIRES_IN: int
    ACCESS_TOKEN_EXPIRES_IN: int
    JWT_ALGORITHM: str

    CLIENT_ORIGIN: str

    class Config:
        env_file = './.env'


settings = Settings()

# uri = "mongodb+srv://aayush:aayush123@cluster0.ntcuxsx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new conn and connect to the server
conn = MongoClient(settings.DATABASE_URL)
db = conn[settings.MONGO_INITDB_DATABASE]

# dbUsers = conn.users  #Creating Database
users_collection = db['Users_Collection']   #Creating Collection for database

# dbBlog = conn.blogs
blogs_collection = db['Blogs_Collection']   #Creating Collection for database

# Another way to create collection 
# User = db.users
# Post = db.posts
# User.create_index([("email", pymongo.ASCENDING)], unique=True)
# Post.create_index([("title", pymongo.ASCENDING)], unique=True)



















# Send a ping to confirm a successful connection
# try:
#     conn.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)