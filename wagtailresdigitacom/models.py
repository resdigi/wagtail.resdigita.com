from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel


class PageHome(Page):
    content = RichTextField(
        blank=True,
        features=['h2', 'h3', 'h4', 'bold', 'italic', 'monospace', 'ol', 'ul', 'hr', 'link', 'document-link', 'image', 'embed', 'code', 'blockquote']
    )

    content_panels = (
        FieldPanel("title", classname="full title"),
        FieldPanel("content"),
    )
