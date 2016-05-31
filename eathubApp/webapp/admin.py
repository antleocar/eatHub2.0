from django.contrib import admin

# Register your models here.

from .models import Tastes, Comment, Step, Following

admin.site.register(Tastes)
admin.site.register(Comment)
admin.site.register(Step)
admin.site.register(Following)
