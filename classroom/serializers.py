from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class ClassRoomSerializer(serializers.ModelSerializer):
    teacher = UserSerializer(many=False,read_only=True)
    class Meta:
        model = ClassRoom
        fields = '__all__' 

 