from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Count, Avg, Q
from datetime import datetime, timedelta

from data_collection.models import UserProfile, HandwritingSample, SpeechSample, VideoSample
from detection_module.models import DetectionResult
from training_module.models import Exercise, UserProgress, ExerciseSession, ProgressReport


def is_admin(user):
    """Check if user is admin/superuser"""
    return user.is_authenticated and (user.is_staff or user.is_superuser)


def admin_login_view(request):
    """Admin login page"""
    if request.user.is_authenticated and is_admin(request.user):
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_staff or user.is_superuser:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'You do not have admin privileges.')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'user_interface/admin_login.html')


@login_required
@user_passes_test(is_admin, login_url='admin_login')
def admin_dashboard(request):
    """Admin dashboard with comprehensive statistics"""
    
    # User Statistics
    total_users = User.objects.filter(is_staff=False, is_superuser=False).count()
    active_users_30days = User.objects.filter(
        last_login__gte=datetime.now() - timedelta(days=30),
        is_staff=False,
        is_superuser=False
    ).count()
    new_users_7days = User.objects.filter(
        date_joined__gte=datetime.now() - timedelta(days=7),
        is_staff=False,
        is_superuser=False
    ).count()
    
    # Sample Statistics
    total_handwriting_samples = HandwritingSample.objects.count()
    total_speech_samples = SpeechSample.objects.count()
    total_video_samples = VideoSample.objects.count()
    samples_today = HandwritingSample.objects.filter(
        timestamp__date=datetime.now().date()
    ).count() + SpeechSample.objects.filter(
        timestamp__date=datetime.now().date()
    ).count()
    
    # Detection Statistics
    total_detections = DetectionResult.objects.count()
    detections_today = DetectionResult.objects.filter(
        detection_timestamp__date=datetime.now().date()
    ).count()
    
    # Risk Level Distribution
    risk_distribution = DetectionResult.objects.values('risk_level').annotate(
        count=Count('id')
    ).order_by('risk_level')
    
    high_risk_count = DetectionResult.objects.filter(risk_level='high').count()
    low_risk_count = DetectionResult.objects.filter(risk_level='low').count()
    
    # Average probabilities
    avg_dyslexia_prob = DetectionResult.objects.aggregate(
        avg=Avg('dyslexia_probability')
    )['avg'] or 0
    avg_dysgraphia_prob = DetectionResult.objects.aggregate(
        avg=Avg('dysgraphia_probability')
    )['avg'] or 0
    
    # Training Statistics
    total_exercises = Exercise.objects.filter(is_active=True).count()
    total_sessions = ExerciseSession.objects.count()
    sessions_today = ExerciseSession.objects.filter(
        start_time__date=datetime.now().date()
    ).count()
    
    avg_session_score = ExerciseSession.objects.aggregate(
        avg=Avg('score')
    )['avg'] or 0
    
    # Exercise type distribution
    exercise_type_stats = Exercise.objects.filter(is_active=True).values(
        'exercise_type'
    ).annotate(count=Count('id'))
    
    # Recent Activity
    recent_users = User.objects.filter(
        is_staff=False, is_superuser=False
    ).order_by('-date_joined')[:10]
    
    recent_detections = DetectionResult.objects.select_related(
        'user', 'handwriting_sample', 'speech_sample'
    ).order_by('-detection_timestamp')[:10]
    
    recent_sessions = ExerciseSession.objects.select_related(
        'user', 'exercise'
    ).order_by('-start_time')[:10]
    
    # User Progress Overview
    users_with_progress = UserProgress.objects.values('user').distinct().count()
    avg_mastery = UserProgress.objects.aggregate(avg=Avg('mastery_level'))['avg'] or 0
    
    # Top Performers
    top_performers = UserProgress.objects.values(
        'user__username'
    ).annotate(
        avg_score=Avg('best_score'),
        total_exercises=Count('exercise')
    ).order_by('-avg_score')[:5]
    
    context = {
        # User Stats
        'total_users': total_users,
        'active_users_30days': active_users_30days,
        'new_users_7days': new_users_7days,
        
        # Sample Stats
        'total_handwriting_samples': total_handwriting_samples,
        'total_speech_samples': total_speech_samples,
        'total_video_samples': total_video_samples,
        'samples_today': samples_today,
        
        # Detection Stats
        'total_detections': total_detections,
        'detections_today': detections_today,
        'high_risk_count': high_risk_count,
        'low_risk_count': low_risk_count,
        'high_risk_pct': (high_risk_count * 100 / total_detections) if total_detections > 0 else 0,
        'low_risk_pct': (low_risk_count * 100 / total_detections) if total_detections > 0 else 0,
        'avg_dyslexia_prob': avg_dyslexia_prob * 100,
        'avg_dysgraphia_prob': avg_dysgraphia_prob * 100,
        'risk_distribution': risk_distribution,
        
        # Training Stats
        'total_exercises': total_exercises,
        'total_sessions': total_sessions,
        'sessions_today': sessions_today,
        'avg_session_score': avg_session_score * 100,
        'exercise_type_stats': exercise_type_stats,
        
        # Progress Stats
        'users_with_progress': users_with_progress,
        'avg_mastery': avg_mastery * 100,
        'top_performers': top_performers,
        
        # Recent Activity
        'recent_users': recent_users,
        'recent_detections': recent_detections,
        'recent_sessions': recent_sessions,
    }
    
    return render(request, 'user_interface/admin_dashboard.html', context)


@login_required
@user_passes_test(is_admin, login_url='admin_login')
def admin_users(request):
    """Admin view to manage users"""
    users = User.objects.filter(
        is_staff=False, is_superuser=False
    ).select_related('userprofile').order_by('-date_joined')
    
    # Add detection and progress stats for each user
    for user in users:
        user.detection_count = DetectionResult.objects.filter(user=user).count()
        user.session_count = ExerciseSession.objects.filter(user=user).count()
        user.latest_detection = DetectionResult.objects.filter(
            user=user
        ).order_by('-detection_timestamp').first()
    
    context = {
        'users': users,
    }
    return render(request, 'user_interface/admin_users.html', context)


@login_required
@user_passes_test(is_admin, login_url='admin_login')
def admin_detections(request):
    """Admin view to see all detection results"""
    detections = DetectionResult.objects.select_related(
        'user', 'handwriting_sample', 'speech_sample'
    ).order_by('-detection_timestamp')
    
    # Filter options
    risk_filter = request.GET.get('risk_level')
    if risk_filter:
        detections = detections.filter(risk_level=risk_filter)
    
    context = {
        'detections': detections,
        'risk_filter': risk_filter,
    }
    return render(request, 'user_interface/admin_detections_v2.html', context)


@login_required
@user_passes_test(is_admin, login_url='admin_login')
def admin_exercises(request):
    """Admin view to manage exercises"""
    exercises = Exercise.objects.all().order_by('-created_at')
    
    # Add usage statistics
    for exercise in exercises:
        exercise.session_count = ExerciseSession.objects.filter(exercise=exercise).count()
        exercise.avg_score = ExerciseSession.objects.filter(
            exercise=exercise
        ).aggregate(avg=Avg('score'))['avg'] or 0
        exercise.user_count = ExerciseSession.objects.filter(
            exercise=exercise
        ).values('user').distinct().count()
    
    context = {
        'exercises': exercises,
    }
    return render(request, 'user_interface/admin_exercises.html', context)


@login_required
@user_passes_test(is_admin, login_url='admin_login')
def admin_logout(request):
    """Admin logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('admin_login')
