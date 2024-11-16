from io import BytesIO

from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

pdfmetrics.registerFont(TTFont("Arial", "arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Bold", "arialbd.ttf"))


def create_pdf_by_executor(tasks):

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    begin = height - 70

    # Установка шрифта
    c.setFont("Arial-Bold", 16)

    # Заголовок
    c.drawString(160, begin, f"Сводка задач для исполнителя: {tasks[0][0]}")

    c.setFont("Arial", 14)

    y_offset = 30  # Смещение между строками
    y_start = begin - 60

    for task in tasks:
        id_task = task[0]
        title = task[1]
        detail = task[2]
        create_date_str = task[3].strftime("%Y-%m-%d")
        exec_date_str = task[4].strftime("%Y-%m-%d")
        status = task[5]
        executors = task[6].split(", ")

        # Заголовок задачи
        c.setFont("Arial-Bold", 14)
        c.drawString(50, y_start, f"Задача №{id_task} от {create_date_str}")

        # Данные задачи
        c.setFont("Arial", 14)
        title_lines = simpleSplit(title, "Arial", 14, width - 100)
        y_title = y_start - 30
        for line in title_lines:
            c.drawString(50, y_title, line)
            y_title -= 15

        # Определение количества исполнителей
        num_executors = len(executors)
        xlist = [50, 350, 550]
        y_start_task = y_start - 60

        # Создание сетки
        for i in range(num_executors + 2):  # +2 для заголовка и даты
            c.line(
                xlist[0],
                y_start_task - i * y_offset,
                xlist[-1],
                y_start_task - i * y_offset,
            )
        for x in xlist:
            c.line(
                x, y_start_task - (num_executors + 1) * y_offset, x, y_start_task
            )  # Вертикальные линии

        # Заголовки для исполнителей и даты
        c.setFont("Arial-Bold", 14)
        c.drawString(150, y_start_task - 15, "Исполнители")
        c.drawString(400, y_start_task - 15, "Дата исполнения")

        # Вставляем дату исполнения
        c.setFont("Arial", 14)
        c.drawString(420, y_start_task - 45, exec_date_str)

        # Вставляем исполнителей в сетку
        for i, exec in enumerate(executors):
            if exec is not None:
                c.drawString(
                    xlist[0] + 15, y_start_task - (i + 2) * y_offset + 15, exec
                )

        if detail != "нет":
            c.drawString(50, y_start_task - (num_executors + 3) * y_offset - 55, detail)

        c.setFont("Arial-Bold", 14)
        c.drawString(
            50, y_start_task - (num_executors + 4) * y_offset - 55, f"Статус: {status}"
        )

        # Добавление подписей
        c.drawString(
            350, y_start_task - (num_executors + 4) * y_offset - 55, "Подтверждаю: "
        )
        c.drawString(
            50, y_start_task - (num_executors + 5) * y_offset - 55, "Примечание: "
        )

        y_start = y_start_task - (num_executors + 6) * y_offset - 55

        if y_start < 50:
            c.showPage()
            y_start = height - 70

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer
