from openpyxl.drawing.image import Image


def insert_chart_image(ws, image_buffer, cell):
    img = Image(image_buffer)
    img.anchor = cell
    ws.add_image(img)
    return img
