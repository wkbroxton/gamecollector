from django.contrib import admin
# add Feeding to the import
from .models import Game, Play

admin.site.register(Game)
# register the new Feeding Model 
admin.site.register(Play)