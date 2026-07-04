# TODO: There may be somewhere better to put this code

from django.db import models

from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField
# TODO: RemovedInWagtail50Warning: `wagtail.contrib.settings.models.BaseSetting` is obsolete and should be replaced by `wagtail.contrib.settings.models.BaseSiteSetting` or `wagtail.contrib.settings.models.BaseGenericSetting`
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting

from wagtail import blocks
from wagtail.fields import StreamField

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from wagtail_link_block.blocks import LinkBlock

import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)
from decouple import AutoConfig

config = AutoConfig(search_path=BASE_DIR)

PRODUCTION = config("PRODUCTION", default=False, cast=bool)

MINIMAL_RICHTEXT_FEATURES = ["bold", "br"]

if PRODUCTION:
    # https://sentry.io/organizations/obvious-agency/projects/obvs-demo-production/getting-started/python-django/
    sentry_sdk.init(
        dsn="https://3f2092650513444d894a89c9da2dee3c@o1398467.ingest.sentry.io/6724881",
        integrations=[
            DjangoIntegration(),
        ],

        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0,  # TODO: adjust this to reduce the amount of performance data tracked

        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True
    )


@register_setting
class SiteSettings(BaseGenericSetting):
    seo_site_description = models.CharField(
        null=True,
        max_length=160,
        help_text="Used by search engines when there is not a specific description for the page. Should be between 50 and 160 characters (any longer and the text may be truncated by many search engines."
    )

    panels = [
        FieldPanel("seo_site_description"),
    ]


@register_setting
class ContactSettings(BaseGenericSetting):
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(null=True, blank=True, max_length=50)
    address = RichTextField(null=True, blank=True)

    panels = [
        FieldPanel("email"),
        FieldPanel("phone"),
        FieldPanel("address"),
    ]


@register_setting
class SocialMediaSettings(BaseGenericSetting):
    show_social_media = models.BooleanField(default=False,
                                            help_text="Enable this to show social media icons in the footer.")
    linkedin = models.URLField(null=True, blank=True, help_text="Enter the full URL of the page.")
    facebook = models.URLField(null=True, blank=True, help_text="Enter the full URL of the page.")
    instagram = models.URLField(null=True, blank=True, help_text="Enter the full URL of the page.")
    twitter = models.URLField(null=True, blank=True, help_text="Enter the full URL of the page.")
    youtube = models.URLField(null=True, blank=True, help_text="Enter the full URL of the page.")

    panels = [
        FieldPanel("show_social_media"),
        FieldPanel("linkedin"),
        FieldPanel("facebook"),
        FieldPanel("instagram"),
        FieldPanel("twitter"),
        FieldPanel("youtube"),
    ]


@register_setting
class ImageSettings(BaseGenericSetting):
    navbar_logo = models.ForeignKey(
        "base.CustomImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    default_article_image = models.ForeignKey(
        "base.CustomImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        FieldPanel("navbar_logo"),
        FieldPanel("default_article_image"),
    ]


# Nav Settings and Blocks
# todo: use CustomLinkBlock by default
class CustomLinkBlock(blocks.StructBlock):
    text = blocks.CharBlock(required=True)
    link = LinkBlock(required=True)
    section_id = blocks.CharBlock(required=False,
                                  help_text="Optional: You can add the name or ID of section which should be scrolled to (must match a section name used by the Section Identifier Block).")

    def get_api_representation(self, value, context=None):
        link_url = ""
        if value["page"]:
            link_url = value["page"].get_url()
        if value["file"]:
            link_url = value["file"].file.url
        if value["custom_url"]:
            link_url = value["custom_url"]
        if value:
            return {
                "link_to": value["link_to"],
                "page": value["page"].id if value["page"] else None,
                "file": value["file"].id if value["file"] else None,
                "custom_url": value["custom_url"],
                "new_window": value["new_window"],
                "link_url": link_url,
            }

    class Meta:
        template = "includes/navigation/menu_row.html"


class NavigationStreamBlock(blocks.StreamBlock):
    link = CustomLinkBlock()

    class Meta:
        label = "Links"
        classname = "collapsed collapsible",


@register_setting
class NavigationSettings(BaseGenericSetting):
    navbar_links = StreamField(
        NavigationStreamBlock(),
        blank=True,
        use_json_field=True,
    )

    show_search_in_nav = models.BooleanField(default=False, help_text="Add the search page to the list of nav items")

    # # Only for simple (1 column) footers:
    # small_footer_links = StreamField(
    #     NavigationStreamBlock(),
    #     default="",
    #     use_json_field=True,
    # )

    # For large (3 column) footers:
    footer_column_1_heading = models.CharField(blank=True, null=True, max_length=40)
    footer_column_1 = StreamField(
        NavigationStreamBlock(),
        default="",
        blank=True,
        use_json_field=True,
    )

    footer_column_2_heading = models.CharField(blank=True, null=True, max_length=40)
    footer_column_2 = StreamField(
        NavigationStreamBlock(),
        default="",
        blank=True,
        use_json_field=True,
    )
    footer_column_3_heading = models.CharField(blank=True, null=True, max_length=40)
    footer_column_3 = StreamField(
        NavigationStreamBlock(),
        default="",
        blank=True,
        use_json_field=True,
    )

    # Update after setup: comment out either the footer_links or the multi column footer links (depending on whether you're using the small or large footer), and make sure the correct template is used.
    panels = [
        FieldPanel("navbar_links", classname="collapsed collapsible"),
        FieldPanel("show_search_in_nav"),
        MultiFieldPanel(
            [
                FieldPanel("footer_column_1_heading"),
                FieldPanel("footer_column_1"),
                FieldPanel("footer_column_2_heading"),
                FieldPanel("footer_column_2"),
                FieldPanel("footer_column_3_heading"),
                FieldPanel("footer_column_3"),
            ],
            heading="Multi Column Footer Links",
            classname="collapsible collapsed"
        )
    ]
