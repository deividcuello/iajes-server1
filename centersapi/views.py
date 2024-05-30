from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.pagination import PageNumberPagination
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Center
from .serializers import CenterSerializer
from django.forms.models import model_to_dict

class CenterApiView(APIView, PageNumberPagination):
    page_size = 8

    # 1. List all
    def get(self, request, *args, **kwargs):
        director = (request.GET.get('director'))
        center = (request.GET.get('center'))
        phone = (request.GET.get('phone'))
        id = (request.GET.get('id'))
        isAdmin = (request.GET.get('isAdmin'))

        centers = Center.objects.all().order_by('-created_at')
        if(center):
            centers = centers.filter(center__icontains=center).order_by('-created_at')
        elif(director):
            centers = centers.filter(director__icontains=director).order_by('-created_at')
        elif(phone):
            centers = centers.filter(phone__icontains=phone).order_by('-created_at')
        elif(id):
            centers = centers.filter(id=id).order_by('-created_at')

        if(isAdmin == 'false'):
            centers = centers.filter(hidden=False).order_by('-created_at')

        centersCount = centers.count()
        results = self.paginate_queryset(centers, request, view=self)
        serializer = CenterSerializer(results, many=True)
        return Response({
            'centers': serializer.data,
            'count': centersCount,
            }, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):

        data = {
            'center': request.data.get('center'), 
            'cover_url': request.data.get('cover_url'), 
            'program_name': request.data.get('program_name'), 
            'phone': request.data.get('phone'), 
            'location': request.data.get('location'), 
            'email': request.data.get('email'), 
            'hidden': request.data.get('hidden'), 
        }

        serializer = CenterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CenterDetailApiView(APIView):
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    # permission_classes = [HasRequiredPermissionForMethod]
    # get_permission_required = 'permission_to_read_this'
    # put_permission_required = 'permission_to_update_this'
    # post_permission_required = 'permission_to_create_this'
    
    def get_object(self, center_id, user_id):

        try:
            return Center.objects.get(id=center_id)
        except CenterApiView.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, center_id, *args, **kwargs):
 
        center_instance = self.get_object(center_id, request.user.id)
        if not center_instance:
            return Response(
                {"res": "Object with id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = CenterSerializer(center_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, center_id, *args, **kwargs):
        isImageUrl = 'http://localhost:8000/media' in request.data.get('isImageUrl')

        center_instance = self.get_object(center_id, request.user.id)
        if not center_instance:
            return Response(
                {"res": "Object with id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        if(isImageUrl):
            data = {
            'center': request.data.get('center'), 
            'program_name': request.data.get('program_name'), 
            'phone': request.data.get('phone'), 
            'location': request.data.get('location'), 
            'email': request.data.get('email'), 
            'hidden': request.data.get('hidden'), 
        }
        else:
            data = {
            'center': request.data.get('center'), 
            'cover_url': request.data.get('cover_url'), 
            'program_name': request.data.get('program_name'), 
            'phone': request.data.get('phone'), 
            'location': request.data.get('location'), 
            'email': request.data.get('email'), 
            'hidden': request.data.get('hidden'), 
        }


        serializer = CenterSerializer(instance = center_instance, data=data, partial = True)
        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, center_id, *args, **kwargs):

        center_instance = self.get_object(center_id, request.user.id)
        if not center_instance:
            return Response(
                {"res": "Object with id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        center_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )
