from django.shortcuts import render

from articles.models import Article


def articles_list(request):
    template = 'articles/news.html'
    ordering = '-published_at'
    article_list = Article.objects.order_by(ordering)
    context = {'object_list': article_list}
    return render(request, template, context)
