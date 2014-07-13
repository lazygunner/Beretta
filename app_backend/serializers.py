from .models import BlogPage, Comment, Headphones
from rest_framework import serializers
from rest_framework.authtoken.models import Token
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

class CarouselImageField(serializers.RelatedField):
    def to_native(self, value):
        return value.get_rendition('fill-240x240').url
                

class PageField(serializers.RelatedField):
    def to_native(self, value):
        return value.title

class BlogListSerializer(serializers.ModelSerializer):
    head_image = ImageField()
    
    class Meta:
        model = BlogPage
        fields = ('id', 'title', 'head_image', 'desc', 'date')



class CommentSerializer(serializers.Serializer):
    pk = serializers.Field()
    owner = serializers.Field()   
    body = serializers.CharField(max_length=255)
    date = serializers.DateTimeField(blank=True)
    
    def restore_object(self, attrs, instance=None):
        if instance is not None:
            instance.body = attrs.get('body', instance.body)
            return instance
        attrs['owner'] = self.context['owner']
        attrs['blog'] = self.context['blog']
        return Comment(**attrs)

    class Meta:
        fields = ('owner', 'body', 'date')

class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(required=True)
    email = serializers.EmailField(max_length=255, required=True)

    def restore_object(self, attrs, instance=None):
        if instance is not None:
            instance.username = attrs.get('username', instance.username)
            instance.password = attrs.get('password', instance.password)
            instance.email = attrs.get('email', instance.email)
            return instance
        return User(**attrs)
        

    def create_user(self):
        if User.objects.filter(email=self.init_data['email']).exists():
            return {'email':'Already existed!'};

        new_user = None;
        try:
            new_user = User.objects.create_user(**self.init_data)
        except:
            return {'username':'Already existed!'}

        token = Token.objects.filter(user=new_user.id)[0]
        data = {'username': new_user.username,
                'auth_token': token.key
               }
        return data
'''
class HeadphonesListSerializer(serializers.Serializer):
'''
    
class HeadphonesListSerializer(serializers.ModelSerializer):
    head_image = ImageField()
    class Meta:
        model = Headphones
        #fields = ('title', 'description', 'transducer', 'wear_type', 'wire_length', 'size', 'weight')
        fields = ('id', 'title', 'head_image')

class CarouselItemSerializer(serializers.Serializer):
    image = CarouselImageField()

class HeadphonesDetailSerializer(serializers.Serializer):
    carousel_items = CarouselItemSerializer(many=True)
    title = serializers.CharField()
    description = serializers.CharField(max_length=1024)
    transducer = serializers.CharField(max_length=2)
    wear_type = serializers.CharField(max_length=2)
    wire_length = serializers.FloatField()
    frequency_range = serializers.CharField(max_length=127)
    impendance = serializers.FloatField()
    sensitivity = serializers.FloatField()
    weight = serializers.FloatField()

