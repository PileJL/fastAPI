from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException, status
import uvicorn
from pydantic import BaseModel

app = FastAPI()

#sample user model
class User(BaseModel):
    fname: str
    mname: str
    lname: str
    address: str
#sample user model for updating purposes
class UpdateUser(BaseModel):
    fname: Optional[str] = None
    mname: Optional[str] = None
    lname: Optional[str] = None
    address: Optional[str] = None

# Dictionary to hold users' data
users = {
}

# function to check if userId exist
def userIdExist(userId) -> bool:
    return userId in users

# get method to get all users
@app.get("/all-users")
def getAllUsers():
    if len(users) > 0:
        return users
    else:
        return {"Table empty": "No existing users"}

# get method to get a specific user by ID
@app.get("/user/{userId}")
def getUser(userId: int):
    try:
        return users[userId]
    except:
        raise HTTPException(status_code=404, detail="User not found")
# post method to add a user
@app.post("/add-user/{userId}")
def addUser(userId: int, user: User):
    if userIdExist(userId):
        raise HTTPException(status_code=409, detail="User ID is already taken")
    
    users[userId] = user
    return users[userId]
# put method to update user data
@app.put("/updateUser/{userId}")
def updateUesr(userId: int, user: UpdateUser):
    if not userIdExist(userId):
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.fname != None:
        users[userId].fname = user.fname
    if user.mname != None:
        users[userId].mname = user.mname
    if user.lname != None:
        users[userId].lname = user.lname

    return users[userId]
# delete method to delete a user
@app.delete("/delete-user")
def deleteUser(userId: int):
    if not userIdExist(userId):
        raise HTTPException(status_code=404, detail="User not found")
    
    del users[userId]
    return {"Success": "User deleted successfully"}