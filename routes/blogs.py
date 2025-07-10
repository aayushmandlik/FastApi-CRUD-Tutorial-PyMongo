from fastapi import APIRouter
from config.db import blogs_collection
from models.blogs import Blogs
from schemas.blogs import blogEntity,blogsEntity
from bson import ObjectId
blogs = APIRouter(prefix='/blogs',tags=['Blogs'])


@blogs.get('/')
async def get_blogs():
    return blogsEntity(blogs_collection.find())


@blogs.get('/{id}')
async def get_one_blog(id):
    return blogEntity(blogs_collection.find_one({"_id":ObjectId(id)}))

@blogs.post('/')
async def create_blog(blog:Blogs):
    blogs_collection.insert_one(dict(blog))
    return blogsEntity(blogs_collection.find())

@blogs.put('/{id}')
async def update_blog(id,blog:Blogs):
    blogs_collection.find_one_and_update({"_id":ObjectId(id)},{"$set":dict(blog)})
    return blogEntity(blogs_collection.find_one({"_id":ObjectId(id)}))

@blogs.delete("/{id}")
async def delete_blog(id):
    return blogEntity(blogs_collection.find_one_and_delete({"_id":ObjectId(id)}))