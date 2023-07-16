from django.core.management.base import BaseCommand

from articles.models import Article


class Command(BaseCommand):
    """ Тестирует чтение данных из БД.
    """
    def add_arguments(self, parser):
        """ Аргументы не используются. """
        pass

    def handle(self, *args, **options):
        """ Печатает данные из БД. """
        articles_objects = Article.objects.all()
        quote = '\r\nСтатьи:'
        for art in articles_objects:
            quote += '\r\n\r\n' + f'{art.title} - {art.text}'
        self.stdout.write(f'{quote}\r\n\r\n')
        return
