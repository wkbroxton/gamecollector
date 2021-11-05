from django.shortcuts import render, redirect
# Add the following import
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from main_app.forms import PlayForm
from .models import Game

# Create your views here.

# Define the home view
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def games_index(request):
  games = Game.objects.all()
  return render(request, 'games/index.html', { 'games': games })

def games_detail(request, game_id):
  game = Game.objects.get(id=game_id)
  play_form = PlayForm
  return render(request, 'games/detail.html', { 
    'game': game, 'play_form': play_form })
  
def add_play(request, game_id):
# create a ModelForm instance using the data in request.POST
  form = PlayForm(request.POST)
  # validate the form
  if form.is_valid():
    new_play = form.save(commit=False)
    new_play.game_id = game_id
    new_play.save()
  return redirect('detail', game_id=game_id)

class GameCreate(CreateView):
  model = Game
  fields = ['name', 'console', 'description', 'year']
  success_url = '/games/'

class GameUpdate(UpdateView):
  model = Game
  # Let's disallow the renaming of a cat by excluding the name field!
  fields = ['name', 'console', 'description', 'year']

class GameDelete(DeleteView):
  model = Game
  success_url = '/games/'