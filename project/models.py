from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.search import index


class ProjectIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + ["intro"]

class ProjectPage(Page):
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + ["intro", "body"]