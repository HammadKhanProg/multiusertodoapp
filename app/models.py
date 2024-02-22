from django.db import models
from django.contrib.auth.models import User
class Todo (models.Model):
    status_choices=[
        ("complete","completed"),
        ("pending","pending")
    ]
    title=models.CharField(max_length=200)
    status=models.CharField(max_length=50,choices=status_choices)
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.title
# Create your models here.
