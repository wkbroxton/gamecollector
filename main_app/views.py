from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import os
import uuid
import boto3
from .models import Game, Accessory, Photo
from .forms import PlayForm

# Create your views here.

# Define the home view
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

@login_required
def games_index(request):
  games = Game.objects.all()
  return render(request, 'games/index.html', { 'games': games })

@login_required
def games_detail(request, game_id):
  game = Game.objects.get(id=game_id)
  accessories_game_doesnt_have = Accessory.objects.exclude(id__in=game.accessories.all().values_list('id'))
  play_form = PlayForm()
  return render(request, 'games/detail.html', { 
    'game': game, 
    'play_form': play_form,
    'accessories': accessories_game_doesnt_have 
  })
  
class GameCreate(CreateView):
  model = Game
  fields = ['name', 'console', 'description', 'year']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class GameUpdate(UpdateView):
  model = Game
  fields = ['name', 'console', 'description', 'year']

class GameDelete(DeleteView):
  model = Game
  success_url = '/games/'

@login_required 
def add_play(request, game_id):
  form = PlayForm(request.POST)
  if form.is_valid():
    new_play = form.save(commit=False)
    new_play.game_id = game_id
    new_play.save()
  return redirect('detail', game_id=game_id)

class AccessoryList(ListView, LoginRequiredMixin):
  model = Accessory

class AccessoryDetail(DetailView, LoginRequiredMixin):
  model = Accessory

class AccessoryCreate(CreateView, LoginRequiredMixin):
  model = Accessory
  fields = '__all__'

class AccessoryUpdate(UpdateView, LoginRequiredMixin):
  model = Accessory
  fields = ['name', 'color']

class AccessoryDelete(DeleteView, LoginRequiredMixin):
  model = Accessory
  success_url = '/accessories/'

@login_required
def assoc_accessory(request, game_id, accessory_id):
  Game.objects.get(id=game_id).accessories.add(accessory_id)
  return redirect('detail', game_id=game_id)

@login_required
def unassoc_accessory(request, game_id, accessory_id):
  Game.objects.get(id=game_id).accessories.remove(accessory_id)
  return redirect('detail', game_id=game_id)

@login_required
def add_photo(request, game_id):
  #the form's input will have a name of photo-file
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
    try:
      bucket = os.environ['S3_BUCKET']
      s3.upload_fileobj(photo_file, bucket, key)
      # build the full url sting
      url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
      Photo.objects.create(url=url, game_id=game_id)
    except Exception as e:
      print('An error occured uploading file to S3', e)
  return redirect('detail', game_id=game_id)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      # Automatically log in the user
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)