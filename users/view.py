from users.crud import Users
from fastapi import APIRouter, HTTPException
from users.schemas import User

router = APIRouter(prefix="/users")


@router.get("/")
def get_users():
    data = Users.get_users()
    if data:
        return data
    else:
        raise HTTPException(status_code=404, detail="Users not found")


@router.post("/create")
def create_users(user: User):

    success = Users.add_user(username=user.username)

    if success:
        return {"message": "User created successfully"}
    else:
        return {"message": "Failed to create user"}


@router.delete("/{id}")
def delete_users(id):
    success = Users.delete_user(id)
    if success is not None:
        return {"message": f"User with id = {id} was deleted successfully"}
    else:
        return {"message": f"User {id} wasn't deleted"}
