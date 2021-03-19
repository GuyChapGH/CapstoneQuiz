from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    pass


class Question(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="setter")
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    answer0 = models.CharField(max_length=30)
    answer0_bool = models.BooleanField()
    answer1 = models.CharField(max_length=30)
    answer1_bool = models.BooleanField()
    answer2 = models.CharField(max_length=30)
    answer2_bool = models.BooleanField()
    answer3 = models.CharField(max_length=30)
    answer3_bool = models.BooleanField()

    def __str__(self):
        return f"{self.user.username} at {self.timestamp}. Question: {self.content} with answers: {self.answer0}, {self.answer0_bool}, {self.answer1}, {self.answer1_bool}, {self.answer2}, {self.answer2_bool}, {self.answer3}, {self.answer3_bool}"
