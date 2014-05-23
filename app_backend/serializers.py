from .models import BlogPage
from rest_framework import serializers
from wagtail.wagtailimages.models import Image


class BlogDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BlogPage
        fields = ('title', 'body')

# get the image url from related filed 'head_image'
class ImageField(serializers.RelatedField):
    def to_native(self, value):
        image = {'title' : value.title,
                'image_url' : value.get_rendition('fill-80x80').url
                }
                
        return image

class BlogListSerializer(serializers.ModelSerializer):
    head_image = ImageField()
    
    class Meta:
        model = BlogPage
        fields = ('title', 'head_image', 'body')
