from django.http import Http404
from rest_framework import routers
from rest_framework.views import APIView
from rest_framework.response import Response
from app_backend.models import BlogPage
from app_backend.serializers import BlogDetailSerializer, BlogListSerializer

class BlogDetailView(APIView):

    def get_object(self, pk):
        try:
            return BlogPage.objects.get(pk=pk)
        except BlogPage.DoesNotExist:
            raise Http404
   
    def get(self, request, pk):
        blog_detail = self.get_object(pk=pk)
        serializer = BlogDetailSerializer(blog_detail)
        return Response(serializer.data)

class BlogListView(APIView):
    
    @property
    def blogs(self):
        # Get list of live blog pages that are descendants of this page
        blogs = BlogPage.objects.live()

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

        # Filter by date
        date = request.GET.get('date')
        if date:
            blogs = blogs.filter(date__lte=date)


        return blogs
   
    def get(self, request):
        blog_list = self.get_context(request)
        serializer = BlogListSerializer(blog_list, many=True)
        return Response(serializer.data)

#router = routers.DefaultRouters()

#router.register(r'blog/$', BlogListView)
#router.register(r'blog/(?P<pk>[0-9]+)/$', BlogDetailViewSet)

