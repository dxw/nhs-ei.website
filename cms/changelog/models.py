from django.db import models

from datetime import datetime

from wagtail.admin.edit_handlers import FieldPanel


class ChangelogEntry(models.Model):
    change_date = models.DateTimeField(
        "When the changes were made", default=datetime.now
    )
    change_description = models.TextField("Description of the changes")

    panels = [
        FieldPanel("change_date"),
        FieldPanel("change_description"),
    ]

    class Meta:
        abstract = True
