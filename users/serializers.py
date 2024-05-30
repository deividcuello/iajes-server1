from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError

UserModel = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserModel
		fields = '__all__'
	def create(self, clean_data):
		user_obj = UserModel.objects.create_user(
			email=clean_data['email'], 
			password=clean_data['password'],)
		user_obj.username = clean_data['username']
		user_obj.phone = clean_data['phone']
		user_obj.university = clean_data['university']
		user_obj.department = clean_data['department']
		user_obj.name = clean_data['name']
		# user_obj.status = clean_data['status']
		user_obj.isDelete = (True, False) [clean_data['isDelete'] == 'false']
		user_obj.adminAccount = (True, False) [clean_data['adminAccount'] == 'false']
		user_obj.save()
		return user_obj

class UserLoginSerializer(serializers.Serializer):
	email = serializers.EmailField()
	password = serializers.CharField()
	##
	def check_user(self, clean_data):
		user = authenticate(username=clean_data['email'], password=clean_data['password'])
		if not user:
			raise ValidationError('user not found')
		return user

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserModel
		fields = ('id', 'email', 'username', 'name', 'password', 'isDelete', 'adminAccount', 'phone', 'university', 'department')
	
	def update(self, instance, validated_data):
		if 'password' in validated_data:
			password = validated_data.pop('password', None)
			instance.set_password(password)
		return super().update(instance, validated_data)

class UsersSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserModel
		fields = ('id', 'email', 'username', 'name', 'password', 'isDelete', 'adminAccount', 'phone', 'university', 'department')