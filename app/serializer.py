from rest_framework import serializers
from app.models import Todo
class todoserializer (serializers.ModelSerializer):
    class Meta:
        model=Todo
        fields="__all__"