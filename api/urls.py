from django.urls import path
from . import views
from . import service
import asyncio

urlpatterns = [
    path('', views.GetVideosfromDB.as_view()),
    path('submit_key', views.save_key)
]

service.THREAD.start()
