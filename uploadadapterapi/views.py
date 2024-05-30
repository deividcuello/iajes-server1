from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UploadAdapter
from .serializers import UploadAdapterSerializer
from uploadadapterapi.models import UploadAdapter

class UploadAdapterApiView(APIView):
    # page_size = 5
    # add permission to check if user is authenticated
    #permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):

        images = UploadAdapter.objects.all().order_by('-created_at')

        imagesCount = images.count()
        # results = self.paginate_queryset(images, request, view=self)
        serializer = UploadAdapterSerializer(images, many=True)
        return Response({
            'images': serializer.data,
            'count': imagesCount}, status=status.HTTP_200_OK)
    # 2. Create
    def post(self, request, *args, **kwargs):

        data = {
            'image': request.data.get('uploadImg'), 
        }
        serializer = UploadAdapterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            image_id = list(UploadAdapter.objects.all().values_list('id', flat=True))[-1]

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UploadAdapterDetailApiView(APIView):
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    # permission_classes = [HasRequiredPermissionForMethod]
    # get_permission_required = 'permission_to_read_this'
    # put_permission_required = 'permission_to_update_this'
    # post_permission_required = 'permission_to_create_this'
    
    def get_object(self, image_id, user_id):

        try:
            return UploadAdapter.objects.get(id=image_id)
        except UploadAdapter.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, image_id, *args, **kwargs):

        image_instance = self.get_object(image_id, request.user.id)
        if not image_instance:
            return Response(
                {"res": "Object with id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = UploadAdapterSerializer(image_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, image_id, *args, **kwargs):

        isImageUrl = 'http://localhost:8000/media' in request.data.get('isImageUrl')
        image_instance = self.get_object(image_id, request.user.id)
        if not image_instance:
            return Response(
                {"res": "Object with id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        if(not isImageUrl):
            data = {
                'image': request.data.get('image'),
            }


        serializer = UploadAdapterSerializer(instance = image_instance, data=data, partial = True)
        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, image_id, *args, **kwargs):

        image_instance = self.get_object(image_id, request.user.id)
        if not image_instance:
            return Response(
                {"res": "Object with id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        image_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )
