from django.contrib import admin

# Register your models here.

from .models import Tastes, Comment, Step, Recipe, Cook, Vote, Savour

admin.site.register(Tastes)
admin.site.register(Comment)
admin.site.register(Step)
admin.site.register(Recipe)
admin.site.register(Cook)
admin.site.register(Vote)
admin.site.register(Savour)
