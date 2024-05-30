from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import News
from .serializers import NewsSerializer
from rest_framework import permissions

class NewsApiView(APIView, PageNumberPagination):
    page_size = 8

    # 1. List all
    def get(self, request, *args, **kwargs):
        headline = (request.GET.get('headline'))
        id = (request.GET.get('id'))
        created_at = (request.GET.get('created_at'))
        isAdmin = (request.GET.get('isAdmin'))
        news = News.objects.all().order_by('-created_at')

        if(headline):
            news = news.filter(title__icontains=headline).order_by('-created_at')
        elif(id):
            news = news.filter(id=id).order_by('-created_at')
        elif(created_at):
            news = news.filter(created_at__icontains=created_at).order_by('-created_at')
        if(isAdmin == 'false'):
            news = news.filter(hidden=False).order_by('-created_at')

        newsCount = news.count()
        results = self.paginate_queryset(news, request, view=self)
        serializer = NewsSerializer(results, many=True)
        return Response({
            'news': serializer.data,
            'count': newsCount
            }, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):

        data = {
            'image_url': request.data.get('image_url'), 
            'title': request.data.get('title'), 
            'description': request.data.get('description'),
            'hidden': request.data.get('hidden'),
            # 'user': request.user.id
        }


        serializer = NewsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            news_id = list(News.objects.all().values_list('id', flat=True))[-1]
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NewsDetailApiView(APIView):
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    # permission_classes = [HasRequiredPermissionForMethod]
    get_permission_required = 'permission_to_read_this'
    put_permission_required = 'permission_to_update_this'
    post_permission_required = 'permission_to_create_this'

    lookup_field = 'slug'
    
    def get_object(self, slug, user_id):

        try:
            return News.objects.get(slug=slug)
        except News.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, slug, *args, **kwargs):

        news_instance = self.get_object(slug, request.user.id)
        if not news_instance:
            return Response(
                {"res": "Object with id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = NewsSerializer(news_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, slug, *args, **kwargs):
        isImageUrl = 'http://localhost:8000/media' in request.data.get('isImageUrl')

        news_instance = self.get_object(slug, request.user.id)
        if not news_instance:
            return Response(
                {"res": "Object with id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        if(not isImageUrl):
            data = {
                'image_url': request.data.get('image_url'), 
                'title': request.data.get('title'), 
                'description': request.data.get('description'),
                'hidden': request.data.get('hidden'),
                # 'user': request.user.id
            }
        else:
            
            data = {
                'title': request.data.get('title'), 
                'description': request.data.get('description'),
                'hidden': request.data.get('hidden'),
                # 'user': request.user.id
            }

        
        serializer = NewsSerializer(instance = news_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, slug, *args, **kwargs):

        news_instance = self.get_object(slug, request.user.id)
        if not news_instance:
            return Response(
                {"res": "Object with id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        news_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )
