from django.db import models

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, PageChooserPanel
from modelcluster.fields import ParentalKey
from django.utils.translation import ugettext_lazy as _

class BlogPage(Page):
    body = RichTextField(verbose_name=_("body"))
    date = models.DateField(_("Post Date"))
    indexed_fields = ('body', )
    search_name = _("Blog Page")

    class Meta:
        verbose_name = _('Blog Page')

    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

BlogPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('date'),
    FieldPanel('body', classname="full"),
]

