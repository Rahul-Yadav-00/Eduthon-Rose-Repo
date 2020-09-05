from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate ,login,logout

# Create your views here.
def index(request):
    if(request.user.is_authenticated):
        return render(request,'user/index.html')
    else:
        return redirect('signin')

def signin(request):
    if(request.user.is_authenticated == False):
        if(request.method == 'POST'):
            username = request.POST['username']
            if(User.objects.filter(username = username).exists()):
                password = request.POST['userPassword']
                user = authenticate(username=username,password=password)
                if user is not None:
                    login(request,user)
                    messages.success(request,'login successful')
                else:
                    messages.error(request,'invalid credentials')
                    return redirect('signin')
        else:
            return render(request,'user/signin.html')
    else:
        return HttpResponse('user is already signin')

def signup(request):
    if(request.method == 'POST'):
        username = request.POST['username']
        if(User.objects.filter(username=username).exists()):
            messages.error(request,'this username is already taken')
            return redirect('signup')
        else:
            email = request.POST['email']
            if(User.objects.filter(email=email).exists()):
                messages.error(request,'this email is already registered')
                return redirect('signin')
            else:
                password = request.POST['userpassword']
                cpassword = request.POST['userconfirmpassword']
                if(password != cpassword):
                    messages.error(request,'your passwords are not matching')
                    return redirect('signup')
                else:
                    if len(username) > 15:
                        messages.error(request, 'Username is very large')
                        return redirect('signup')
                    else:
                        myuser = User.objects.create_user(username = username,email = email,
                                                            password = password)
                        messages.success(request, 'Your Nature Window account is created')
                        return  redirect('signin')
    else:
        return render(request,'user/signin.html')

@login_required(login_url='signin')
def signout(request):
    logout(request)
    messages.success(request,'Successfully Logout')
    return redirect('signin')
