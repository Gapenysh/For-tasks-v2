import jinja2
import pdfkit
from datetime import datetime
from io import BytesIO
import os
import tempfile

template_path = os.path.join(os.getcwd(), "tasks", "templates")


def generate_pdf_from_html_template(tasks, counter, username, font_size):

    template_loader = jinja2.FileSystemLoader(template_path)
    template_env = jinja2.Environment(loader=template_loader)

    template = template_env.get_template("template.html")
    context = {
        "tasks": tasks,
        "executor_name": username,
        "number": counter,
        "font_size": font_size,
    }
    output_text = template.render(context)

    config = pdfkit.configuration(
        wkhtmltopdf=r"C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"
    )
    with tempfile.NamedTemporaryFile(delete=False) as temp_pdf_file:
        temp_pdf_path = temp_pdf_file.name
        pdfkit.from_string(output_text, temp_pdf_path, configuration=config)

    # Чтение содержимого временного файла в буфер
    with open(temp_pdf_path, "rb") as f:
        buffer = BytesIO(f.read())

    # Удаление временного файла
    os.remove(temp_pdf_path)
    buffer.seek(0)
    return buffer
