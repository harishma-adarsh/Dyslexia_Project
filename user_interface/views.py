from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import json
import os
from datetime import datetime, timedelta
from django.db import models

from data_collection.models import UserProfile, HandwritingSample, SpeechSample
from handwriting_analysis.models import HandwritingAnalysis
from speech_analysis.models import SpeechAnalysis
from detection_module.models import DetectionResult
from training_module.models import Exercise, UserProgress, ExerciseSession, ProgressReport

def home(request):
    """Home page with child-friendly interface"""
    if request.user.is_authenticated:
        # Get user's recent progress
        recent_sessions = ExerciseSession.objects.filter(user=request.user).order_by('-start_time')[:5]
        recent_detections = DetectionResult.objects.filter(user=request.user).order_by('-detection_timestamp')[:3]
        
        context = {
            'recent_sessions': recent_sessions,
            'recent_detections': recent_detections,
        }
        return render(request, 'user_interface/home.html', context)
    return render(request, 'user_interface/landing.html')

def register(request):
    """User registration with child-friendly form"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create user profile
            UserProfile.objects.create(
                user=user,
                age=request.POST.get('age', 8),
                grade_level=request.POST.get('grade_level', '3rd')
            )
            login(request, user)
            messages.success(request, 'Welcome! Your account has been created.')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'user_interface/register.html', {'form': form})

@login_required
def upload_data(request):
    """Data upload interface for handwriting and speech samples"""
    if request.method == 'POST':
        # Handle handwriting upload
        if 'handwriting_image' in request.FILES:
            handwriting_sample = HandwritingSample.objects.create(
                user=request.user,
                image_file=request.FILES['handwriting_image'],
                text_content=request.POST.get('handwriting_text', ''),
                eye_tracking_data=json.loads(request.POST.get('eye_tracking_data', '[]'))
            )
            messages.success(request, 'Handwriting sample uploaded successfully!')
        
        # Handle speech upload
        if 'speech_audio' in request.FILES:
            speech_sample = SpeechSample.objects.create(
                user=request.user,
                audio_file=request.FILES['speech_audio'],
                text_content=request.POST.get('speech_text', '')
            )
            messages.success(request, 'Speech sample uploaded successfully!')
        
        return redirect('upload_data')
    
    return render(request, 'user_interface/upload_data.html')

@login_required
def analyze_samples(request):
    """Analyze uploaded samples"""
    if request.method == 'POST':
        sample_id = request.POST.get('sample_id')
        sample_type = request.POST.get('sample_type')
        
        if sample_type == 'handwriting':
            sample = get_object_or_404(HandwritingSample, id=sample_id, user=request.user)
            
            # Simplified analysis - create mock results for demonstration
            analysis_result = {
                'irregular_shapes_score': 0.3,
                'spacing_issues_score': 0.4,
                'stroke_pattern_score': 0.2,
                'overall_handwriting_score': 0.3,
                'letter_formation_issues': ['Some letters may need practice'],
                'spacing_analysis': {'word_spacing_consistency': 0.7},
                'stroke_analysis': {'stroke_consistency': 0.6},
                'model_confidence': 0.8
            }
            
            # Save analysis
            HandwritingAnalysis.objects.create(
                sample=sample,
                user=request.user,
                **analysis_result
            )
            
            messages.success(request, 'Handwriting analysis completed!')
        
        elif sample_type == 'speech':
            sample = get_object_or_404(SpeechSample, id=sample_id, user=request.user)
            
            # Simplified analysis - create mock results for demonstration
            analysis_result = {
                'pronunciation_score': 0.7,
                'fluency_score': 0.6,
                'reading_speed': 120.0,
                'pause_frequency': 1.5,
                'mispronunciations': [],
                'fluency_issues': ['Minor rhythm variations'],
                'phoneme_analysis': {'mfcc_mean': [0.1, 0.2, 0.3]},
                'pitch_variation': 0.3,
                'volume_consistency': 0.8,
                'rhythm_score': 0.7,
                'model_confidence': 0.8
            }
            
            # Save analysis
            SpeechAnalysis.objects.create(
                sample=sample,
                user=request.user,
                **analysis_result
            )
            
            messages.success(request, 'Speech analysis completed!')
    
    # Get user's samples
    handwriting_samples = HandwritingSample.objects.filter(user=request.user).order_by('-timestamp')
    speech_samples = SpeechSample.objects.filter(user=request.user).order_by('-timestamp')
    
    context = {
        'handwriting_samples': handwriting_samples,
        'speech_samples': speech_samples,
    }
    return render(request, 'user_interface/analyze_samples.html', context)

@login_required
def detection_results(request):
    """View detection results and recommendations"""
    if request.method == 'POST':
        # Run combined detection
        handwriting_sample_id = request.POST.get('handwriting_sample_id')
        speech_sample_id = request.POST.get('speech_sample_id')
        
        handwriting_analysis = None
        speech_analysis = None
        
        if handwriting_sample_id:
            handwriting_analysis = HandwritingAnalysis.objects.filter(
                sample_id=handwriting_sample_id, user=request.user
            ).first()
        
        if speech_sample_id:
            speech_analysis = SpeechAnalysis.objects.filter(
                sample_id=speech_sample_id, user=request.user
            ).first()
        
        # Simplified detection - create mock results for demonstration
        if handwriting_analysis and speech_analysis:
            overall_risk = (handwriting_analysis.overall_handwriting_score + 
                           (1 - speech_analysis.pronunciation_score)) / 2
        elif handwriting_analysis:
            overall_risk = handwriting_analysis.overall_handwriting_score
        elif speech_analysis:
            overall_risk = 1 - speech_analysis.pronunciation_score
        else:
            overall_risk = 0.5
        
        risk_level = 'low' if overall_risk < 0.3 else 'medium' if overall_risk < 0.6 else 'high'
        
        detection_result = {
            'dyslexia_probability': overall_risk,
            'dysgraphia_probability': handwriting_analysis.overall_handwriting_score if handwriting_analysis else 0.0,
            'overall_risk_score': overall_risk,
            'risk_level': risk_level,
            'detection_confidence': 0.8,
            'recommended_actions': [
                'Practice handwriting exercises',
                'Work on reading fluency',
                'Consider professional assessment if concerns persist'
            ],
            'strengths_identified': [
                'Good effort in completing tasks',
                'Willingness to practice'
            ],
            'areas_of_concern': [
                'Letter formation needs improvement',
                'Reading speed could be enhanced'
            ]
        }
        
        # Save detection result
        DetectionResult.objects.create(
            user=request.user,
            handwriting_sample=handwriting_analysis.sample if handwriting_analysis else None,
            speech_sample=speech_analysis.sample if speech_analysis else None,
            handwriting_analysis=handwriting_analysis,
            speech_analysis=speech_analysis,
            **detection_result
        )
        
        messages.success(request, 'Detection analysis completed!')
        return redirect('detection_results')
    
    # Get user's detection results
    detection_results = DetectionResult.objects.filter(user=request.user).order_by('-detection_timestamp')
    
    context = {
        'detection_results': detection_results,
    }
    return render(request, 'user_interface/detection_results.html', context)

@login_required
def training_exercises(request):
    """Training exercises interface"""
    exercises = Exercise.objects.filter(is_active=True)
    user_progress = UserProgress.objects.filter(user=request.user)
    
    context = {
        'exercises': exercises,
        'user_progress': user_progress,
    }
    return render(request, 'user_interface/training_exercises.html', context)

@login_required
def start_exercise(request, exercise_id):
    """Start a training exercise"""
    exercise = get_object_or_404(Exercise, id=exercise_id)
    
    if request.method == 'POST':
        # Handle exercise completion
        session_data = json.loads(request.POST.get('session_data', '{}'))
        score = float(request.POST.get('score', 0))
        duration = int(request.POST.get('duration', 0))
        
        # Create exercise session
        session = ExerciseSession.objects.create(
            user=request.user,
            exercise=exercise,
            score=score,
            duration=duration,
            session_data=session_data
        )
        
        # Update user progress
        progress, created = UserProgress.objects.get_or_create(
            user=request.user,
            exercise=exercise
        )
        
        progress.attempts += 1
        if score > progress.best_score:
            progress.best_score = score
            progress.successful_attempts += 1
        
        progress.total_time_spent += duration
        progress.last_attempt = datetime.now()
        
        if not progress.first_attempt:
            progress.first_attempt = datetime.now()
        
        if score >= 0.8:  # 80% threshold for completion
            progress.completed_at = datetime.now()
            progress.mastery_level = min(progress.mastery_level + 0.1, 1.0)
        
        progress.save()
        
        messages.success(request, f'Great job! You scored {score:.1%}')
        return redirect('training_exercises')
    
    context = {
        'exercise': exercise,
    }
    return render(request, 'user_interface/exercise_session.html', context)

@login_required
def progress_reports(request):
    """View progress reports and analytics"""
    # Generate progress report for current month
    current_date = datetime.now().date()
    report, created = ProgressReport.objects.get_or_create(
        user=request.user,
        report_date=current_date
    )
    
    if created:
        # Calculate progress metrics
        sessions_this_month = ExerciseSession.objects.filter(
            user=request.user,
            start_time__month=current_date.month,
            start_time__year=current_date.year
        )
        
        report.total_exercises_completed = sessions_this_month.count()
        report.average_score = sessions_this_month.aggregate(
            avg_score=models.Avg('score')
        )['avg_score'] or 0
        
        report.total_time_spent = sum(s.duration for s in sessions_this_month if s.duration) // 60
        
        # Calculate improvements
        last_month = current_date - timedelta(days=30)
        last_month_sessions = ExerciseSession.objects.filter(
            user=request.user,
            start_time__gte=last_month,
            start_time__lt=current_date - timedelta(days=15)
        )
        
        if last_month_sessions.exists():
            old_avg = last_month_sessions.aggregate(avg_score=models.Avg('score'))['avg_score'] or 0
            new_avg = sessions_this_month.aggregate(avg_score=models.Avg('score'))['avg_score'] or 0
            report.reading_improvement = max(0, new_avg - old_avg)
        
        report.save()
    
    # Get all reports
    reports = ProgressReport.objects.filter(user=request.user).order_by('-report_date')
    
    context = {
        'current_report': report,
        'reports': reports,
    }
    return render(request, 'user_interface/progress_reports.html', context)

@login_required
def profile(request):
    """User profile management"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        profile.age = request.POST.get('age', profile.age)
        profile.grade_level = request.POST.get('grade_level', profile.grade_level)
        profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    context = {
        'profile': profile,
    }
    return render(request, 'user_interface/profile.html', context)

# API endpoints for AJAX requests
@login_required
@csrf_exempt
def upload_handwriting_api(request):
    """API endpoint for handwriting upload"""
    if request.method == 'POST':
        try:
            image_file = request.FILES['image']
            text_content = request.POST.get('text', '')
            eye_tracking_data = json.loads(request.POST.get('eye_tracking', '[]'))
            
            sample = HandwritingSample.objects.create(
                user=request.user,
                image_file=image_file,
                text_content=text_content,
                eye_tracking_data=eye_tracking_data
            )
            
            return JsonResponse({
                'success': True,
                'sample_id': str(sample.id),
                'message': 'Handwriting sample uploaded successfully'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
@csrf_exempt
def upload_speech_api(request):
    """API endpoint for speech upload"""
    if request.method == 'POST':
        try:
            audio_file = request.FILES['audio']
            text_content = request.POST.get('text', '')
            
            sample = SpeechSample.objects.create(
                user=request.user,
                audio_file=audio_file,
                text_content=text_content
            )
            
            return JsonResponse({
                'success': True,
                'sample_id': str(sample.id),
                'message': 'Speech sample uploaded successfully'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def logout_view(request):
    """Logout user and redirect to home"""
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('home')
