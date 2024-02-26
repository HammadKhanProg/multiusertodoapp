from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from app.models import Todo
from .forms import todoform

from rest_framework.response import Response
from .serializer import todoserializer
from django.core.paginator import Paginator
# user Authentication and authorization

def signup (request):
    if request.method=="GET":
        form=UserCreationForm()
        data={
            "form":form
        }
        return render (request,"signup.html",data)
    else:
        form=UserCreationForm(data=request.POST)
        data={
                "form":form
            }
        if form.is_valid:
            form.save()
            return redirect ("home")
        else:
            return render(request,"signup.html",data)
        
def signin (request):
    if request.method=="GET":
        form=AuthenticationForm()
        data={
            "form":form
        }
        return render (request,"signin.html",data)
    else:
        form=AuthenticationForm(data=request.POST)
        data={
            "form":form
        }
        if form.is_valid():
            username=form.cleaned_data.get("username")
            password=form.cleaned_data.get("password")
            user=authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect("home")
            else:
                return render (request,"signin.html",data)
        else:
            return render (request,"signin.html",data)
        
def signout (request):
    logout(request)
    return redirect ("signin")


# Todo Area

@login_required(login_url="signin")        
def home (request):
    if request.method=="GET":
        if request.user.is_authenticated:
            user=request.user
            tasks=Todo.objects.filter(user=user)
            paginator=Paginator(tasks,3)
            page_no=request.GET.get("page")
            tastfinal=paginator.get_page(page_no)
            form=todoform()
            data={
                "form":form,
                "tasks":tastfinal
                }
            return render (request,"home.html",data)
    else:
        if request.user.is_authenticated:
            user=request.user
            st=request.POST.get("ui")
            tasks=Todo.objects.filter(user=user,title__icontains=st)
            form=todoform()
            data={
                "form":form,
                "tasks":tasks
                }
            return render (request,"home.html",data)
def add_todo (request):
    if request.user.is_authenticated:
        user=request.user
        form=todoform(request.POST)
        data={
            "form":form
        }
        if form.is_valid():
            todo=form.save(commit=False)
            todo.user=user
            todo.save()
            print(form.cleaned_data)
            return redirect ("home")
        else:
            return render (request,"home.html",data)   
def update (request,pk):
    if request.method=="GET":
        task=Todo.objects.get(id=pk)
        form = todoform(instance=task)
        data={
            "form":form
        }
        return render(request,"update.html",data)
    else:
        task=Todo.objects.get(id=pk)
        form = todoform(request.POST,instance=task)
        if form.is_valid():
            form.save()
            return redirect("home")
    return render(request,"update.html",data)
def delete (request,pk):
    task=Todo.objects.get(id=pk)
    task.delete()
    return redirect ("home")

def admin (request):
    if request.user.is_authenticated:
        user=request.user
        if user.is_superuser:
            users=User.objects.all()
            data={
                "users":users
            }
            return render(request,'adminpanel.html',data)
        else:
            redirect ('home')




# Rest api area
from rest_framework.views import APIView
from rest_framework import generics,permissions
from rest_framework.authentication import BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated,BasePermission,IsAdminUser
from django.contrib.auth.models import User
from .serializer import userserializer

class writebyuseronly (BasePermission):
    def has_permission(self, request, view):
        user=request.user
        if request.method=="GET":
            return True
        if request.method=="RETRIEVE" or request.method=="PUT" or request.method=="DELETE":
            if user.is_superuser:
                return True
        return False

class todolist (generics.ListCreateAPIView):
    serializer_class=todoserializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class tododetaillist (generics.RetrieveUpdateDestroyAPIView):
    queryset=Todo.objects.all()
    serializer_class=todoserializer
    permission_classes = [IsAdminUser,IsAuthenticated,writebyuseronly]


class users_signup (generics.ListCreateAPIView):
    queryset=User.objects.all()
    serializer_class=userserializer

class users_detail_signup (generics.RetrieveUpdateDestroyAPIView):
    queryset=User.objects.all()
    serializer_class=userserializer


    