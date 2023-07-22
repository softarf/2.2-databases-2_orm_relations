from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from articles.models import Article, Rubric, ArticleRubric


class ArticleRubricInlineFormset(BaseInlineFormSet):
    """ Класс для обработки списка однотипных форм. """

    def clean(self):
        """ Реализует проверку на наличие одной и только одной основной рубрики. """
        error_text = "Укажите основную рубрику"
        for form in self.forms:
            # В form.cleaned_data будет словарь с данными
            # каждой отдельной формы, которые вы можете проверить
            if form.cleaned_data and not form.cleaned_data['DELETE'] and form.cleaned_data["is_main"]:
                # Рассматривает только заполненные формы, и непомеченные на удаление,
                if error_text:
                    error_text = ""
                else:
                    error_text = "Основной может быть только одна рубрика"
                    break
        if error_text:
            # вызовом исключения ValidationError можно указать админке о наличие ошибки
            # таким образом объект не будет сохранен,
            # а пользователю выведется соответствующее сообщение об ошибке
            raise ValidationError(error_text)    # 'Тут всегда ошибка'
        return super().clean()  # вызываем базовый код переопределяемого метода


class ArticleRubricInLine(admin.TabularInline):
    """ Таблица, встраиваемая в отображение другой таблицы. """
    model = ArticleRubric
    extra = 1
    formset = ArticleRubricInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'published_at')
    list_display_links = ('title', 'text')
    search_fields = ('title', 'text')
    inlines = [ArticleRubricInLine, ]    # Добавляем встраиваемые данные (таблицу ArticleRubric)


# admin.site.register(Article, ArticleAdmin)    # Можно и так, вместо декоратора.


@admin.register(Rubric)
class RubricAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_display_links = ('name', )
    search_fields = ('name', )


# @admin.register(ArticleRubric)
# class ArticleRubricAdmin(admin.ModelAdmin):
#     list_display = ('article', 'rubric', 'is_main')
#     list_display_links = ('article', 'rubric')
#     search_fields = ('article', 'rubric')
