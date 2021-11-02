from django.contrib import admin

## import your models here
from .models import Game

# Register your models here
admin.site.register(Game)