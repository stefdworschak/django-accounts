import hashlib
from io import BytesIO
import os
from PIL import Image

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile

from .models import LANG_CHOICES, ProfileImage


def lang_choices_as_dict():
    lang_choices = []
    for lang in LANG_CHOICES:
        lang_choice = {
            'value': lang[0],
            'label': lang[1],
        }
        lang_choices.append(lang_choice)
    return lang_choices


def format_profile_photo(upload, upload_name):
    """ Crop and resize profile image """
    resize = False
    img = Image.open(upload)
    width, height = img.size
    if width < height:
        height_diff = (height-width) / 2
        img_area = (0, height_diff, width, width+height_diff)
        if width > 500:
            resize = True
    elif width > height:
        width_diff = (width-height) / 2
        img_area = (width_diff, 0, height+width_diff, height)
        if height > 500:
            resize = True
    else:
        print("No changes Needed")
    cropped_img = img.crop(img_area)
    if resize:
        maxsize = (350, 350)
        cropped_img.thumbnail(maxsize, Image.ANTIALIAS)
    thumb_io = BytesIO()
    cropped_img.save(thumb_io, format='PNG')
    pillow_image = ContentFile(thumb_io.getvalue())

    return InMemoryUploadedFile(
        pillow_image,       # file
        None,               # field_name
        upload_name,        # file name
        'image/png',       # content_type
        pillow_image.tell,  # size
        None                # content_type_extra
    )


def delete_image_in_debug(request, upload_name):
    """ Checks if run in DEBUG and removes local file to be able to save
    a new version. Not necessary in prod with AWS S3 """
    profile_image = ProfileImage.objects.filter(user=request.user.id)
    if profile_image and settings.DEBUG:
        profile_image.delete()
        if os.path.exists(f'.{settings.MEDIA_URL}{upload_name}'):
            os.remove(f'.{settings.MEDIA_URL}{upload_name}')
