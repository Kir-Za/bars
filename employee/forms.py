from django import forms
from .models import Quest, Candidate


class CreateCandForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['name', 'age', 'email', 'planet', 'exame']


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['answers']
