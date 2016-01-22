import random

import os
import time

from django.conf import settings


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
