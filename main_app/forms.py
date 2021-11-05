from django.forms import ModelForm
from .models import Playing

class PlayingForm(ModelForm):
  class Meta:
    model = Playing
    fields = ['date', 'played']