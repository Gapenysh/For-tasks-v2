from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

pdfmetrics.registerFont(TTFont("Arial", "arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Bold", "arialbd.ttf"))


def create_pdf(data, counter, text_size):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    begin = height - 70
    id_task = data[0]
    title = data[1]
    detail = data[2]
    create_date_str = data[3].strftime("%d.%m.%Y")
    exec_date_str = data[4].strftime("%d.%m.%Y")
    status = data[5]
    executors = data[6].split(", ")

    # Установка шрифта
    c.setFont("Arial-Bold", text_size + 2)

    # Заголовок
    if text_size >= 20:
        c.drawString(
            120, begin, f"Контрольная карточка №{counter} от {create_date_str}"
        )
    else:
        c.drawString(
            160, begin, f"Контрольная карточка №{counter} от {create_date_str}"
        )

    c.setFont("Arial", text_size)

    # Данные
    title_lines = simpleSplit(title, "Arial", text_size, width - 100)
    y_title = begin - 60
    for line in title_lines:
        c.drawString(50, y_title, line)
        y_title -= 15

    # Определение количества исполнителей
    num_executors = len(executors)
    y_offset = 30  # Смещение между строками

    xlist = [50, 350, 550]
    y_start = begin - 115

    # Создание сетки
    for i in range(num_executors + 2):  # +2 для заголовка и даты
        c.line(xlist[0], y_start - i * y_offset, xlist[-1], y_start - i * y_offset)
    for x in xlist:
        c.line(
            x, y_start - (num_executors + 1) * y_offset, x, y_start
        )  # Вертикальные линии

    # Заголовки для исполнителей и даты
    c.setFont("Arial-Bold", text_size)
    c.drawString(150, y_start - 15, "Исполнители")
    if text_size >= 20:
        c.drawString(370, y_start - 15, "Дата исполнения")
    else:
        c.drawString(400, y_start - 15, "Дата исполнения")

    # Вставляем дату исполнения
    c.setFont("Arial", text_size)
    c.drawString(420, y_start - 45, exec_date_str)

    # Вставляем исполнителей в сетку
    for i, executor in enumerate(executors):
        if executor is not None:
            c.drawString(xlist[0] + 15, y_start - (i + 2) * y_offset + 15, executor)

    # if detail != "нет":
    #     c.drawString(50, begin - (num_executors + 3) * y_offset - 55, detail)

    c.setFont("Arial-Bold", text_size)
    c.drawString(50, begin - (num_executors + 4) * y_offset - 55, f"Статус: {status}")

    # Добавление подписей
    c.drawString(350, begin - (num_executors + 4) * y_offset - 55, "Подтверждаю: ")
    c.drawString(50, begin - (num_executors + 5) * y_offset - 55, "Примечание: ")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer
