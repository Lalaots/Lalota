from django import forms
from . import models

class CreateHuman(forms.ModelForm):
    class Meta:
        model = models.Human
        fields = ['name','age']