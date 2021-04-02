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
    answer1 = models.CharField(max_length=30)
    answer2 = models.CharField(max_length=30)
    answer3 = models.CharField(max_length=30)
    correct_answer = models.CharField(max_length=30, default="unanswered")

    def __str__(self):
        return f"{self.user.username} at {self.timestamp}. Question: {self.content} with answers: {self.answer0}, {self.answer1}, {self.answer2}, {self.answer3}. Correct answer: {self.correct_answer}"


class Quiz(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="quiz_master")
    timestamp = models.DateTimeField(auto_now_add=True)
    quiz_name = models.CharField(max_length=30, unique=True)
    questions = models.ManyToManyField("Question")

    def __str__(self):
        first_question = self.questions.all().first()
        return f"{self.user.username} at {self.timestamp}. Quizname: {self.quiz_name}. First question: {first_question.content}"
