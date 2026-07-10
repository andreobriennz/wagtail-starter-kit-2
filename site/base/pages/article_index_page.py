# from django.db import models
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from wagtail.admin.panels import FieldPanel
from wagtail.models import Page

from base.mixins import PageMixin
from base.pages.article_page import *


class ArticleIndexPage(Page, PageMixin):
    subpage_types = ["base.ArticlePage"]

    max_count = 1

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        page_num = request.GET.get('page', 1)
        articles = ArticlePage.objects.live().public().order_by('-first_published_at')
        paginated_articles = Paginator(articles, 10)

        try:
            articles_page = paginated_articles.page(page_num)
        except (PageNotAnInteger, EmptyPage):
            articles_page = paginated_articles.page(1)

        context["paginated_articles"] = paginated_articles
        context["articles"] = list(articles_page)
        context["current_page"] = articles_page.number

        return context

    def get_template(self, request, *args, **kwargs):
        return "pages/article_index_page.html"
