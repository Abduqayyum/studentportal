from atexit import register
import re
from django.contrib import admin
from .models import Notes, Homework, Todo

# Register your models here.
admin.site.register(Notes)
admin.site.register(Homework)
admin.site.register(Todo)