import redis_lock
from django.core.management.base import BaseCommand
from django_redis import get_redis_connection


class Command(BaseCommand):
    help = "Init for django server"

    def handle(self, *args, **options):
        """
        Run init commmand for django server
        """
        self.refresh_lock()

    def refresh_lock(self):
        """
        Reset all lock for chrome resource
        """
        redis_lock.reset_all(get_redis_connection("default"))
