from django.urls import path
from . import views
from . import admin_views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
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
    
    # Admin routes
    path('admin-login/', admin_views.admin_login_view, name='admin_login'),
    path('admin-dashboard/', admin_views.admin_dashboard, name='admin_dashboard'),
    path('admin-users/', admin_views.admin_users, name='admin_users'),
    path('admin-detections/', admin_views.admin_detections, name='admin_detections'),
    path('admin-exercises/', admin_views.admin_exercises, name='admin_exercises'),
    path('admin-logout/', admin_views.admin_logout, name='admin_logout'),
]
