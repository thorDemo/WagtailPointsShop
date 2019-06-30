from django.db import models
from wagtail.documents.models import Document, AbstractDocument
# from wagtail.documents.wagtail_hooks import


class CustomDocument(AbstractDocument):
    # Custom field example:
    source = models.CharField(
        max_length=255,
        # This must be set to allow Wagtail to create a document instance
        # on upload.
        blank=True,
        null=True
    )

    admin_form_fields = Document.admin_form_fields + (
            # Add all custom fields names to make them appear in the form:
            # 'source',
        )
