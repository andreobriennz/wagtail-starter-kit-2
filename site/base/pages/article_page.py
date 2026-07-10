# from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.search import index

from base.mixins import PageMixin
from base.blocks import BaseStreamBlock

class ArticlePage(Page, PageMixin):
    content = StreamField(
        BaseStreamBlock(required=False),
        verbose_name="Main Content",
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("subtitle", classname="full"),
        FieldPanel("summary_text"),
        FieldPanel("summary_image"),
        FieldPanel("content"),
    ]

    subpage_types = []

    parent_page_types = ["base.ArticleIndexPage"]

    search_fields = Page.search_fields + [
        index.SearchField("title", partial_match=True, boost=4),
        index.SearchField("subtitle", partial_match=True, boost=2),
        index.SearchField("summary_text", partial_match=True, boost=2),
        index.SearchField("content"),
        index.SearchField("seo_title"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["display_breadcrumbs"] = True
        return context

    def get_template(self, request, *args, **kwargs):
        return "pages/standard_page.html"

    @property
    def structured_data(self):
        url = self.full_url
        data = {
            "@type": "BlogPosting",
            "headline": self.title,
            # Can be Article, NewsArticle or BlogPosting: https://developers.google.com/search/docs/advanced/structured-data/article
            # "author": { "@type": "BlogPosting", "name": self.author },
            "datePublished": self.first_published_at.strftime("%Y-%m-%d"),
            "dateModified": self.last_published_at.strftime("%Y-%m-%d"),
            "url": url,
        }
        if self.summary_image:
            data["image"] = self.summary_image.get_rendition("fill-750x750").full_url

        return data