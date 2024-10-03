from tasks.crud import Tasks
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from tasks.schemas import Task, TaskUpdate, TaskStatusUpdate
from tasks.create_pdf import create_pdf
from users.crud import Users
from users.schemas import UpdateTaskUsers

router = APIRouter(prefix="/tasks")


@router.get("/")
def show_tasks():
    data = Tasks.get_tasks()
    return data


@router.get("/{status}")
def get_tasks_from_status(status: str):
    tasks = Tasks.get_info_by_status(status=status)
    return tasks


@router.post("/create")
def create_task(task: Task):

    users = Users.get_users()
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
def show_task_from_id(id: int):
    data = Tasks.get_task_by_id(id)
    if data is None:
        return {"message": f"Task with id = {id} not found"}
    return data


@router.patch("/{id}")
def update_task_status(id: int, task: TaskStatusUpdate):
    print(task.status)

    success = Tasks.update_task_status(id=id, status=task.status)
    if success:
        return {"message": "Task status updated successfully"}
    else:
        return {"message": "Failed to update task status"}


@router.delete("/{id}")
def delete_task(id: int):
    success = Tasks.delete_task(id)
    if success is not None:
        return {"message": f"Task with id = {id} was deleted successfully"}
    else:
        return {"message": f"Task {id} wasn't deleted"}


@router.put("/{id}/redact")
def update_task(id: int, task: TaskUpdate):

    success = Tasks.update_task(
        id=id,
        title=task.title,
        detail=task.detail,
        creat_date=task.creation_date,
        exec_date=task.execution_date,
        mark=task.execution_mark,
    )
    task_from_id = show_task_from_id(id)
    if success:
        return {"message": "Task updated successfully", "task_from_id": task_from_id}
    else:
        return {"message": "Failed to update task"}


@router.get("/{id}/redact_users")
def show_task_from_id_redact_users(id: int):
    users = Tasks.get_users_from_task_id(id)
    return users


# @router.get("/{id}/redact_users")
# def show_task_from_id_redact_users(id: int):
#     data = Tasks.get_task_by_id(id)
#     print(data)
#     return data


@router.put("/{id}/redact_users")
def update_task_executors(id: int, users: UpdateTaskUsers):

    success = Tasks.update_task_executors(
        id,
        executors=users.executors,
    )

    if success:
        return {"message": "Task updated successfully"}

    else:
        return {"message": "Failed to update task"}


@router.get("/{id}/download")
def download_pdf(id: int):
    task = Tasks.get_task_by_id(task_id=id)
    if task is None:
        return {"message": f"Task with id = {id} not found"}

    file = create_pdf(task)
    print(f"Отправка пдф для {id} задачи")
    return StreamingResponse(
        file,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=task_{id}.pdf"},
    )
