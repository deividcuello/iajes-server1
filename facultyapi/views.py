from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.pagination import PageNumberPagination
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Faculty
from .serializers import FacultySerializer
from django.forms.models import model_to_dict


class FacultyApiView(APIView, PageNumberPagination):
    page_size = 8

    # 1. List all
    def get(self, request, *args, **kwargs):
        facultyTitle = (request.GET.get('facultyTitle'))
        email = (request.GET.get('email'))
        country = (request.GET.get('country'))
        topic = (request.GET.get('topic'))
        university = (request.GET.get('university'))
        id = (request.GET.get('id'))
        isAdmin = (request.GET.get('isAdmin'))

        faculty = Faculty.objects.all().order_by('-created_at')
        if(facultyTitle):
            faculty = faculty.filter(title__icontains=facultyTitle).order_by('-created_at')
        elif(email):
            faculty = faculty.filter(email__icontains=email).order_by('-created_at')
        elif(country):
            faculty = faculty.filter(country__icontains=country).order_by('-created_at')
        elif(topic):
            faculty = faculty.filter(topics__icontains=topic).order_by('-created_at')
        elif(university):
            faculty = faculty.filter(university__icontains=university).order_by('-created_at')
        elif(id):
            faculty = faculty.filter(id=id).order_by('-created_at')

        if(isAdmin == 'false'):
            faculty = faculty.filter(hidden=False).order_by('-created_at')

        facultyCount = faculty.count()
        results = self.paginate_queryset(faculty, request, view=self)
        serializer = FacultySerializer(results, many=True)
        return Response({
            'faculty': serializer.data,
            'count': facultyCount,
            }, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        data = {
            'university': request.data.get('university'), 
            'email': request.data.get('email'), 
            'title': request.data.get('title'), 
            'country': request.data.get('country'), 
            'topics': request.data.get('topics'), 
            'hidden': request.data.get('hidden'), 
        }


        serializer = FacultySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FacultyDetailApiView(APIView):
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    # permission_classes = [HasRequiredPermissionForMethod]
    # get_permission_required = 'permission_to_read_this'
    # put_permission_required = 'permission_to_update_this'
    # post_permission_required = 'permission_to_create_this'
    
    def get_object(self, faculty_id, user_id):

        try:
            return Faculty.objects.get(id=faculty_id)
        except FacultyApiView.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, faculty_id, *args, **kwargs):
 
        faculty_instance = self.get_object(faculty_id, request.user.id)
        if not faculty_instance:
            return Response(
                {"res": "Object with id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = FacultySerializer(faculty_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, faculty_id, *args, **kwargs):

        faculty_instance = self.get_object(faculty_id, request.user.id)
        if not faculty_instance:
            return Response(
                {"res": "Object with id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'university': request.data.get('university'), 
            'email': request.data.get('email'), 
            'title': request.data.get('title'), 
            'country': request.data.get('country'), 
            'topics': request.data.get('topics'), 
            'hidden': request.data.get('hidden'), 
        }

        serializer = FacultySerializer(instance = faculty_instance, data=data, partial = True)
        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, faculty_id, *args, **kwargs):

        faculty_instance = self.get_object(faculty_id, request.user.id)
        if not faculty_instance:
            return Response(
                {"res": "Object with id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        faculty_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )
