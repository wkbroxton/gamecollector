from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

# Create your models here.

TIMES = (
    ('M', 'Morning'),
    ('A', 'Afternoon'),
    ('E', 'Evening')
)
# new code above

class Accessory(models.Model):
  name = models.CharField(max_length=50)
  color = models.CharField(max_length=20)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('accessories_detail', kwargs={'pk': self.id})

class Game(models.Model):
  name = models.CharField(max_length=100)
  console = models.CharField(max_length=100)
  description = models.TextField(max_length=250)
  year = models.IntegerField()
  accessories = models.ManyToManyField(Accessory)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.name
  
    # Add this method
  def get_absolute_url(self):
    return reverse('detail', kwargs={'game_id': self.id})
  
  def played_for_today(self):
    return self.play_set.filter(date=date.today()).count() >= len(TIMES)

class Play(models.Model):
  date = models.DateField('Date Played')
  time = models.CharField('Time of Day Played',
    max_length=1,
    choices=TIMES,
    default=TIMES[0][0])
  
  game = models.ForeignKey(Game, on_delete=models.CASCADE)

  def __str__(self):
    return f"{self.get_time_display()} on {self.date}"

  class Meta:
    ordering = ['-date']

class Photo(models.Model):
  url = models.CharField(max_length=200)
  cat = models.ForeignKey(Game, on_delete=models.CASCADE)

  def __str__(self):
    return f"Photo for cat_id: {self.cat_id} @{self.url}"