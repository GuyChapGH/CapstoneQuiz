import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse

from django.shortcuts import render
from django.urls import reverse

from .models import User
from .models import Question
from .models import Quiz
from .models import Contestant

from .forms import QuestionCreateForm, QuizCreateForm, ContestantSelectForm, ResultsSelectForm


# Create your views here.


def index(request):
    return render(request, "capstone/index.html")


@login_required
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


@login_required
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


@login_required
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


@login_required
def play_quiz(request, contestant_id):
    try:
        contestant = Contestant.objects.get(pk=contestant_id)
    except Contestant.DoesNotExist:
        raise Http404("Contestant not found.")

    # index, n, controls question in quiz. n=0 is first question and n=N-1 is last question
    n = 0

    # question uses method defined in Contestant model
    question = contestant.question(n)

    # multiple_choice uses method defined  in Contestant model
    multiple_choice0 = contestant.multiple_choice0(n)

    # multiple_choice uses method defined  in Contestant model
    multiple_choice1 = contestant.multiple_choice1(n)

    # multiple_choice uses method defined  in Contestant model
    multiple_choice2 = contestant.multiple_choice2(n)

    # multiple_choice uses method defined  in Contestant model
    multiple_choice3 = contestant.multiple_choice3(n)

    # first_correct_answer uses method defined in Contestant model
    correct_answer = contestant.correct_answer(n)

    # number of questions in quiz uses method defined in Contestant model
    number_questions = contestant.questions_in_quiz()

    return render(request, "capstone/play_quiz.html",   {
        "contestant_id": contestant_id,
        "contestant": contestant,
        "question": question,
        "multiple_choice0": multiple_choice0,
        "multiple_choice1": multiple_choice1,
        "multiple_choice2": multiple_choice2,
        "multiple_choice3": multiple_choice3,
        "correct_answer": correct_answer,
        "number_questions": number_questions
    })


@login_required
def play_quizAPI(request, contestant_id):
    try:
        contestant = Contestant.objects.get(pk=contestant_id)
    except Contestant.DoesNotExist:
        raise Http404("Contestant not found.")

# Update quiz_score and supply index n
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("question_index") is not None:
            # this makes the variable, n, accessible
            global n
            n = data["question_index"]
            return JsonResponse({"message": "index successfully updated."})
        # return JsonResponse({"question": "Got this far"})
        if data.get("score_point") is True:
            contestant.score_point()
            contestant.save()
            return JsonResponse({"message": "quiz_score successfully updated."})

# Return question and answers with index n. Return quiz_score.
    if request.method == "GET":
        return JsonResponse({"question": contestant.question(n),
                             "multiple_choice0": contestant.multiple_choice0(n),
                             "multiple_choice1": contestant.multiple_choice1(n),
                             "multiple_choice2": contestant.multiple_choice2(n),
                             "multiple_choice3": contestant.multiple_choice3(n),
                             "correct_answer": contestant.correct_answer(n),
                             "quiz_score": contestant.q_score()
                             })


@login_required
def results_select(request):
    if request.method == 'POST':

        # Get form quiz_input
        form = ResultsSelectForm(request.POST)
        # Check form validation
        if form.is_valid():
            # Get quiz object from form. And capture quiz_id.
            quiz_id = form.cleaned_data['quiz'].id

            # Redirect to results_display html page with quiz_id
            return HttpResponseRedirect(reverse("results_display", args=(quiz_id,)))

        else:
            # Return part completed form
            return render(request, "capstone/results_select.html",  {
                "form": form
            })

    else:
        # Return fresh form
        return render(request, "capstone/results_select.html", {
            "form": ResultsSelectForm()
        })


@login_required
def results_display(request, quiz_id):
    # Get all contestant objects for given quiz_id, order by timestamp and take the five most recent.
    try:
        queryset = Contestant.objects.all().filter(quiz__id=quiz_id).order_by('-timestamp')[:5]
    except queryset.DoesNotExist:
        raise Http404("Quiz results not found.")
    # Get quiz name for given quiz_id
    quiz_name = Quiz.objects.all().filter(id=quiz_id).first()

    return render(request, "capstone/results_display.html", {
        "quiz_id": quiz_id,
        "quiz_name": quiz_name,
        "queryset": queryset
    })


@login_required
def results_displayAPI(request, quiz_id):

    if request.method == "GET":
        # Get all contestant objects for given quiz_id, order by timestamp and take the five most recent.
        try:
            queryset = Contestant.objects.all().filter(quiz__id=quiz_id).order_by('-timestamp')[:5]
        except queryset.DoesNotExist:
            raise Http404("Quiz results not found.")

        # Create empty lists for graph labels and data
        labels = []
        data = []

        # Populate lists with values from queryset
        for entry in queryset:
            labels.append(entry.user.username)
            data.append(entry.quiz_score)

        return JsonResponse({
            "labels": labels,
            "data": data
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
