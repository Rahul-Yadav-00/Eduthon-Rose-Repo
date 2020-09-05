from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from rest_framework.decorators import  api_view
from rest_framework.response import Response

from .models import *
from .serializers import *

# Create your views here.

@api_view(['GET'])
@login_required(login_url='signin')
def allJoinclass(request):
    user = request.user
    if(ClassStudents.objects.filter(student = user).exists()):
        classstudent = ClassStudents.objects.filter(student = user)
        classes_join = []
        for i in classstudent:
            classes_join.append(i.classroom)
        serializer = ClassRoomSerializer(classes_join,many=True)
        return Response(serializer.data)
    else:
        return HttpResponse("you not join any class yet")

@api_view(['GET'])
@login_required(login_url='signin')
def allOwnclass(request):
    if(ClassRoom.objects.filter(teacher = request.user).exists()):
        classrooms = ClassRoom.objects.filter(teacher = request.user)
        serializer = ClassRoomSerializer(classrooms,many=True)
        return Response(serializer.data)
    else:   
        return HttpResponse('you not create any classroom yet')