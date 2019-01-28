from django.contrib import admin
from django.urls import path

from persons import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.PersonListView.as_view(), name="person_full"),
]
