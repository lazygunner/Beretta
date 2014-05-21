from django.http import Http404
from rest_framework import routers
from rest_framework.views import APIView
from rest_framework.response import Response
from app_backend.models import BlogPage
from app_backend.serializers import BlogDetailSerializer

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
    
    def get(self, request):
        blog_list = BlogPage.objects.all()
        serializer = BlogDetailSerializer(blog_list, many=True)
        return Response(serializer.data)

#router = routers.DefaultRouters()

#router.register(r'blog/$', BlogListView)
#router.register(r'blog/(?P<pk>[0-9]+)/$', BlogDetailViewSet)

