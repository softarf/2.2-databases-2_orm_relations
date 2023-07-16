import os
import json

from django.core.management.base import BaseCommand
from articles.models import Article


class Command(BaseCommand):
    """ Переносит данные из json-файла в модель (таблицу БД) Article.
    """
    def add_arguments(self, parser):
        """ Получает имя json-файла с данными для загрузки.
            По умолчанию - 'articles.json'. """
        parser.add_argument(
            'file_name',
            action='store',
            nargs='?',
            default='articles.json',
            help='Название файла для считывания данных'
        )

    def handle(self, *args, **options):
        """ Переносит данные из json-файла в модель (таблицу БД) Article. """
        input_file = options['file_name']
        if not os.path.exists(input_file):
            self.stdout.write(f"Файл с данными не найден\n{input_file}")
            return
        with open(input_file, 'rt', encoding='utf-8') as json_file:
            json_data = json.load(json_file)

        for record in json_data:
            if record['model'] == 'articles.article':
                # Переносит только те данные, которых нет в базе.
                art, created = Article.objects.get_or_create(
                                                    title=record['fields']['title'],
                                                    text=record['fields']['text'],
                                                    published_at=record['fields']['published_at'],
                                                    image=record['fields']['image'],
                )
                message = f"""\nСтатья: "{record['fields']['title']}"\n"""
                self.stdout.write(message + ("успешно" if created else "Пропущена"))    # Для теста.
            else:
                self.stdout.write(f"Неизвестная запись данных: {record['model']}")
        self.stdout.write("Перенос данных завершён.")    # Для теста.
        return
