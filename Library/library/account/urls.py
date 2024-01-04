from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('history', views.history, name='history'),
    path('security', views.security, name='security'),
    path('save_profile_changes', views.save_profile_changes, name='save_profile_changes'),
    path('save_security_changes', views.save_security_changes, name='save_security_changes'),



]