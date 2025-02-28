from typing import List

from tasks.crud import Tasks
from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
from tasks.schemas import Task, TaskUpdate, TaskStatusUpdate, TaskPDFDownload
from tasks.create_pdf import create_pdf
from tasks.create_pdf_by_user import create_pdf_by_executor
from users.schemas import UpdateTaskUsers
from tasks.counter_of_download import read_file_counter, write_file_counter


router = APIRouter(prefix="/tasks")


@router.get("/")
def show_tasks():
    data = Tasks.get_tasks()
    return data


@router.get("/filter_users")
def get_task_filter_by_users(executors_id: List[int] = Query(None)):
    tasks_filter_by_executors = Tasks.filter_from_users(executors_id)
    return tasks_filter_by_executors


@router.get("/search_tasks")
def search_tasks(query: str):
    tasks = Tasks.search_tasks_by_query(query)
    return tasks


@router.get("/{status}")
def get_tasks_from_status(status: str):
    tasks = Tasks.get_info_by_status(status=status)
    return tasks


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
        success_update_executors = Tasks.update_task_executors(
            id=id,
            executors=task.executors,
        )
        if success_update_executors:
            return {
                "message": "Task updated successfully",
                "task_from_id": task_from_id,
            }
        else:
            return {"message": "Executors was not updated"}
    else:
        return {"message": "Failed to update task"}


@router.get("/{id}/redact_users")
def show_task_from_id_redact_users(id: int):
    users = Tasks.get_users_from_task_id(id)
    return users


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


@router.post("/{id}/download")
def download_pdf(id: int, download_setting: TaskPDFDownload):
    counter = read_file_counter()
    counter += 1
    write_file_counter(counter)
    task = Tasks.get_task_by_id(task_id=id)
    if task is None:
        return {"message": f"Task with id = {id} not found"}

    file = create_pdf(task, counter, download_setting.text_size)

    print(f"Отправка пдф для {id} задачи")
    headers = {
        "Content-Disposition": f"attachment; filename=KP_{str(counter)}.pdf",
        "Access-Control-Expose-Headers": "Content-Disposition",
        "X-count": str(counter),  # Разрешаем доступ к заголовку Content-Disposition
    }

    return StreamingResponse(file, media_type="application/pdf", headers=headers)


@router.get("/{status}/filter_users")
def get_task_filter_by_users_status(status: str, executors_id: List[int] = Query(None)):

    tasks_filter_status_by_executors = Tasks.filter_from_users_status(
        status, executors_id
    )
    return tasks_filter_status_by_executors


@router.post("/{id}/user_tasks_pdf")
def download_user_tasks_pdf(id: int, download_setting: TaskPDFDownload):
    counter = read_file_counter()
    counter += 1
    write_file_counter(counter)
    executor = Tasks.get_name_user_by_id(user_id=id)
    tasks = Tasks.get_all_tasks_for_user_by_id(
        user_id=id,
    )
    if tasks is None:
        return {"message": f"Tasks for executor: {executor} not founded"}
    print(tasks)

    file = create_pdf_by_executor(
        tasks=tasks,
        username=executor,
        counter=counter,
        text_size=download_setting.text_size,
    )
    print(f"Отправка всех задач в формате пдф для пользователя: {executor}")
    headers = {
        "Content-Disposition": f"attachment; filename=KP_{str(counter)}.pdf",
        "Access-Control-Expose-Headers": "Content-Disposition",
        "X-count": str(counter),  # Разрешаем доступ к заголовку Content-Disposition
    }

    return StreamingResponse(file, media_type="application/pdf", headers=headers)
