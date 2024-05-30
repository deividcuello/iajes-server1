from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.pagination import PageNumberPagination
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Document
from .serializers import DocumentSerializer
from django.forms.models import model_to_dict



class DocApiView(APIView, PageNumberPagination):
    page_size = 8

    # 1. List all
    def get(self, request, *args, **kwargs):
        docTitle = (request.GET.get('docTitle'))
        docAuthor = (request.GET.get('docAuthor'))
        docYear = (request.GET.get('docYear'))
        isAdmin = (request.GET.get('isAdmin'))
        id = (request.GET.get('id'))

        docs = Document.objects.all().order_by('-created_at')

        if(docTitle):
            docs = docs.filter(title__icontains=docTitle).order_by('-created_at')
        elif(docAuthor):
            docs = docs.filter(author__icontains=docAuthor).order_by('-created_at')
        elif(docYear):
            docs = docs.filter(year__icontains=docYear).order_by('-created_at')
        elif(id):
            docs = docs.filter(id=id).order_by('-created_at')

        if(isAdmin == 'false'):
            docs = docs.filter(hidden=False).order_by('-created_at')

        docsCount = docs.count()
        results = self.paginate_queryset(docs, request, view=self)
        serializer = DocumentSerializer(results, many=True)
        return Response({
            'docs': serializer.data,
            'count': docsCount,
            }, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):

        data = {
            'title': request.data.get('title'), 
            # 'cover_url': request.data.get('cover_url'), 
            'document': request.data.get('doc'), 
            'year': request.data.get('year'), 
            'author': request.data.get('author'), 
            'hidden': request.data.get('hidden'),
        }

        serializer = DocumentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DocDetailApiView(APIView):
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    # permission_classes = [HasRequiredPermissionForMethod]
    # get_permission_required = 'permission_to_read_this'
    # put_permission_required = 'permission_to_update_this'
    # post_permission_required = 'permission_to_create_this'
    
    def get_object(self, doc_id, user_id):

        try:
            return Document.objects.get(id=doc_id)
        except DocApiView.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, doc_id, *args, **kwargs):
 
        doc_instance = self.get_object(doc_id, request.user.id)
        if not doc_instance:
            return Response(
                {"res": "Object with id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = DocumentSerializer(doc_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, doc_id, *args, **kwargs):
        # isImageUrl = 'http://localhost:8000/media' in request.data.get('isImageUrl')
        isDocUrl = 'http://localhost:8000/media' in request.data.get('isDocUrl')

        doc_instance = self.get_object(doc_id, request.user.id)
        if not doc_instance:
            return Response(
                {"res": "Object with id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        if(isDocUrl):
            data = {
                'title': request.data.get('title'), 
                # 'cover_url': request.data.get('cover_url'),
                'year': request.data.get('year'), 
                'author': request.data.get('author'), 
                'hidden': request.data.get('hidden'),
            }
        else:
            data = {
                'title': request.data.get('title'), 
                # 'cover_url': request.data.get('cover_url'), 
                'document': request.data.get('doc'), 
                'year': request.data.get('year'), 
                'author': request.data.get('author'), 
                'hidden': request.data.get('hidden'),
            }

        serializer = DocumentSerializer(instance = doc_instance, data=data, partial = True)
        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, doc_id, *args, **kwargs):

        doc_instance = self.get_object(doc_id, request.user.id)
        if not doc_instance:
            return Response(
                {"res": "Object with id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        doc_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )
