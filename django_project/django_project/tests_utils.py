import os
import mock
import redis_lock

from django.conf import settings
from django.test import TestCase
from django_redis import get_redis_connection
from django_project.utils import generate_user_media_image_path, get_chrome_resource


class GenerateUserMediaPathTest(TestCase):
    """
    Test for generate user media path
    """
    def test_generate_user_media_image_path(self):
        file_path = generate_user_media_image_path(prefix='unittest')
        file_path = os.path.join(settings.MEDIA_ROOT, file_path)
        self.assertTrue(os.path.exists(file_path))
        os.remove(file_path)

    def test_generate_user_media_image_path_by_random_name(self):
        file_path = generate_user_media_image_path(name='exists', prefix='unittest')
        file_path = os.path.join(settings.MEDIA_ROOT, file_path)
        self.assertTrue(os.path.exists(file_path))

        file_path2 = generate_user_media_image_path(name='exists', prefix='unittest')
        file_path2 = os.path.join(settings.MEDIA_ROOT, file_path2)
        self.assertTrue(os.path.exists(file_path2))

        self.assertNotEqual(file_path, file_path2)
        os.remove(file_path)
        os.remove(file_path2)


class GetChromeResourceTest(TestCase):
    """
    Test for get chrome resource
    """
    def setUp(self):
        redis_lock.reset_all(get_redis_connection("default"))

    def _empty_lock_pool(self):
        for idx in xrange(settings.CHROME_USER_DATA_DIR_POOL_SIZE):
            get_chrome_resource()

    def test_can_get_lock(self):
        lock, path = get_chrome_resource()
        self.assertIsNotNone(lock)

    def test_when_no_resource_can_use_tmp(self):
        self._empty_lock_pool()
        lock, path = get_chrome_resource()
        self.assertIsNone(lock)
        self.assertTrue(os.path.exists(path))

    @mock.patch('time.time')
    @mock.patch('random.randint')
    def test_can_random_tmp(self, mock_randint, mock_time):
        self._empty_lock_pool()
        mock_randint.side_effect = [1, 2]
        mock_time.side_effect = [1, 2]
        mock_path = os.path.join('/tmp/', 'chrome_user_data_11')
        os.system('mkdir -p ' + mock_path)
        expected_path = os.path.join('/tmp/', 'chrome_user_data_22')
        os.system('rm -rf ' + expected_path)

        lock, path = get_chrome_resource()
        self.assertIsNone(lock)
        self.assertTrue(expected_path, path)
