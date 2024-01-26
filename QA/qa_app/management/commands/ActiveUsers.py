from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Показывает всех активных пользователей'

    def handle(self, *args, **options):
        active_users = User.objects.filter(is_active=True)

        self.stdout.write(self.style.SUCCESS('Active Users:'))
        for user in active_users:
            self.stdout.write(self.style.SUCCESS(f'- {user.username}'))