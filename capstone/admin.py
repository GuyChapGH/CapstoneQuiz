from django.contrib import admin

from .models import Question, Quiz

# Register your models here.

admin.site.register(Question)
admin.site.register(Quiz)