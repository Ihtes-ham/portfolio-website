from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/chat/', views.ai_chat, name='ai_chat'),
    path('api/analyze-cv/', views.analyze_cv, name='analyze_cv'),
]