from django.db import models
from django.urls import reverse

# Create your models here.

class Game(models.Model):
  name = models.CharField(max_length=100)
  console = models.CharField(max_length=100)
  description = models.TextField(max_length=250)
  year = models.IntegerField()

  def __str__(self):
    return self.name
  
    # Add this method
  def get_absolute_url(self):
    return reverse('detail', kwargs={'game_id': self.id})