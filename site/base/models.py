from django.db import models
from django.contrib.auth.models import AbstractUser

# from modelcluster.fields import ParentalKey
# from wagtail_advanced_form_builder.models.abstract_advanced_form_field import AbstractAdvancedFormField
from wagtail.images.models import AbstractImage, AbstractRendition
from wagtail.documents.models import AbstractDocument

# from .pages import *

# class StandardPageFormBuilderFormField(AbstractAdvancedFormField):
#     page = ParentalKey("base.StandardPage", on_delete=models.CASCADE, related_name="form_fields")

class User(AbstractUser):
    pass


class CustomImage(AbstractImage):
    pass


class CustomImageRendition(AbstractRendition):
    image = models.ForeignKey(CustomImage, on_delete=models.CASCADE, related_name='renditions')

    class Meta:
        unique_together = (
            ('image', 'filter_spec', 'focal_point_key'),
        )


class CustomDocument(AbstractDocument):
    pass
