from rest_framework import serializers
from django.contrib.auth.models import User
from app.models import Todo
class todoserializer (serializers.ModelSerializer):
    class Meta:
        model=Todo
        fields="__all__"

class userserializer (serializers.ModelSerializer):
    class Meta:
        model=User
        fields="__all__"