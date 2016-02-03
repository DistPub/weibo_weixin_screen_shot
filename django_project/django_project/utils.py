import random
import os
import time

from PIL import Image
from django.conf import settings
from django.core.cache import cache


def generate_user_media_image_path(name=None, prefix=None, suffix='png'):
    """
    Generate empty file under media folder
    Return file path except media root, so the absolute path is settings.MEDIA_ROOT + RETURNS
    :param name: specified a file name
    :param prefix: file name prefix
    :param suffix: file name suffix
    :return: file path
    """
    if not name:
        name = str(int(time.time()))

    if prefix:
        name = prefix + '_' + name

    use_first_chance = False
    while True:
        if not use_first_chance:
            use_first_chance = True
            tmp_name = name + '.' + suffix
            file_path = os.path.join(settings.MEDIA_ROOT, tmp_name)
        else:
            tmp_name = name + str(random.randint(0, 999999)) + str(int(time.time())) + '.' + suffix
            file_path = os.path.join(settings.MEDIA_ROOT, tmp_name)

        if not os.path.exists(file_path):
            open(file_path, 'w').close()
            return tmp_name

def get_chrome_resource():
    """
    Return chrome resource lock and user data path
    If no resource just return a temp path
    """
    for idx, lock_name in enumerate(settings.CHROME_RESOURCE_LOCKS):
        lock = cache.lock(lock_name, expire=settings.CHROME_RESOURCE_LOCK_TIME)
        if lock.acquire(blocking=False):
            return lock, settings.CHROME_USER_DATA_DIR_POOL[idx]

    while True:
        tmp_name = 'chrome_user_data_' + str(random.randint(0, 999999)) + str(int(time.time()))
        tmp_path = os.path.join('/tmp/', tmp_name)
        if os.path.exists(tmp_path):
            continue

        os.mkdir(tmp_path)
        return None, tmp_path

def crop_image(file_path, start_x_pos, start_y_pos, width, height):
    """
    Crop image to specified size
    """
    bounding_box = (
        start_x_pos,
        start_y_pos,
        start_x_pos + width,
        start_y_pos + height
    )
    base_image = Image.open(file_path)
    cropped_image = base_image.crop(bounding_box)
    base_image = base_image.resize(cropped_image.size)
    base_image.paste(cropped_image)
    base_image.save(file_path)
