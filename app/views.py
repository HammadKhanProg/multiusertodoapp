from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from app.models import Todo
from .forms import todoform

from rest_framework.response import Response
from .serializer import todoserializer

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
    if request.user.is_authenticated:
        user=request.user
        tasks=Todo.objects.filter(user=user)
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
    task=Todo.objects.get(id=pk)
    form = todoform(instance=task)
    data={
        "form":form
    }
    return render(request,"update.html",data)
def delete (request,pk):
    task=Todo.objects.get(id=pk)
    task.delete()
    return redirect ("home")


# Rest api area
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.authentication import BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated,BasePermission

class writebyadminonly (BasePermission):
    def has_permission(self, request, view):
        user=request.user
        if request.method=="GET":
            return True
        if request.method=="POST" or request.method=="PUT" or request.method=="DELETE":
            if user.is_superuser:
                return True
        return False

class todolist (generics.ListCreateAPIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    queryset=Todo.objects.all()
    serializer_class=todoserializer

class tododetaillist (generics.RetrieveUpdateDestroyAPIView):
    queryset=Todo.objects.all()
    serializer_class=todoserializer



    