from django.urls import path
from . import views

urlpatterns = [
    path('', views.main),
    path('geography',views.geography),
    path('needable',views.needable),
    path('skills',views.skills),
    path('vacancies',views.vacancies)
]
