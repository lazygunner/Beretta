from django.db import models
from django.conf import settings

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, PageChooserPanel
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from modelcluster.fields import ParentalKey
from django.utils.translation import ugettext_lazy as _


class LinkFields(models.Model):
    link_external = models.URLField("External link", blank=True)
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        related_name='+'
    )
    link_document = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        related_name='+'
    )

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_document:
            return self.link_document.url
        else:
            return self.link_external

    panels = [
        FieldPanel('link_external'),
        PageChooserPanel('link_page'),
        DocumentChooserPanel('link_document'),
    ]

    class Meta:
        abstract = True


class RelatedLink(LinkFields):
    title = models.CharField(max_length=255, help_text="Link title")

    panels = [
        FieldPanel('title'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    class Meta:
        abstract = True

class BlogIndexPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('app_backend.BlogIndexPage', related_name='related_links')

class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    indexed_fields = ('intro', )

    @property
    def blogs(self):
        # Get list of live blog pages that are descendants of this page
        blogs = BlogPage.objects.live().descendant_of(self)

        # Order by most recent date first
        blogs = blogs.order_by('-date')

        return blogs

    def get_context(self, request):
        # Get blogs
        blogs = self.blogs

        # Filter by tag
        tag = request.GET.get('tag')
        if tag:
            blogs = blogs.filter(tags__name=tag)

        # Pagination
        page = request.GET.get('page')
        paginator = Paginator(blogs, 10)  # Show 10 blogs per page
        try:
            blogs = paginator.page(page)
        except PageNotAnInteger:
            blogs = paginator.page(1)
        except EmptyPage:
            blogs = paginator.page(paginator.num_pages)

        # Update template context
        context = super(BlogIndexPage, self).get_context(request)
        context['blogs'] = blogs
        return context

BlogIndexPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('intro', classname="full"),
    InlinePanel(BlogIndexPage, 'related_links', label="Related links"),
]

class BlogPage(Page):
    body = RichTextField(verbose_name=_("body"))
    date = models.DateField(verbose_name=_("Post Date"))
    indexed_fields = ('body', )
    search_name = _("Blog Page")
    head_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='head_image'
    )
    class Meta:
        verbose_name = _('Blog Page')

    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

BlogPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('date'),
    ImageChooserPanel('head_image'),
    FieldPanel('body', classname="full"),
]

class Comment(models.Model):
    body = models.CharField(max_length=255, verbose_name=_('Comment Body'))
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False, related_name='owned_comment')
    date = models.DateField(verbose_name=_("Comment Date"))
    blog = models.ForeignKey(
        'app_backend.BlogPage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='comment'
    )
   
