from django.db import models

class PageMixin(models.Model):
    subtitle = models.CharField(max_length=255, null=True, blank=True)

    summary_text = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="A summary of the article or page to be used in cards which link to the article (not the article itself)")

    summary_image = models.ForeignKey(
        "base.CustomImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    def get_summary_image(self):
        if self.summary_image:
            return self.summary_image
        elif self.feature_image:
            return self.feature_image
        else:
            return None

    class Meta:
        abstract = True