from django.db import models


class Article(models.Model):

    title = models.CharField(max_length=256, verbose_name='Название')
    text = models.TextField(null=True, blank=True, verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение',)
    #
    objects = models.Manager()

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-published_at', ]

    def __str__(self):
        return self.title


class Rubric(models.Model):
    # Культура Город Здоровье Наука Космос Международные отношения
    name = models.CharField(max_length=100, verbose_name='Название')
    articles = models.ManyToManyField(Article, related_name='rubrics', through='ArticleRubric')
    #
    objects = models.Manager()

    class Meta:
        verbose_name = 'Рубрика'
        verbose_name_plural = 'Рубрики'
        ordering = ['name', ]

    def __str__(self):
        return self.name


class ArticleRubric(models.Model):

    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья', related_name='relations')
    rubric = models.ForeignKey(Rubric, on_delete=models.CASCADE, verbose_name='Рубрика', related_name='relations')
    is_main = models.BooleanField(null=True, blank=True, verbose_name='Основная')

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Тематики статьи'
        ordering = ['id', ]

    def __str__(self):
        return f"article_id: {self.article},  rubric_id: {self.rubric}"
