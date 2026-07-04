from django.db import models
from wagtail.images.models import AbstractImage, AbstractRendition
from wagtail.documents.models import AbstractDocument

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
