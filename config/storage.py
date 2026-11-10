"""Cloudinary-backed media storage for production property photos."""

import os
from io import BytesIO
from urllib.request import urlopen

from django.core.exceptions import ImproperlyConfigured
from django.core.files import File
from django.core.files.storage import Storage


class CloudinaryMediaStorage(Storage):
    """Store ImageField files in Cloudinary while keeping local dev on disk."""

    def __init__(self, **options):
        if not os.environ.get('CLOUDINARY_URL'):
            raise ImproperlyConfigured(
                'Set CLOUDINARY_URL to enable Cloudinary media storage.'
            )

        from cloudinary import uploader
        from cloudinary.utils import cloudinary_url

        self.uploader = uploader
        self.cloudinary_url = cloudinary_url

    def _save(self, name, content):
        if not getattr(content, 'name', None):
            content.name = name
        result = self.uploader.upload(content, resource_type='image')
        return result['public_id']

    def _open(self, name, mode='rb'):
        if mode not in ('rb', 'r'):
            raise ValueError('Cloudinary media files are read-only after upload.')
        with urlopen(self.url(name), timeout=20) as response:
            return File(BytesIO(response.read()), name=name)

    def delete(self, name):
        self.uploader.destroy(name, resource_type='image')

    def exists(self, name):
        # Cloudinary assigns a random public ID to each uploaded image.
        return False

    def url(self, name):
        return self.cloudinary_url(
            name,
            secure=True,
            resource_type='image',
        )[0]
