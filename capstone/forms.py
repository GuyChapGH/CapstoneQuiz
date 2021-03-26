from django import forms
from .models import Question


class QuestionCreateForm(forms.ModelForm):
    class Meta:
        model = Question
        exclude = ['user', 'timestamp']
