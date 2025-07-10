from fastapi import APIRouter,HTTPException,status,Depends,Request
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from auth.jwt_handler import create_access_token,verify_token,create_refresh_token
from passlib.context import CryptContext
from models.user import User
from config.db import users_collection
from schemas.user import userEntity,usersEntity
from bson import ObjectId
from hashing import hash_password,pwd_context
from typing import List

user = APIRouter(prefix="/users",tags=['Users'])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='users/login')

blacklisted_tokens: List[str] = []

# Verify hashed password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Get current user using JWT
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload


def require_admin(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access only")
    return current_user

# 🔐 Login with Access + Refresh token
@user.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_record = users_collection.find_one({"email": form_data.username})
    if not user_record or not verify_password(form_data.password, user_record["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    data = {"id": str(user_record["_id"]), "email": user_record["email"], "role": user_record["role"]}
    access_token = create_access_token(data)
    refresh_token = create_refresh_token(data)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


# 🔄 Refresh Access Token
@user.post('/refresh')
async def refresh_token(refresh_token: str):
    if refresh_token in blacklisted_tokens:
        raise HTTPException(status_code=403, detail="Token has been blacklisted")

    payload = verify_token(refresh_token)
    if not payload:
        raise HTTPException(status_code=403, detail="Invalid or expired refresh token")

    new_access_token = create_access_token(payload)
    return {"access_token": new_access_token, "token_type": "bearer"}


# 🚪 Logout - Blacklist refresh token
@user.post('/logout')
async def logout(refresh_token: str):
    blacklisted_tokens.append(refresh_token)
    return {"message": "Successfully logged out"}


# 👤 Protected User Profile
@user.get('/profile')
async def get_profile(current_user: dict = Depends(get_current_user)):
    return {"message": "Welcome", "user": current_user}


# 👮‍♂️ Admin-only Route
@user.get('/admin/dashboard')
async def admin_dashboard(current_user: dict = Depends(require_admin)):
    return {"message": f"Welcome Admin {current_user['email']}"}


# ➕ Register
@user.post('/')
async def create_users(user: User):
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=409, detail="Email already exists")
    user.password = hash_password(user.password)
    users_collection.insert_one(dict(user))
    return {"message": "User registered"}



@user.get('/')
async def find_all_users():
    print(users_collection.find())
    print(usersEntity(users_collection.find()))
    return usersEntity(users_collection.find())

@user.get('/{id}')
async def find_one_user(id):
    return userEntity(users_collection.find_one({"_id":ObjectId(id)}))
    

# @user.post('/')
# async def create_users(user: User):
#     user.password = hash_password(user.password)
#     users_collection.insert_one(dict(user))
#     return usersEntity(users_collection.find())

@user.put('/{id}')
async def update_users(id,user:User):
    users_collection.find_one_and_update({"_id":ObjectId(id)},{"$set":dict(user)})
    return userEntity(users_collection.find_one({"_id":ObjectId(id)}))

@user.delete('/{id}')
async def delete_users(id,user:User):
    return userEntity(users_collection.find_one_and_delete({"_id":ObjectId(id)}))
