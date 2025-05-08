from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.search import index
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from modelcluster.fields import ParentalKey, ParentalManyToManyField
import re
# from resdigita.models import wagtail_resdigita_features


wagtail_resdigita_features=['h2', 'h3', 'h4', 'bold', 'italic', 'ol', 'ul', 'hr', 'link', 'document-link', 'image', 'embed', 'code', 'blockquote']

class ProjectPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'ProjectPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class ProjectPage(Page):
    intro = models.CharField(max_length=250)
    body = RichTextField(
        blank=True,
        features=wagtail_resdigita_features,
    )
    tags = ClusterTaggableManager(through=ProjectPageTag, blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        "tags", 
        "intro", 
        "image", 
        "body"
    ]

class ProjectIndexPage(Page):
    intro = RichTextField(blank=True)
    decorative_title = RichTextField(
        blank=True,
        features=['bold'],
    )
    cta = models.CharField(max_length=128, blank=True)

    content_panels = Page.content_panels + [
        'decorative_title', "intro", 'cta']

    def get_project_pages(self):
        return self.get_children().specific().live().public().type(ProjectPage)


    def get_context(self, request):
        context = super().get_context(request)
        context["page"].decorative_title = re.sub(r'^<p[^>]*>(.*?)</p>$', r'\1', context["page"].decorative_title, flags=re.DOTALL)
        context['page'].projectpages = self.get_project_pages()

        return context

class ProjectTagIndexPage(Page):

    def get_context(self, request):

        # Filter by tag
        tag = request.GET.get('tag')
        projectpages = ProjectPage.objects.filter(tags__name=tag)

        # Update template context
        context = super().get_context(request)
        context['projectpages'] = projectpages
        return context