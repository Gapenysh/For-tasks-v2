from tasks.crud import Tasks
from fastapi import APIRouter, requests
from tasks.schemas import CreateTask

router = APIRouter(prefix="/tasks")


@router.get("/")
def show_tasks():
    data = Tasks.get_tasks()
    return data


@router.post("/create")
def create_task(task: CreateTask):

    success = Tasks.create_task(
        title=task.title,
        detail=task.detail,
        creat_date=task.creation_date,
        exec_date=task.execution_date,
        exec_mark=task.execution_mark,
        executors=task.executors,
    )

    if success:
        return {"message": "Task created successfully"}
    else:
        return {"message": "Failed to create task"}
