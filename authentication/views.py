from django.shortcuts import render,redirect    
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.


def loginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request,user)
            return redirect('index')
        else:
            return render(request, 'login.html', {'error':"Invalid UserName or Password"})
    else:
        return render(request, 'login.html', {})
@login_required
def logoutView(request):
    logout(request)
    return redirect('index')

def registerView(request):
    if request.method=="POST":
        try:
            username=request.POST['username']
            password1=request.POST['password1']
            password2=request.POST['password2']
            firstname=request.POST['firstname']
            lastname=request.POST['lastname']
            email=request.POST['email']
        except:
            return render(request,'register.html',{'msg':"Fill All The Fields"})
        if email and User.objects.filter(email=email).count() > 0:
            return render(request, 'register.html', { 'msg': "Email Already Exists" })
        if password1 != password2:
            return render(request, 'register.html', { 'msg': "Passwords not matching" })
        try:
            user = User.objects.create_user(
                username = username,
                first_name = firstname,
                last_name = lastname,
                email = email,
                password = password1
            )
            user.save()
        except:
            return render(request, 'register.html', { 'msg': "Username already exists" })
        user = authenticate(request, username=username, password=password1)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'register.html', { 'msg': "User created Successfully" })
    else:
        return render(request, 'register.html')

