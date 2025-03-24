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

#    def __str__(self):
#        return f"{self.user.username} at {self.timestamp}. Question: {self.content} with answers: {self.answer0}, {self.answer1}, {self.answer2}, {self.answer3}. Correct answer: {self.correct_answer}"

    def __str__(self):
        return f"Question: {self.content}"


class Quiz(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="quiz_master")
    timestamp = models.DateTimeField(auto_now_add=True)
    quiz_name = models.CharField(max_length=30, unique=True)
    questions = models.ManyToManyField("Question")

    def __str__(self):
        # first_question = self.questions.all().first()
        # return f"{self.user.username} at {self.timestamp}. Quizname: {self.quiz_name}. First question: {first_question.content}"
        return f"{self.quiz_name}"


class Contest(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="contestant")
    timestamp = models.DateTimeField(auto_now_add=True)
    quiz = models.ForeignKey("Quiz", on_delete=models.CASCADE)
    quiz_score = models.IntegerField(default=0)

    def __str__(self):
        timestamp = self.timestamp.strftime("%b %-d %Y, %-I:%M %p")
        return f"{self.user.username} at {timestamp}. Quizname: {self.quiz.quiz_name}."
    # return f"{self.user.username}. Quizname: {first_quiz.quiz_name}"

    def question(self, n):
        question = self.quiz.questions.all()[n]
        return f"{question.content}"

    def multiple_choice0(self, n):
        question = self.quiz.questions.all()[n]
        return f"{question.answer0}"

    def multiple_choice1(self, n):
        question = self.quiz.questions.all()[n]
        return f"{question.answer1}"

    def multiple_choice2(self, n):
        question = self.quiz.questions.all()[n]
        return f"{question.answer2}"

    def multiple_choice3(self, n):
        question = self.quiz.questions.all()[n]
        return f"{question.answer3}"

    def correct_answer(self, n):
        question = self.quiz.questions.all()[n]
        return f"{question.correct_answer}"

    def questions_in_quiz(self):
        number_questions = self.quiz.questions.count()
        return f"{number_questions}"

    def score_point(self):
        self.quiz_score += 1

    def q_score(self):
        return f"{self.quiz_score}"
