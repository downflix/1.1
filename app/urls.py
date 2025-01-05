from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name = "index"),
    path('fetch-videos/', views.fetch_videos, name='fetch_videos'),
    path("terms/",views.terms,name = "terms"),
    path("copy/",views.copy,name = "copy"),
    path("privacy/",views.privacy,name="privacy"),
]