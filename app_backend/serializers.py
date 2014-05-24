from .models import BlogPage, Comment
from rest_framework import serializers
from wagtail.wagtailimages.models import Image
from django.contrib.auth.models import User


class BlogDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BlogPage
        fields = ('title', 'body')

# get the image url from related filed 'head_image'
class ImageField(serializers.RelatedField):
    def to_native(self, value):
        image = {'title' : value.title,
                'image_url' : value.get_rendition('fill-240x240').url
                }
                
        return image

class BlogListSerializer(serializers.ModelSerializer):
    head_image = ImageField()
    
    class Meta:
        model = BlogPage
        fields = ('id', 'title', 'head_image', 'desc', 'date')



class CommentSerializer(serializers.Serializer):
    pk = serializers.Field()
    owner = serializers.CharField()   
    body = serializers.CharField(max_length=255)
    blog = serializers.CharField()
    def restore_object(self, attrs, instance=None):
        if instance is not None:
            instance.body = attrs.get('body', instance.body)
            instance.blog = attrs.get('blog', instance.blog)
            return instance
        attrs['blog'] = BlogPage.objects.get(pk=attrs['blog'])
        attrs['owner'] = User.objects.all().first()
        return Comment(**attrs)

