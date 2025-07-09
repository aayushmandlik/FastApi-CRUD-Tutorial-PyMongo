from fastapi import APIRouter
from models.user import User
from config.db import users_collection
from schemas.user import userEntity,usersEntity
from bson import ObjectId
user = APIRouter()

@user.get('/')
async def find_all_users():
    print(users_collection.find())
    print(usersEntity(users_collection.find()))
    return usersEntity(users_collection.find())

@user.get('/{id}')
async def find_one_user(id):
    return userEntity(users_collection.find_one({"_id":ObjectId(id)}))
    

@user.post('/')
async def create_users(user: User):
    users_collection.insert_one(dict(user))
    return usersEntity(users_collection.find())

@user.put('/{id}')
async def update_users(id,user:User):
    users_collection.find_one_and_update({"_id":ObjectId(id)},{"$set":dict(user)})
    return userEntity(users_collection.find_one({"_id":ObjectId(id)}))

@user.delete('/{id}')
async def delete_users(id,user:User):
    return userEntity(users_collection.find_one_and_delete({"_id":ObjectId(id)}))
