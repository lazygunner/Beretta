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

        # Filter by date
        date = request.GET.get('date')
        if date:
            blogs = blogs.filter(date__lte=date)

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
   
    def get(self, request):
        blog_list = get_context(request)
        serializer = BlogDetailSerializer(blog_list, many=True)
        return Response(serializer.data)

#router = routers.DefaultRouters()

#router.register(r'blog/$', BlogListView)
#router.register(r'blog/(?P<pk>[0-9]+)/$', BlogDetailViewSet)

