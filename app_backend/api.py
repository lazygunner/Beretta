from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from app_backend.models import BlogPage, Comment
from app_backend.serializers import BlogDetailSerializer, BlogListSerializer, CommentSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly

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

    def get_blog_list(self, request):
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


        return blogs[:10]
   
    def get(self, request):
        blog_list = self.get_blog_list(request)
        serializer = BlogListSerializer(blog_list, many=True)
        return Response(serializer.data)


class CommentListView(APIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticatedOrReadOnly,]
   
    def get_comment_list(self, request, blog_pk):
        try:
            comments = Comment.objects.filter(blog=blog_pk)
            return comments
        except Comment.DoesNotExist:
            raise Http404
        

    def get(self, request, blog_pk):
        comment_list = self.get_comment_list(request, blog_pk=blog_pk)
        serializer = CommentSerializer(comment_list, many=True)
        return Response(serializer.data)

    def post(self, request, blog_pk):
        data = request.DATA
        context = {}
        context['blog'] = BlogPage.objects.get(pk=blog_pk)
        context['owner'] = request.user
        serializer = CommentSerializer(data=data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDetailView(APIView):
     
    def get_comment(self, pk):
        try:
            return Comment.objects(pk=pk)
        except Comment.DoesNotExist:
            raise Http404
   
    def get(self, request, pk):
        comment = get_comment(pk=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)


