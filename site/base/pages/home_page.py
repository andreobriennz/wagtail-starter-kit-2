from django.db import models

from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page

from base.blocks import BaseStreamBlock, HeroBannerStreamBlock
from base.mixins import PageMixin


class HomePage(Page, PageMixin):
    hero_banner = StreamField(
        HeroBannerStreamBlock(min=1, max=1, required=False),
        verbose_name="Banner",
        blank=True,
        max_num=1,
        use_json_field=True,
    )

    content = StreamField(
        BaseStreamBlock(required=False),
        verbose_name="Main Content",
        blank=True,
        use_json_field=True,
    )
    
    keywords = models.CharField(max_length=255, null=True, blank=True, help_text="A comma separated list of keywords.")

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        FieldPanel("summary_image"),
        FieldPanel("hero_banner"),
        FieldPanel("content"),
    ]
    
    promote_panels = Page.promote_panels + [
        FieldPanel("keywords"),
    ]

    max_count = 1

    subpage_types = ['base.StandardPage', 'base.ArticleIndexPage']

    def get_template(self, request, *args, **kwargs):
        return "pages/standard_page.html"

    @property
    def structured_data(self):
        url = self.full_url
        data = {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "url": url,
            "@id": url,
            "datePublished": self.first_published_at.strftime("%Y-%m-%d"),
            "dateModified": self.last_published_at.strftime("%Y-%m-%d"),
        }
        if self.summary_image:
            data["image"] = self.summary_image.get_rendition("fill-750x750").full_url
        if self.keywords:
            data["keywords"] = self.keywords

        return data