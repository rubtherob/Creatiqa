from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = u'Запуск с созданием проекта'

    def handle(self, *args, **kwargs):
        try:
            User.objects.create_superuser(email='rubtherobsss@gmail.com', password='1')
        except:
            pass