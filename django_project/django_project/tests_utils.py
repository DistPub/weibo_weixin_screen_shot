import os
from django.conf import settings
from django.test import TestCase

from django_project.utils import generate_user_media_image_path


class GenerateUserMediaPath(TestCase):
    """
    Test for generate user media path
    """
    def test_generate_user_media_image_path(self):
        file_path = generate_user_media_image_path(prefix='unittest')
        file_path = os.path.join(settings.MEDIA_ROOT, file_path)
        self.assertTrue(os.path.exists(file_path))
        os.remove(file_path)