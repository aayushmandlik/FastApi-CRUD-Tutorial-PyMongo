# from pymongo import MongoClient

# conn = MongoClient("mongodb://localhost:27017")

from pymongo import MongoClient
# from pymongo.server_api import ServerApi

uri = "mongodb+srv://aayush:aayush123@cluster0.ntcuxsx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
conn = MongoClient(uri)

dbUsers = conn.users
users_collection = dbUsers['Users_Collection']

dbBlog = conn.blogs
blogs_collection = dbBlog['Blogs_Collection']

# Send a ping to confirm a successful connection
# try:
#     conn.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)