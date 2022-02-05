import io
import sys
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile


def edit_image(image):
    name = image.name
    size = 500, 500
    image = Image.open(image).convert("RGBA")
    image.thumbnail(size)
    wm = Image.open('media/watermark.png').convert("RGBA")
    image.paste(wm, (0, 0), mask=wm)
    stream = io.BytesIO()
    image.save(stream, 'PNG', quality=90)
    data = InMemoryUploadedFile(stream, 'ImageField', name, 'PNG/image', sys.getsizeof(stream), charset=None)
    return data
