import os
import uuid

from django.contrib.auth import get_user_model
from django.utils.text import slugify


def image_file_path(instance, filename):
    catalog = "posts"
    _attr = instance.title
    if isinstance(instance, get_user_model()):
        catalog = "avatars"
        _attr = instance.email
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(_attr)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads", catalog, filename)
