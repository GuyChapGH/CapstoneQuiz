from django import forms
from .models import Question


CHOICES = [('answer0', 'Answer A'), ('answer1', 'Answer B'),
           ('answer2', 'Answer C'), ('answer3', 'Answer D')]


class QuestionCreateForm(forms.ModelForm):
    correct_answer = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())

    class Meta:
        model = Question
        exclude = ['user', 'timestamp']
        labels = {
            "content": "Question",
            "answer0": "Answer A",
            "answer1": "Answer B",
            "answer2": "Answer C",
            "answer3": "Answer D",
        }
