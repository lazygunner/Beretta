from .models import BlogPage
from rest_framework import serializers


class BlogDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BlogPage
        fields = ('title', 'body')
