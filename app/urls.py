from django.urls import path
from app.views import signup,home,signin,signout,add_todo,update,delete,todolist,tododetaillist
from rest_framework.authtoken.views import ObtainAuthToken
urlpatterns = [
    path("signup/",signup,name="signup"),
    path('',home,name="home"),
    path("signin/",signin,name="signin"),
    path("signout/",signout,name="signout"),
    path("add_todo/",add_todo,name="add_todo"),
    path("update/<pk>",update,name="update"),
    path("delete/<pk>",delete,name="delete"),

    path('api/todolist/',todolist.as_view()),
    path('api/todolist/<pk>',tododetaillist.as_view()),

    path("auth/login/",ObtainAuthToken.as_view())
]
