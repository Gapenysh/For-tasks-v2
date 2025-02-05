from io import BytesIO

from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

pdfmetrics.registerFont(TTFont("Arial", "arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Bold", "arialbd.ttf"))


def create_pdf_by_executor(tasks, username, counter, text_size):

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    begin = height - 70

    # Установка шрифта
    c.setFont("Arial-Bold", text_size + 2)

    # Заголовок
    c.drawString(200, begin, f"Контрольная карточка №{counter}")
    c.drawString(40, begin - 25, f"Сводка задач для исполнителя: {username}")

    c.setFont("Arial", text_size)

    y_offset = 30  # Смещение между строками
    y_start = begin - 60

    for i, task in enumerate(tasks):
        id_task = task[0]
        title = task[1]
        detail = task[2]
        create_date_str = task[3].strftime("%Y-%m-%d")
        exec_date_str = task[4].strftime("%Y-%m-%d")
        status = task[5]
        executors = task[6].split(",")

        # Заголовок задачи
        c.setFont("Arial-Bold", text_size + 2)
        c.drawString(
            50, y_start, f"Задача №{i + 1} от {create_date_str} до {exec_date_str}"
        )

        # Данные задачи
        c.setFont("Arial", text_size)
        title_lines = simpleSplit(title, "Arial", text_size, width - 100)
        y_title = y_start - 30
        for line in title_lines:
            c.drawString(50, y_title, line)
            y_title -= 15

        y_start -= y_offset * 3

        if y_start < 100:
            c.showPage()
            y_start = height - 35

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer
