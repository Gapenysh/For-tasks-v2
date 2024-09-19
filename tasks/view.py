from tasks.crud import Tasks
from fastapi import APIRouter, Depends
from tasks.schemas import Task, TaskUpdate, TaskStatusUpdate


router = APIRouter(prefix="/tasks")


@router.get("/")
def show_tasks():
    data = Tasks.get_tasks()
    return data


@router.post("/create")
def create_task(task: Task):

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


@router.get("/{id}")
def show_task_from_id(task_id: int):
    data = Tasks.get_task_by_id(task_id)
    print(data)
    return data


@router.patch("/{id}")
def update_task_status(task_id: int, task: TaskStatusUpdate):

    success = Tasks.update_task_status(id=task_id, mark=task.status)
    if success:
        return {"message": "Task status updated successfully"}
    else:
        return {"message": "Failed to update task status"}


@router.put("/{id}/redact")
def update_task(task_id: int, task: TaskUpdate):

    success = Tasks.update_task(
        id=task_id,
        title=task.title,
        detail=task.detail,
        creat_date=task.creation_date,
        exec_date=task.execution_date,
        mark=task.execution_mark,
    )
    if success:
        return {"message": "Task updated successfully"}
    else:
        return {"message": "Failed to update task"}
