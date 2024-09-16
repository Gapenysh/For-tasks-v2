from users.crud import Users
from fastapi import APIRouter, requests
from users.schemas import CreateUser

router = APIRouter(prefix="/user")


@router.get("/")
def get_users():
    data = Users.get_users()
    return data


@router.post("/create")
def create_users(user: CreateUser):

    success = Users.add_user(username=user.username)

    if success:
        return {"message": "User created successfully"}
    else:
        return {"message": "Failed to create user"}
