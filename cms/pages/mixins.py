from django.db import models
from wagtail.admin.edit_handlers import (
    FieldPanel,
)


class MetadataMixin(models.Model):
    class Meta:
        abstract = True

    md_owner = models.TextField("Content Owner", blank=True)
    md_description = models.TextField("Description of content", blank=True)
    md_pac_reference = models.TextField("PAC Reference", blank=True)

    panels = [
        FieldPanel("md_owner"),
        FieldPanel("md_description"),
        FieldPanel("md_pac_reference"),
    ]
