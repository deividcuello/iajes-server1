from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.pagination import PageNumberPagination
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Project
from .serializers import ProjectSerializer
from django.forms.models import model_to_dict


class ProjectsApiView(APIView, PageNumberPagination):
    page_size = 8

    # 1. List all
    def get(self, request, *args, **kwargs):
        industry = request.GET.get('industry')
        university = (request.GET.get('university'))
        association = request.GET.get('association')
        start_year = (request.GET.get('start_year'))
        end_year = (request.GET.get('end_year'))
        investigator = (request.GET.get('investigator'))
        projectName = (request.GET.get('projectName'))
        id = (request.GET.get('id'))
        approved = (request.GET.get('approved'))
        keyword = (request.GET.get('keyword'))
        userId = (request.GET.get('userId'))
        isAdmin = (request.GET.get('isAdmin'))

        if(approved == 'true'):
            approved = True
        elif(approved == 'false'):
            approved = False
        else:
            approved = 'None'
        
        if(industry):
            if(industry != 'true'):
                project = Project.objects.all().filter(industry=industry).order_by('-created_at')
            else:
                project = Project.objects.all().order_by('-created_at')
            if(university):
                project = project.filter(college__icontains=university).order_by('-created_at')
            elif(association):
                project = project.filter(region__icontains=association).order_by('-created_at')
            elif(start_year):
                project = project.filter(start_year__icontains=start_year).order_by('-created_at')
            elif(end_year):
                project = project.filter(end_year__icontains=end_year).order_by('-created_at')
            elif(investigator):
                project = project.filter(investigator__icontains=investigator).order_by('-created_at')
            elif(projectName):
                project = project.filter(title__icontains=projectName).order_by('-created_at')
            elif(keyword):
                project = project.filter(keywords__icontains=keyword).order_by('-created_at')
            elif(id):
                project = project.filter(id=id).order_by('-created_at')
            elif(userId and userId != 'undefined'):
                project = project.filter(user=userId).order_by('-created_at')
        else:
            project = Project.objects.all().order_by('-created_at')
        
        if(isAdmin == 'false'):
            project = project.filter(hidden=False).order_by('-created_at')
        
        if(approved != 'None'):
            project = project.filter(approved=approved).order_by('-created_at')
        
        projectCount = project.count()
        results = self.paginate_queryset(project, request, view=self)
        serializer = ProjectSerializer(results, many=True)
        return Response({
            'projects': serializer.data,
            'count': projectCount,
            }, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):

        data = {
            'title': request.data.get('title'), 
            'image_url': request.data.get('image_url'), 
            'college': request.data.get('college'), 
            'investigator': request.data.get('investigator'), 
            'start_year': request.data.get('start_year'), 
            'end_year': request.data.get('end_year'), 
            'isWorking': request.data.get('isWorking'), 
            'industry': request.data.get('industry'), 
            'region': request.data.get('region'), 
            'summary': request.data.get('summary'), 
            'email': request.data.get('email'),
            'approved': request.data.get('approved'),
            'partner_organization': request.data.get('partner_organization'),
            'keywords': request.data.get('keywords'),
            'published_date': request.data.get('published_date'),
            'hidden': request.data.get('hidden'),
            'user': request.data.get('user')
        }

        serializer = ProjectSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ProjectDetailApiView(APIView):
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    # permission_classes = [HasRequiredPermissionForMethod]
    # get_permission_required = 'permission_to_read_this'
    # put_permission_required = 'permission_to_update_this'
    # post_permission_required = 'permission_to_create_this'

    lookup_field = 'slug'
    
    def get_object(self, slug, user_id):

        try:
            return Project.objects.get(slug=slug)
        except Project.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, slug, *args, **kwargs):

        project_instance = self.get_object(slug, request.user.id)
        if not project_instance:
            return Response(
                {"res": "Object with id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ProjectSerializer(project_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, slug, *args, **kwargs):
        isImageUrl = 'http://localhost:8000/media' in request.data.get('isImageUrl')

        project_instance = self.get_object(slug, request.user.id)
        if not project_instance:
            return Response(
                {"res": "Object with id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        if(not isImageUrl):
            data = {
            'title': request.data.get('title'), 
            'image_url': request.data.get('image_url'), 
            'college': request.data.get('college'), 
            'investigator': request.data.get('investigator'), 
            'industry': request.data.get('industry'), 
            'region': request.data.get('region'), 
            'start_year': request.data.get('start_year'), 
            'end_year': request.data.get('end_year'), 
            'isWorking': request.data.get('isWorking'), 
            'summary': request.data.get('summary'), 
            'email': request.data.get('email'),
            'approved': request.data.get('approved'),
            'published_date': request.data.get('published_date'),
            'partner_organization': request.data.get('partner_organization'),
            'keywords': request.data.get('keywords'),
            'hidden': request.data.get('hidden'),
        }
        else:
            data = {
            'title': request.data.get('title'), 
            'college': request.data.get('college'), 
            'investigator': request.data.get('investigator'), 
            'industry': request.data.get('industry'), 
            'region': request.data.get('region'), 
            'start_year': request.data.get('start_year'), 
            'end_year': request.data.get('end_year'), 
            'isWorking': request.data.get('isWorking'), 
            'summary': request.data.get('summary'), 
            'email': request.data.get('email'),
            'approved': request.data.get('approved'),
            'published_date': request.data.get('published_date'),
            'partner_organization': request.data.get('partner_organization'),
            'keywords': request.data.get('keywords'),
            'hidden': request.data.get('hidden'),
        }
        
        serializer = ProjectSerializer(instance = project_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, slug, *args, **kwargs):

        project_instance = self.get_object(slug, request.user.id)
        if not project_instance:
            return Response(
                {"res": "Object with id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        project_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )

    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    # permission_classes = [HasRequiredPermissionForMethod]
    # get_permission_required = 'permission_to_read_this'
    # put_permission_required = 'permission_to_update_this'
    # post_permission_required = 'permission_to_create_this'
    
    lookup_field = 'slug'
    