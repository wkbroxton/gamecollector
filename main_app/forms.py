from django.forms import ModelForm
from .models import Play

class PlayForm(ModelForm):
  class Meta:
    model = Play
    fields = ['date', 'time']