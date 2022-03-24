import email
import imp
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
# Create your views here.
def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        firstname = request.POST['first_name']
        lastname = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        confirmpassword = request.POST['cpassword']
        
        if password == confirmpassword:
            if User.objects.filter(username=username).exists():
                return redirect('index')
            else:
                user = User.objects.create_user(first_name=firstname, last_name=lastname,email=email,username=username,password=password)
                user.save()
                messages.info(request,'signup successfully')
                return redirect('login_page')
        else:
            return redirect('index')
    else:
        return redirect('index')
        

def login_page(request):
    return render(request,'login.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username,password=password)
        
        if user is not None:
            auth.login(request, user)
            messages.info(request,'logged in successfully')
            return redirect('gallery')
        else:
            messages.info(request,'Incorect password or user name')
            return redirect('login_page')
    else:
        return redirect('login_page')

@login_required(login_url='login_page')
def gallery(request):
    
    return render(request, 'gallery.html')
    

def logout(request):
    auth.logout(request)
    messages.info(request,'logged out successfully')
    return redirect('login_page')

def reg(request):
    return render(request, 'reg.html')

def imageregister(request):
    if request.method == 'POST':
        fullname=request.POST['firstname']
        secondname=request.POST['secondname']
        email=request.POST['email']
        image = request.FILES['image']
        upload = Upload_image(image=image,fullname=fullname,secondname=secondname,email=email)
        upload.save()
        return redirect('imageshow')
    
def imageshow(request):
    empty = Upload_image.objects.all()
    return render(request, 'imageshow.html', {'empty':empty})

def delete(request,imgid):
    employees=Upload_image.objects.get(imgid=imgid)
    employees.delete()
    return redirect('imageshow')

def edit(request,imgid):
    employees=Upload_image.objects.get(imgid=imgid)
    return render(request, 'edit.html',{'imgs':employees})

def update(request,imgid):
    if request.method == 'POST':
        employees=Upload_image.objects.get(imgid=imgid)
        employees.fullname=request.POST.get('fullname',employees.fullname)
        employees.secondname=request.POST.get('secondname',employees.secondname)
        employees.email=request.POST.get('email',employees.email)
        employees.image = request.FILES.get('image',employees.image)
        employees.save()
        return redirect('imageshow')

