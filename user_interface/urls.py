from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('upload/', views.upload_data, name='upload_data'),
    path('analyze/', views.analyze_samples, name='analyze_samples'),
    path('detection/', views.detection_results, name='detection_results'),
    path('training/', views.training_exercises, name='training_exercises'),
    path('exercise/<uuid:exercise_id>/', views.start_exercise, name='start_exercise'),
    path('progress/', views.progress_reports, name='progress_reports'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    
    # API endpoints
    path('api/upload/handwriting/', views.upload_handwriting_api, name='upload_handwriting_api'),
    path('api/upload/speech/', views.upload_speech_api, name='upload_speech_api'),
]
