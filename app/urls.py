from django.urls import path
from .views import Home,Base

urlpatterns = [
    path('',Home.as_view(),name='home'),
    path('',Base.as_view(),name='home'),

]