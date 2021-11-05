from django.db import models
from django.urls import reverse

# Create your models here.

TIMES = (
    ('M', 'Morning'),
    ('A', 'Afternoon'),
    ('E', 'Evening')
)
# new code above

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

class Play(models.Model):
  date = models.DateField()
  time = models.CharField(
    max_length=1,
    # add the 'choices' field option
    choices=TIMES,
    # set the default value for meal to be 'B'
    default=TIMES[0][0]
  )

  game = models.ForeignKey(Game, on_delete=models.CASCADE)

  def __str__(self):
    # Nice method for obtaining the friendly value of a Field.choice
    return f"{self.get_time_display()} on {self.date}"

