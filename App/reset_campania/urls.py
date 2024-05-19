from django.urls import path
from App.reset_campania import views

urlpatterns = [
    path('', views.vista_reset, name = "reset"),
    path('reset_campania/', views.reset_campania, name = "reset_campania")
]
