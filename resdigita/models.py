from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel

from blog.models import BlogIndexPage, BlogPage
from project.models import ProjectIndexPage, ProjectPage
# from base.models import NavigationSettings
# from wagtail.contrib.settings.models import BaseGenericSetting
# from resdigita.services import get_blog_posts

wagtail_resdigita_features=['h2', 'h3', 'h4', 'bold', 'italic', 'ol', 'ul', 'hr', 'link', 'document-link', 'image', 'embed', 'code', 'blockquote']

class PageHome(Page):
    intro = RichTextField(blank=True, max_length=255,features=['bold', 'italic','link','document-link'])

    content = RichTextField(
        blank=True,
        features=wagtail_resdigita_features,
    )

    hero_cta = models.CharField(
        blank=True,
        verbose_name="Hero CTA",
        max_length=255,
        help_text="Text to display on Call to Action",
    )

    hero_cta_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Hero CTA link",
        help_text="Choose a page to link to for the Call to Action",
    )

    content_panels = (
        FieldPanel("title", classname="full title"),
        FieldPanel("intro"),
        FieldPanel("content"),
        FieldPanel("hero_cta"),
        FieldPanel("hero_cta_link"),
    )

    def get_context(self, request):

        context = super().get_context(request)

        context['blogindexpages'] = self.get_children().specific().live().type(BlogIndexPage)
        context['projectindexpages'] = self.get_children().specific().live().type(ProjectIndexPage)
        for item in context['blogindexpages']:
            item.blogpages = item.get_blog_pages()
        for item in context['projectindexpages']:
            item.projectpages = item.get_children().live().type(ProjectPage)
        return context