from django import forms
from django.db import models

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet

import re

wagtail_resdigita_features=['h2', 'h3', 'h4', 'bold', 'italic', 'ol', 'ul', 'hr', 'link', 'document-link', 'image', 'embed', 'code', 'blockquote']

@register_snippet
class Author(models.Model):
    name = models.CharField(max_length=255)
    author_image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    panels = ["name", "author_image"]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Authors'

class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )
    
class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    authors = ParentalManyToManyField('blog.Author', blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel(["date", FieldPanel("authors", widget=forms.CheckboxSelectMultiple), "tags"], heading="Blog information"), "intro", "body", "gallery_images"]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["main_image"] = self.main_image()
        return context
    

class BlogPageGalleryImage(Orderable):
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = ["image", "caption"]


class BlogIndexPage(Page):
    decorative_title = RichTextField(
        blank=True,
        features=['bold'],
    )
    cta = models.CharField(max_length=128,blank=True)

    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + ["decorative_title", "intro", "cta"]


    def get_blog_pages(self):
        return self.get_children().specific().live().public().type(BlogPage).order_by('-first_published_at')

    def get_context(self, request):
        context = super().get_context(request)
        context["page"].decorative_title = re.sub(r'^<p[^>]*>(.*?)</p>$', r'\1', context["page"].decorative_title, flags=re.DOTALL)
        context['page'].blogpages = self.get_blog_pages()
        for blogpage in context['page'].blogpages.specific():
            blogpage.main_image = blogpage.main_image()
        return context




class BlogTagIndexPage(Page):

    def get_context(self, request):

        # Filter by tag
        tag = request.GET.get('tag')
        blogpages = BlogPage.objects.filter(tags__name=tag)
        # Update template context
        context = super().get_context(request)
        context['blogpages'] = blogpages
        if ("%s" % context['decorative_title']) == "":
            context['decorative_title'] = context['title']
        return context
