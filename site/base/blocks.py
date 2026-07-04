from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock

from wagtail_link_block.blocks import LinkBlock
from wagtail_advanced_form_builder.blocks import InlineFormBlock


MINIMAL_RICHTEXT_FEATURES = ["bold", "br"]
DEFAULT_RICHTEXT_FEATURES = ["h2", "h3", "h4", "bold", "ol", "ul", "link", "document-link", "image", "br"]
RICHTEXT_HELP_TEXT = """
    Highlight text to show the toolbar. You can also pin the toolbar with the pin icon. 
    (Pro tip: '/' is a shortcut to bring up the toolbar with additional options).
"""


# BUTTONS
class ButtonBlock(blocks.StructBlock):
    text = blocks.CharBlock(required=True)
    style = blocks.ChoiceBlock(
        choices=[("primary", "Primary"), ("secondary", "Secondary")],
        default="primary",
        blank=True,
    )
    link = LinkBlock()

    class Meta:
        icon = "link"


class ButtonsBlock(blocks.StructBlock):
    items = blocks.ListBlock(
        ButtonBlock(required=False, blank=True),
        blank=True,
    )

    class Meta:
        label = "Button(s)"
        icon = "link"
        template = "blocks/buttons.html"


# CTA
class CTABannerBlock(blocks.StructBlock):
    image = ImageChooserBlock(
        required=True,
        help_text="A banner which is 50% width on desktop and full width on mobile (use photos which are at least 960x600px).",
    )
    image_side = blocks.ChoiceBlock(choices=[
        ('left', 'Left'),
        ('right', 'Right'),
    ])
    title = blocks.CharBlock(required=False)
    text = blocks.RichTextBlock(
        template="blocks/richtext_block.html",
        features=MINIMAL_RICHTEXT_FEATURES,
        required=False,
        help_text=RICHTEXT_HELP_TEXT,
    )
    buttons = ButtonsBlock(required=False, blank=True)

    class Meta:
        label = "Call to Action"
        icon="pick"
        template = "blocks/cta_banner_block.html"


# IMAGE BLOCKS
class ImageBannerBlock(blocks.StructBlock):
    image = ImageChooserBlock(
        required=True,
        help_text="A full width banner. Should be a photo which is large, landscape and high resolution (use photos which are at least 1920x640px).",
    )

    class Meta:
        label = "Image Banner"
        icon="image"
        template = "blocks/image_banner_block.html"


class BaseImageBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=True)
    text = blocks.RichTextBlock(
        template="blocks/richtext_block.html",
        features=MINIMAL_RICHTEXT_FEATURES,
        required=False,
        help_text=RICHTEXT_HELP_TEXT,
    )


class ImageBlock(BaseImageBlock):
    size = blocks.ChoiceBlock(choices=[('thumbnail', 'Thumbnail'), ('full', 'Large'),])

    class Meta:
        label = "Single Image"
        icon="image"
        template = "blocks/image_block.html"


class ImageGalleryBlock(blocks.StructBlock):
    enable_modal = blocks.BooleanBlock(default=False, required=False)
    items = blocks.ListBlock(BaseImageBlock(icon="form"))

    class Meta:
        label = "Image Gallery"
        help_text = "A gallery of images to be displayed as a group."
        icon="image"
        template = "blocks/image_gallery_block.html"


# CARDS and GRIDS
class CardItemBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=False)
    text = blocks.RichTextBlock(
        template="blocks/richtext_block.html",
        features=DEFAULT_RICHTEXT_FEATURES,
        help_text=RICHTEXT_HELP_TEXT,
    )

    class Meta:
        icon = "form"


class CardListBlock(blocks.StructBlock):
    items = blocks.ListBlock(CardItemBlock())

    class Meta:
        label = "Card List"
        help_text = "A group of cards, each containing some text and/or an image. Usually used to display information which isn't clickable."
        icon="table"
        template = "blocks/card_list_block.html"


class CardLinkBlock(blocks.StructBlock):
    link = LinkBlock()
    image = ImageChooserBlock(required=True)
    text = blocks.RichTextBlock(
        template="blocks/richtext_block.html",
        features=["h2", "bold", "br"],
        required=False,
        help_text=RICHTEXT_HELP_TEXT,
    )


class CardLinkListBlock(blocks.StructBlock):
    items = blocks.ListBlock(CardLinkBlock(icon="form"))
    view_more = LinkBlock(required=False, blank=True, label="View more link", help_text="If there are more items to view, provide a link here to the page where they can be viewed.")

    class Meta:
        label = "Card Links"
        icon="table"
        help_text = "A group of clickable cards, each containing some text and/or an image. Often used when linking to articles."
        template = "blocks/card_link_list_block.html"


# ACCORDION
class AccordionItemBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True)
    content = blocks.RichTextBlock(
        template="blocks/richtext_block.html",
        help_text=RICHTEXT_HELP_TEXT,
    )

    class Meta:
        label = "Accordion Item"
        icon = "form"


class AccordionListBlock(blocks.StructBlock):
    accordion_items = blocks.ListBlock(AccordionItemBlock())

    class Meta:
        label = "Accordion Block"
        icon="list-ul"
        template = "blocks/accordion_block.html"


# MISC
class VideoBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True)
    url = blocks.CharBlock(
        required=True,
        help_text="A link to a video on YouTube or Vimeo (eg https://www.youtube.com/embed/YE7VzlLtp-4).",
    )

    class Meta:
        label = "Video"
        template = "blocks/video_block.html"


class VideoEmbedBlock(blocks.StaticBlock):
    video = EmbedBlock(
        help_text="Insert an embed URL e.g https://player.vimeo.com/video/70461160",
        template="blocks/embed_block.html",
    )

    class Meta:
        label = "Video Embed"


class QuoteBlock(blocks.StructBlock):
    quote = blocks.CharBlock(required=True)
    name = blocks.CharBlock(required=False)
    title = blocks.CharBlock(required=False)

    class Meta:
        label = "Quote"
        icon="openquote"
        template = "blocks/quote_block.html"


class TestimonialBlock(QuoteBlock):
    photo = ImageChooserBlock(required=True)


class TestimonialListBlock(blocks.StructBlock):
    testimonials = blocks.ListBlock(TestimonialBlock(icon="form"))
    class Meta:
        label = "Testimonials"
        help_text = "Adding three testimonials is recommended"
        icon="openquote"
        template = "blocks/testimonials_block.html"


class SectionIdentifier(blocks.StructBlock):
    section_id = blocks.CharBlock(required=True, help_text="Create a name for a section. This can optionally be used by links to automatically scroll to this section of the page.")

    class Meta:
        template = "blocks/section_identifier.html"


class HorizontalRuleBlock(blocks.StaticBlock):
    class Meta:
        label = "Horizontal Line"
        icon="horizontalrule"
        template = "blocks/horizontal_rule_block.html"


class VerticalGapBlock(blocks.StaticBlock):
    class Meta:
        label = "Vertical Gap"
        icon="arrows-up-down"
        template = "blocks/vertical_gap_block.html"


class FormFromPageBlock(blocks.StructBlock):
    page_with_form = blocks.PageChooserBlock()

    class Meta:
        template = "blocks/form_from_other_page.html"


# TWO COLUMN BLOCK
class SimpleGridItemStreamBlock(blocks.StreamBlock):
    text = blocks.RichTextBlock(
        template="blocks/grid_block_richtext.html",
        help_text=RICHTEXT_HELP_TEXT,
    )

    image = ImageChooserBlock(
        # help_text="Use photos which are at least 960x600px",
        template="blocks/grid_block_image.html"
    )

    class Meta:
        icon = "form"
        label = "Column"


class SimpleGridBlock(blocks.StructBlock):
    style = blocks.ChoiceBlock(
        choices=[("50-50", "50/50"), ("70-30", "70/30"), ("30-70", "30/70")],
        default="50-50",
        label="Columns per row",
        blank=True,
    )

    content = blocks.ListBlock(SimpleGridItemStreamBlock())

    class Meta:
        label="Two Column Block"
        icon="table"
        template = "blocks/simple_grid_block.html"


# GRID BUILDER BLOCK
class BaseSimpleStreamBlock(blocks.StreamBlock):
    text = blocks.RichTextBlock(
        template="blocks/grid_block_richtext.html",
        features=["h2", "h3", "h4", "bold", "ol", "ul", "link", "document-link", "br"],
        help_text=RICHTEXT_HELP_TEXT,
    )

    image = ImageChooserBlock(
        # help_text="Use photos which are at least 960x600px",
        template="blocks/grid_block_image.html"
    )


class GridBlockItem(blocks.StructBlock):
    # # uncomment only if used on a site with items that span multiple columns
    # columns = blocks.ChoiceBlock(
    #     choices=[("one", "One"), ("two", "Two"), ("three", "Three"), ("four", "Four")],
    #     default="one",
    #     label="Columns spanned by item",
    #     help_text="In most cases this will be one",
    #     blank=True,
    # )

    content = BaseSimpleStreamBlock(required=False)

    class Meta:
        icon="form"


class GridBlock(blocks.StructBlock):
    columns = blocks.ChoiceBlock(
        choices=[("two", "Two"), ("three", "Three"), ("four", "Four")],
        default="two",
        label="Columns per row",
        blank=True,
    )

    items = blocks.ListBlock(GridBlockItem())

    class Meta:
        label = "Multi-column Block"
        help_text = "Select the number of columns each row should have, then create blocks for the grid (override the default width of the columns if needed)"
        icon="table"
        template = "blocks/grid_block.html"


# BANNER BLOCKS
class HeroBannerBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True)
    subtitle = blocks.CharBlock(required=False)
    background_image = ImageChooserBlock(required=True)
    buttons = ButtonsBlock()

    class Meta:
        label = "Hero Banner"
        icon="pick"
        template = "blocks/hero_banner_block.html"


class SimpleBannerBlock(blocks.StructBlock):
    background_image = ImageChooserBlock(required=False)

    class Meta:
        label = "Simple Banner"
        icon="image"
        help_text="A simple banner using the title and subtitle with an optional image."
        template = "blocks/simple_banner_block.html"


class CustomRichTextBlock(blocks.StructBlock):
        text = blocks.RichTextBlock(
        template="blocks/richtext_block.html",
        features=DEFAULT_RICHTEXT_FEATURES,
        help_text=RICHTEXT_HELP_TEXT,
    )


# STREAMBLOCKS
class BaseStreamBlock(blocks.StreamBlock):
    text = blocks.RichTextBlock(
        template="blocks/richtext_block.html",
        features=DEFAULT_RICHTEXT_FEATURES,
        help_text=RICHTEXT_HELP_TEXT,
    )
    buttons_block = ButtonsBlock()
    cta_banner_block = CTABannerBlock()
    simple_grid_block = SimpleGridBlock()
    grid_block = GridBlock()
    card_list_block = CardListBlock()
    card_link_list_block = CardLinkListBlock()
    image_block = ImageBlock()
    image_gallery_block = ImageGalleryBlock()
    # video_block = VideoBlock() # Note: Video Embed Block is usually used as it's better for SEO, but this can be used if more customization is needed
    video_embed_block = EmbedBlock(
        help_text="Insert an embed URL e.g https://player.vimeo.com/video/70461160",
        template="blocks/video_embed_block.html",
    )
    quote_block = QuoteBlock()
    testimonials_block = TestimonialListBlock()
    accordion_block = AccordionListBlock()
    horizontal_rule = HorizontalRuleBlock()
    vertical_gap = VerticalGapBlock()
    section_identifier = SectionIdentifier()
    contact_form = InlineFormBlock(required=False, help_text="Edit this form on the email form page.")
    form_from_other_page = FormFromPageBlock()


class HeroBannerStreamBlock(blocks.StreamBlock):
    simple_banner = SimpleBannerBlock(required=True)
    hero_banner = HeroBannerBlock(required=True)
