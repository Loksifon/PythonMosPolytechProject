from django.core.management.base import BaseCommand

class Command(BaseCommand):
	help = 'Это команда показывает разработчика проекта'
	def handle(self, *args, **options):
		self.stdout.write('Привет, Этот проект написал Корнелюк Владислав Андреевич, группа 221-323')