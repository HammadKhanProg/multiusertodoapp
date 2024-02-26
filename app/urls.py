from django.urls import path
from app.views import signup,home,signin,signout,add_todo,update,delete,todolist,admin,tododetaillist,users_signup,users_detail_signup
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    
    path("signup/",signup,name="signup"),
    path('',home,name="home"),
    path('adm/',admin,name="adm"),
    path("signin/",signin,name="signin"),
    path("signout/",signout,name="signout"),
    path("add_todo/",add_todo,name="add_todo"),
    path("update/<pk>",update,name="update"),
    path("delete/<pk>",delete,name="delete"),

    path('api/todolist/',todolist.as_view()),
    path('api/todolist/<pk>',tododetaillist.as_view()),

    path('api/signup/',users_signup.as_view()),
    path('api/signup/<pk>',users_detail_signup.as_view()),
    
    path("auth/login/",TokenObtainPairView.as_view()),
    path("auth/login/refresh/",TokenRefreshView.as_view())

]
