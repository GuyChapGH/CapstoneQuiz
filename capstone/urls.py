from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create_question/", views.create_question, name="create_question"),
    path("create_quiz/", views.create_quiz, name="create_quiz"),
    path("quiz_select/", views.quiz_select, name="quiz_select"),
    path("play_quiz/<int:contestant_id>", views.play_quiz, name="play_quiz"),
    path("results_select/", views.results_select, name="results_select"),
    path("results_display/<int:quiz_id>", views.results_display, name="results_display"),

    # API Routes
    path("play_quizAPI/<int:contestant_id>", views.play_quizAPI, name="play_quizAPI"),

    # User paths
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
