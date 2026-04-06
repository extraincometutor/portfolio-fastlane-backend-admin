from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from models.user import UserLogin
from database import users_collection
import hashlib
from utils.serialization import fix_id

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
async def login(user_data: UserLogin):
    try:
        user = await users_collection.find_one({"Username": user_data.username,"Status":True},{"_id":0})
        if not user:
            return JSONResponse({'Error': 'User not found'}, status_code=400)
        hashed_password = hashlib.sha512(user_data.password.encode('utf-8')).hexdigest() if user_data.password else ''
        if user['Password'] != hashed_password:
            return JSONResponse({'Error': 'Incorrect password'}, status_code=400)
        return JSONResponse({'Success': fix_id(user)}, status_code=200)
    except Exception as e:
        return JSONResponse({'Error': str(e)}, status_code=500)
