from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel

from blog.models import BlogPage
from project.models import ProjectPage
# from base.models import NavigationSettings

# from wagtail.contrib.settings.models import BaseGenericSetting




class PageHome(Page):
    content = RichTextField(
        blank=True,
        max_length=255,
        help_text="Write an introduction for the site",
        features=['h2', 'h3', 'h4', 'bold', 'italic', 'ol', 'ul', 'hr', 'link', 'document-link', 'image', 'embed', 'code', 'blockquote']
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
        FieldPanel("content"),
        FieldPanel("hero_cta"),
        FieldPanel("hero_cta_link"),
    )

    def get_context(self, request):

        context = super().get_context(request)

        blogpages = BlogPage.objects.live().order_by('-first_published_at')
        projectpages = ProjectPage.objects.live()
        # navset = NavigationSettings.load(request_or_site=request)

        # Update template context
        
        context['blogpages'] = blogpages
        context['projectpages'] = projectpages
        return context