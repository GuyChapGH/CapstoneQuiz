from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User
from .models import Question
from .models import Contestant

from .forms import QuestionCreateForm, QuizCreateForm, ContestantSelectForm


# Create your views here.


def index(request):
    return render(request, "capstone/index.html")


def create_question(request):
    if request.method == 'POST':

        # Get form input
        form = QuestionCreateForm(request.POST)

        # Check all fields correct, complete user field with current user and save
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return HttpResponseRedirect(reverse("create_question"))
        else:
            # Add last saved question to bottom of form and return part completed form
            question_last = Question.objects.all().last()
            return render(request, "capstone/create_question.html", {
                "form": form,
                "question_last": question_last
            })
    else:
        # Add last saved question to bottom of form and return fresh form
        question_last = Question.objects.all().last()
        return render(request, "capstone/create_question.html", {
            "form": QuestionCreateForm(),
            "question_last": question_last
        })


def create_quiz(request):
    if request.method == 'POST':

        # Get form input
        form = QuizCreateForm(request.POST)

        # Check all fields correct, complete user field with current user and save
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return HttpResponseRedirect(reverse("create_quiz"))
        else:
            # return part completed form
            return render(request, "capstone/create_quiz.html", {
                "form": form
            })
    else:
        # return fresh form
        return render(request, "capstone/create_quiz.html", {
            "form": QuizCreateForm()
        })


def quiz_select(request):
    if request.method == 'POST':

        # Get form input
        form = ContestantSelectForm(request.POST)

        # Check all fields correct, complete user field with current user and save
        if form.is_valid():
            form.instance.user = request.user
            form.save()

            # Get id from last created Contestant object
            contestant_id = Contestant.objects.all().last().id
            return HttpResponseRedirect(reverse("play_quiz", args=(contestant_id,)))
        else:
            # return part completed form
            return render(request, "capstone/quiz_select.html", {
                "form": form
            })
    else:
        # return fresh form
        return render(request, "capstone/quiz_select.html", {
            "form": ContestantSelectForm()
        })


def play_quiz(request, contestant_id):

    try:
        contestant = Contestant.objects.get(pk=contestant_id)
    except Contestant.DoesNotExist:
        raise Http404("Contestant not found.")

    # first_question uses method defined in Contestant model
    first_question = contestant.first_question()

    # first_correct_answer uses method defined in Contestant model
    first_correct_answer = contestant.first_correct_answer()

    return render(request, "capstone/play_quiz.html",   {
        "contestant": contestant,
        "first_question": first_question,
        "first_correct_answer": first_correct_answer
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "capstone/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "capstone/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "capstone/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "capstone/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "capstone/register.html")
