from django.db import models

from wagtail.admin.panels import FieldPanel
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.search import index
from wagtail.contrib.forms.panels import FormSubmissionsPanel
from wagtail.admin.panels import ObjectList, TabbedInterface

from wagtail_advanced_form_builder.models.abstract_advanced_email_form import AbstractAdvancedEmailForm
from wagtail.models import Page

from base.mixins import PageMixin
from base.blocks import BaseStreamBlock, HeroBannerStreamBlock
# from base.models import StandardPageFormBuilderFormField




from modelcluster.fields import ParentalKey
from wagtail_advanced_form_builder.models.abstract_advanced_form_field import AbstractAdvancedFormField
class StandardPageFormBuilderFormField(AbstractAdvancedFormField):
    page = ParentalKey(
        "base.StandardPage", on_delete=models.CASCADE, related_name="form_fields"
    )


class StandardPage(AbstractAdvancedEmailForm, Page, PageMixin):
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

    form_field = StandardPageFormBuilderFormField

    content_panels = Page.content_panels + [
        FieldPanel("subtitle", classname="full"),
        FieldPanel("summary_image"),
        FieldPanel("hero_banner"),
        FieldPanel("content"),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Content"),
            ObjectList(
                [FormSubmissionsPanel(heading="Submissions")]
                + AbstractAdvancedEmailForm.content_panels,
                heading="Form",
            ),
            ObjectList(Page.promote_panels, heading="Promote"),
            ObjectList(
                Page.settings_panels, heading="Settings", classname="settings"
            ),
        ]
    )

    search_fields = Page.search_fields + [
        index.SearchField("title", partial_match=True, boost=4),
        index.SearchField("subtitle", partial_match=True, boost=2),
        index.SearchField("content"),
        index.SearchField("seo_title"),
    ]

    def get_template(self, request, *args, **kwargs):
        return "pages/standard_page.html"

    promote_panels = Page.promote_panels + [
        FieldPanel("keywords"),
    ]

    @property
    def structured_data(self):
        url = self.full_url
        data = {
            "@context": "https://schema.org",
            "@type": "WebPage",
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