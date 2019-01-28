from django.contrib import admin
from django.urls import path

from persons import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.PersonListView.as_view(), name="person_full"),
    path('persons/person_id_<int:pk>/', views.PersonDetailView.as_view(),
         name="person_detail"),
]
