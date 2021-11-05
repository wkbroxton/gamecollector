from django.shortcuts import render
# Add the following import
from django.views.generic.edit import CreateView, UpdateView, DeleteView
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
  return render(request, 'games/detail.html', { 'game': game })

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