from django.contrib.auth import get_user_model, login, logout
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer
from rest_framework import permissions, status
from rest_framework.pagination import PageNumberPagination
from .validations import custom_validation, validate_email, validate_password
from .models import AppUser

class UserRegister(APIView):
	permission_classes = (permissions.AllowAny,)
    
	def post(self, request):
		clean_data = custom_validation(request.data)
		serializer = UserRegisterSerializer(data=clean_data)
		if serializer.is_valid(raise_exception=True):
			user = serializer.create(clean_data)
			if user:
				return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = (SessionAuthentication,)
	##
	def post(self, request):
		data = request.data
		assert validate_email(data)
		assert validate_password(data)
		serializer = UserLoginSerializer(data=data)
		if serializer.is_valid(raise_exception=True):
			user = serializer.check_user(data)
			login(request, user)
			return Response(serializer.data, status=status.HTTP_200_OK)


class UserLogout(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = ()
	def post(self, request):
		logout(request)
		return Response(status=status.HTTP_200_OK)


class UserView(APIView):

	##
	def get(self, request):
		serializer = UserSerializer(request.user)
		return Response({'user': serializer.data}, status=status.HTTP_200_OK)


class UsersView(APIView, PageNumberPagination):
    page_size = 8
    def get(self, request):
        id = (request.GET.get('id'))
        contain_word = (request.GET.get('contain'))
        isAdmin = request.GET.get('isAdmin')
        email = request.GET.get('email')
        username = request.GET.get('username')
        username_search = request.GET.get('username_search')
        email_search = request.GET.get('email_search')

        if(username_search != 'null' and username_search != None):
            users = AppUser.objects.all().filter(username=username_search).order_by('-created_at')
        elif(email_search != 'null' and email_search != None):
            users = AppUser.objects.all().filter(email=email_search).order_by('-created_at')
        elif (id != 'null' and id != None):
            users = AppUser.objects.all().filter(id=id).order_by('-created_at')
        elif (contain_word != 'null' and contain_word != None):
            users = AppUser.objects.all().filter(username__icontains=contain_word).order_by('-created_at')
        elif (email != 'null' and email != None):
            users = AppUser.objects.all().filter(email__icontains=email).order_by('-created_at')
        elif (username != 'null' and username != None):
            users = AppUser.objects.all().filter(username__icontains=username).order_by('-created_at')
        else:
            users = AppUser.objects.all().order_by('-created_at')
        if(isAdmin == 'false'):
            users = AppUser.filter(hidden=False).order_by('-created_at')

        usersCount = users.count()
        results = self.paginate_queryset(users, request, view=self)
 
        serializer = UserSerializer(results, many=True)
        return Response({
            'users': serializer.data, 
            'count': usersCount,}, status=status.HTTP_200_OK)


class UserDetailApiView(APIView):
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    def get_object(self, username_id, user_id):
        
        try:
            # return Note.objects.get(id=note_id, user = user_id)
            return AppUser.objects.get(id=username_id)
        except AppUser.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, username_id, *args, **kwargs):
        username_instance = self.get_object(username_id, request.user.id)
        if not username_instance:
            return Response(
                {"res": "Object with id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = UserSerializer(username_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, username_id, *args, **kwargs):
        recover_password = request.data.get('recover_password')
        update_username = request.data.get('update_username')
        update_password = request.data.get('update_password')
        update_email = request.data.get('update_email')
        update_phone = request.data.get('update_phone')
        update_name = request.data.get('update_name')
        update_university = request.data.get('update_university')
        update_department = request.data.get('update_department')
        
        username_instance = self.get_object(username_id, request.user.id)
        if not username_instance:
            return Response(
                {"res": "Object with id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        if(recover_password or update_password):
            data = {
                'password': request.data.get('password')
            }
        elif(update_username):
            data = {
                'username': request.data.get('username')
            }
        elif(update_phone):
            data = {
                'phone': request.data.get('phone')
            }
        elif(update_email):
            data = {
                'email': request.data.get('email')
            }
        elif(update_name):
            data = {
                'name': request.data.get('name')
            }
        elif(update_university):
            data = {
                'university': request.data.get('university')
            }
        elif(update_department):
            data = {
                'department': request.data.get('department')
            }
        elif(request.data.get('password')):
            data = {
                'email': request.data.get('email'),
                'username': request.data.get('username'),
                'password': request.data.get('password'),
                'phone': request.data.get('phone'),
                'department': request.data.get('department'),
                'university': request.data.get('university'),
                'name': request.data.get('name'),
                'adminAccount': request.data.get('adminAccount'),
            }
        else:
            data = {
                'email': request.data.get('email'),
                'username': request.data.get('username'),
                'phone': request.data.get('phone'),
                'department': request.data.get('department'),
                'university': request.data.get('university'),
                'name': request.data.get('name'),
                'adminAccount': request.data.get('adminAccount'),
            }

        serializer = UserSerializer(instance = username_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, username_id, *args, **kwargs):

        username_instance = self.get_object(username_id, request.user.id)
        serializer = UserSerializer(username_instance)
        if not username_instance:
            return Response(
                {"res": "Object with id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        if(not serializer.data['isDelete']):
            return Response(
            {"res": "No deleted because isDelete is False!"},
            status=status.HTTP_200_OK
        )
 
        username_instance.delete()
        
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )
