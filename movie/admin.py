from django.contrib import admin
from movie.models import *
# Register your models here.
admin.site.register(Movies)
admin.site.register(Comment)