from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseBadRequest
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

@login_required(login_url='signin')
def joinClass(request):
    if(request.method == 'POST'):
        clscode = request.POST['classcode']
        if(ClassRoom.objects.filter(classCode = clscode).exists()):
            classroom = ClassRoom.objects.get(classCode = clscode)
            if(classroom.teacher == request.user):
                messages.error(request,'you are teacher in this class')
                return redirect('index')
            else:
                class_student = ClassStudents.objects.create(student=request.user,classroom = classroom)
                messages.success(request,'class is joined')
                return redirect('index')
        else:
            messages.error(request,'wrong class code')
            return redirect('index')
    else:
        return HttpResponseBadRequest("error")

@login_required(login_url='signin')
def createClass(request): 
    if(request.method == 'POST'):
        classname = request.POST['classname']
        classdecription = request.POST['classdescription']
        classsubject = request.POST['classsubject']
        classroom = ClassRoom.objects.create(classname=classname,classdecription=classdecription,
                                                classsubject=classsubject,teacher=request.user)
        messages.success(request,'class is created')
        return  redirect('index')
    else:
        messages.error(request,'error')
        return redirect('index')

@login_required(login_url='signin')
def classDetails(request,clscode):
    classroom = ClassRoom.objects.get(classCode=clscode)
    if(classroom.teacher == request.user):
        classroom = ClassRoom.objects.get(classCode = clscode)
        class_students =  ClassStudents.objects.none()
        students = []
        if(ClassStudents.objects.filter(classroom = classroom).exists()):
            class_students = ClassStudents.objects.filter(classroom = classroom)
            for c_s in class_students:
                students.append(c_s.student)
        chats = Chat.objects.none()
        if(Chat.objects.filter(classroom = classroom).exists()):
            chats  = Chat.objects.filter(classroom = classroom)

        data = {'students':students,'chats':chats}
        return render(request,'classroom/ownclass.html',data)
    else:
        classroom = ClassRoom.objects.get(classCode = clscode)
        class_students =  ClassStudents.objects.none()
        students = []
        if(ClassStudents.objects.filter(classroom = classroom).exists()):
            class_students = ClassStudents.objects.filter(classroom = classroom)
            for c_s in class_students:
                students.append(c_s.student)
        chats = Chat.objects.none()
        if(Chat.objects.filter(classroom = classroom).exists()):
            chats  = Chat.objects.filter(classroom = classroom)

        data = {'students':students,'chats':chats}
        return render(request,'classroom/joinclass.html',data)

@login_required(login_url='signin')
def createTest(request,clscode):
    if(request.method == 'POST'):
        classroom = ClassRoom.objects.get(classCode = clscode)
        testname = request.POST['name']
        topics = request.POST['testtopic']
        test = ClassTest.objects.create(classroom = classroom,name = testname,testTopic = topics)

        questions = request.POST.getlist('questions[]')
        options_a = request.POST.getlist('options_a[]')
        options_b = request.POST.getlist('options_b[]')
        options_c = request.POST.getlist('options_c[]')
        options_d = request.POST.getlist('options_d[]')
        answers = request.POST.getlist('answers[]')

        mcqs = zip(questions,options_a,options_b,options_c,options_d,answers)
        
        for question,option_a,option_b,option_c,option_d,answer in mcqs:
            mcq = MCQuestion.objects.create(test=test,question = question,
                                            option_a = option_a,option_b=option_b,
                                            option_c=option_c,option_d=option_d,
                                            answer = answer)

        return HttpResponse("creaesd")
    else:
        return render(request,'classroom/createtest.html',{'clscode':clscode})