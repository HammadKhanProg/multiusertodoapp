from django.forms import ModelForm
from app.models import Todo

class todoform (ModelForm):
    class Meta:
        model=Todo
        fields=["title","status"]