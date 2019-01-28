from django.contrib import admin
from .models import Person, Document

admin.site.register(Person)  # Register User model to Django Admin.
admin.site.register(Document)  # Register Document model to Django Admin.