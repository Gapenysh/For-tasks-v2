from fastapi import APIRouter

from tasks.crud import Tasks

router = APIRouter(prefix="/test")


@router.put("/{id}/download")
def download_pdf(id: int):
    task = Tasks.get_task_from_id(id)
    buffer = create_pdf(task)

    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"task_details_{task_id}.pdf",
        mimetype="application/pdf",
    )
