# from django.db import models
from django.core.paginator import Paginator

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
        articles = ArticlePage.objects.live().public().reverse()
        paginated_articles = Paginator(articles, 10)

        context["paginated_articles"] = paginated_articles
        context["articles"] = list( paginated_articles.page(page_num) )
        context["current_page"] = page_num

        return context

    def get_template(self, request, *args, **kwargs):
        return "pages/article_index_page.html"
