from django.urls import path     
from . import views

urlpatterns = [
    path('', views.index ),
    path('login', views.login),
    path('dashboard', views.dashboard),
    path('blast', views.blast),
    path('logout', views.logout),
]