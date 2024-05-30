from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.pagination import PageNumberPagination
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Video
from .serializers import VideoSerializer
from django.forms.models import model_to_dict

class VideoApiView(APIView, PageNumberPagination):
    page_size = 8

    # 1. List all
    def get(self, request, *args, **kwargs):
        videoTitle = (request.GET.get('videoTitle'))
        id = (request.GET.get('id'))
        isAdmin = (request.GET.get('isAdmin'))
        isPagination = (request.GET.get('isPagination'))

        videos = Video.objects.all().order_by('-created_at')
        if(videoTitle):
            videos = videos.filter(title__icontains=videoTitle).order_by('-created_at')
        elif(id):
            videos = videos.filter(id=id).order_by('-created_at')

        if(isAdmin == 'false'):
            videos = videos.filter(hidden=False).order_by('-created_at')

        videosCount = videos.count()
        if(isPagination == 'true'):
            results = self.paginate_queryset(videos, request, view=self)
            serializer = VideoSerializer(results, many=True)
        else:
            serializer = VideoSerializer(videos, many=True)

        return Response({
            'videos': serializer.data,
            'count': videosCount,
            }, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):

        data = {
            'video_url': request.data.get('video_url'), 
            'title': request.data.get('title'), 
            'hidden': request.data.get('hidden'),
        }

        serializer = VideoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VideoDetailApiView(APIView):
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    # permission_classes = [HasRequiredPermissionForMethod]
    # get_permission_required = 'permission_to_read_this'
    # put_permission_required = 'permission_to_update_this'
    # post_permission_required = 'permission_to_create_this'
    
    def get_object(self, video_id, user_id):

        try:
            return Video.objects.get(id=video_id)
        except VideoApiView.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, video_id, *args, **kwargs):
 
        video_instance = self.get_object(video_id, request.user.id)
        if not video_instance:
            return Response(
                {"res": "Object with id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = VideoSerializer(video_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, video_id, *args, **kwargs):
        # isImageUrl = 'http://localhost:8000/media' in request.data.get('isImageUrl')
        
        video_instance = self.get_object(video_id, request.user.id)
        if not video_instance:
            return Response(
                {"res": "Object with id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
                'video_url': request.data.get('video_url'), 
                'title': request.data.get('title'), 
                'hidden': request.data.get('hidden'),
            }

        serializer = VideoSerializer(instance = video_instance, data=data, partial = True)
        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, video_id, *args, **kwargs):

        video_instance = self.get_object(video_id, request.user.id)
        if not video_instance:
            return Response(
                {"res": "Object with id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        video_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )
