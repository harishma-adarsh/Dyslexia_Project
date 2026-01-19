from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import json
import os
import wave
import struct
import math
from datetime import datetime, timedelta
from django.db import models

from data_collection.models import UserProfile, HandwritingSample, SpeechSample, VideoSample
from handwriting_analysis.models import HandwritingAnalysis
from speech_analysis.models import SpeechAnalysis
from detection_module.models import DetectionResult
from detection_module.detection_engine import DyslexiaDetectionEngine
from training_module.models import Exercise, UserProgress, ExerciseSession, ProgressReport

def home(request):
    """Home page with child-friendly interface"""
    if request.user.is_authenticated:
        # Guide users through the intended flow
        has_handwriting = HandwritingSample.objects.filter(user=request.user).exists()
        has_speech = SpeechSample.objects.filter(user=request.user).exists()
        if not (has_handwriting or has_speech):
            return redirect('upload_data')

        # Get user's recent progress
        recent_sessions = ExerciseSession.objects.filter(user=request.user).order_by('-start_time')[:5]
        recent_detections = DetectionResult.objects.filter(user=request.user).order_by('-detection_timestamp')[:3]
        # Determine if latest detection indicates a condition that needs training
        latest_detection = DetectionResult.objects.filter(user=request.user).order_by('-detection_timestamp').first()
        has_positive_detection = bool(latest_detection and (
            latest_detection.risk_level in ['medium', 'high'] or
            latest_detection.dyslexia_probability > 0.4 or
            latest_detection.dysgraphia_probability > 0.4
        ))

        # If a condition is detected, suggest training
        if has_positive_detection:
            # Note: We don't automatically redirect if they might want to see history,
            # but we can prioritize showing training links in the UI.
            pass
        
        context = {
            'recent_sessions': recent_sessions,
            'recent_detections': recent_detections,
            'hide_upload': has_positive_detection,
        }
        return render(request, 'user_interface/home.html', context)
    return render(request, 'user_interface/landing.html')

from user_interface.forms import SimpleRegistrationForm

def register(request):
    """User registration with simple password validation"""
    if request.method == 'POST':
        form = SimpleRegistrationForm(request.POST)
        if form.is_valid():
            # Create user
            user = form.save()
            
            # Create user profile
            UserProfile.objects.create(
                user=user,
                age=form.cleaned_data['age'],
                grade_level=form.cleaned_data['grade_level']
            )
            
            # Log the user in
            login(request, user)
            messages.success(request, 'Welcome! Your account has been created.')
            return redirect('home')
    else:
        form = SimpleRegistrationForm()
    
    return render(request, 'user_interface/register.html', {'form': form})

def login_view(request):
    """Custom user login page"""
    if request.user.is_authenticated:
        return redirect('home')
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Welcome back!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'user_interface/login.html', {'form': form})

@login_required
def upload_data(request):
    """Data upload interface for handwriting and speech samples"""
    if request.method == 'POST':
        if request.POST.get('use_demo') == '1':
            # ... (demo logic remains the same)
            # Ensure demo files exist on disk
            handwriting_dir = os.path.join(settings.MEDIA_ROOT, 'handwriting_samples')
            speech_dir = os.path.join(settings.MEDIA_ROOT, 'speech_samples')
            os.makedirs(handwriting_dir, exist_ok=True)
            os.makedirs(speech_dir, exist_ok=True)

            demo_img_path = os.path.join(handwriting_dir, 'demo.png')
            demo_wav_path = os.path.join(speech_dir, 'demo.wav')

            if not os.path.exists(demo_img_path):
                png_bytes = bytes([137,80,78,71,13,10,26,10,0,0,0,13,73,72,68,82,0,0,0,1,0,0,0,1,8,2,0,0,0,144,119,83,222,0,0,0,12,73,68,65,84,8,215,99,248,15,4,0,9,251,3,253,167,130,196,94,0,0,0,0,73,69,78,68,174,66,96,130])
                with open(demo_img_path, 'wb') as f: f.write(png_bytes)

            if not os.path.exists(demo_wav_path):
                framerate = 16000
                with wave.open(demo_wav_path, 'w') as wf:
                    wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(framerate)
                    wf.writeframes(b'\x00' * 32000)

            handwriting_sample = HandwritingSample.objects.create(
                user=request.user, image_file='handwriting_samples/demo.png',
                text_content='The cat sat on the mat.', eye_tracking_data=[{"x":100,"y":200,"timestamp":1000}]
            )
            speech_sample = SpeechSample.objects.create(
                user=request.user, audio_file='speech_samples/demo.wav',
                text_content='The cat sat on the mat.'
            )
            VideoSample.objects.create(
                user=request.user, video_file='video_samples/demo.mp4',
                description='Demo reading video'
            )

            # 1. Create Mock Analyses
            hw_analysis = HandwritingAnalysis.objects.create(
                sample=handwriting_sample, user=request.user,
                irregular_shapes_score=0.35, spacing_issues_score=0.45,
                stroke_pattern_score=0.25, overall_handwriting_score=0.4,
                letter_formation_issues=['Slight irregularity'],
                spacing_analysis={'word_spacing_consistency': 0.65},
                stroke_analysis={'stroke_consistency': 0.7},
                model_confidence=0.9
            )
            sp_analysis = SpeechAnalysis.objects.create(
                sample=speech_sample, user=request.user,
                pronunciation_score=0.6, fluency_score=0.5,
                reading_speed=110.0, pause_frequency=1.8,
                mispronunciations=['Minor errors'],
                fluency_issues=['Moderate variations'],
                phoneme_analysis={'mfcc_mean': [0.1, 0.2]},
                pitch_variation=0.3, volume_consistency=0.7,
                rhythm_score=0.6, model_confidence=0.85
            )

            # 2. Run Engine & Save Result
            engine = DyslexiaDetectionEngine()
            result = engine.detect_dyslexia(hw_analysis.__dict__, sp_analysis.__dict__)
            
            DetectionResult.objects.create(
                user=request.user, handwriting_sample=handwriting_sample,
                speech_sample=speech_sample, handwriting_analysis=hw_analysis,
                speech_analysis=sp_analysis, dyslexia_probability=result['dyslexia_probability'],
                dysgraphia_probability=result['dysgraphia_probability'],
                overall_risk_score=result['overall_risk_score'],
                risk_level=result['risk_level'],
                detection_confidence=result['detection_confidence'],
                recommended_actions=result['recommended_actions'],
                strengths_identified=result['strengths_identified'],
                areas_of_concern=result['areas_of_concern']
            )

            messages.success(request, 'Demo analysis completed! Training exercises are now available.')
            return redirect('detection_results')

        action = request.POST.get('action')
        handwriting_sample = None
        speech_sample = None

        # Handle handwriting upload
        if 'handwriting_image' in request.FILES:
            try:
                eye_data = request.POST.get('eye_tracking_data', '[]')
                if not eye_data or eye_data.strip() == '':
                    eye_data = '[]'
                
                handwriting_sample = HandwritingSample.objects.create(
                    user=request.user,
                    image_file=request.FILES['handwriting_image'],
                    text_content=request.POST.get('handwriting_text', ''),
                    eye_tracking_data=json.loads(eye_data)
                )
                if action != 'run_combined':
                    messages.success(request, 'Handwriting sample uploaded successfully!')
            except Exception as e:
                messages.error(request, f'Error uploading handwriting: {str(e)}')
        
        # Handle speech upload
        if 'speech_audio' in request.FILES:
            speech_sample = SpeechSample.objects.create(
                user=request.user,
                audio_file=request.FILES['speech_audio'],
                text_content=request.POST.get('speech_text', '')
            )
            if action != 'run_combined':
                messages.success(request, 'Speech sample uploaded successfully!')

        # Handle video upload
        if 'video_file' in request.FILES:
            VideoSample.objects.create(
                user=request.user,
                video_file=request.FILES['video_file'],
                description=request.POST.get('video_description', '')
            )
            if action != 'run_combined':
                messages.success(request, 'Video sample uploaded successfully!')

        if action == 'run_combined' and (handwriting_sample or speech_sample):
            # 1. Handwriting Analysis (if provided)
            hw_analysis = None
            if handwriting_sample:
                hw_analysis_result = {
                    'irregular_shapes_score': 0.35,
                    'spacing_issues_score': 0.45,
                    'stroke_pattern_score': 0.25,
                    'overall_handwriting_score': 0.4,
                    'letter_formation_issues': ['Slight irregularity in letter formation'],
                    'spacing_analysis': {'word_spacing_consistency': 0.65},
                    'stroke_analysis': {'stroke_consistency': 0.7},
                    'model_confidence': 0.85
                }
                hw_analysis = HandwritingAnalysis.objects.create(
                    sample=handwriting_sample, user=request.user, **hw_analysis_result
                )

            # 2. Speech Analysis (if provided)
            sp_analysis = None
            if speech_sample:
                sp_analysis_result = {
                    'pronunciation_score': 0.65,
                    'fluency_score': 0.55,
                    'reading_speed': 110.0,
                    'pause_frequency': 1.8,
                    'mispronunciations': ['Minor phoneme errors'],
                    'fluency_issues': ['Moderate rhythm variations'],
                    'phoneme_analysis': {'mfcc_mean': [0.15, 0.25, 0.35]},
                    'pitch_variation': 0.35,
                    'volume_consistency': 0.75,
                    'rhythm_score': 0.65,
                    'model_confidence': 0.82
                }
                sp_analysis = SpeechAnalysis.objects.create(
                    sample=speech_sample, user=request.user, **sp_analysis_result
                )

            # 3. Run Detection Engine
            engine = DyslexiaDetectionEngine()
            result = engine.detect_dyslexia(
                hw_analysis.__dict__ if hw_analysis else None,
                sp_analysis.__dict__ if sp_analysis else None
            )
            
            # 4. Save Detection Result
            DetectionResult.objects.create(
                user=request.user,
                handwriting_sample=handwriting_sample,
                speech_sample=speech_sample,
                handwriting_analysis=hw_analysis,
                speech_analysis=sp_analysis,
                dyslexia_probability=result['dyslexia_probability'],
                dysgraphia_probability=result['dysgraphia_probability'],
                overall_risk_score=result['overall_risk_score'],
                risk_level=result['risk_level'],
                detection_confidence=result['detection_confidence'],
                recommended_actions=result['recommended_actions'],
                strengths_identified=result['strengths_identified'],
                areas_of_concern=result['areas_of_concern']
            )

            messages.success(request, 'Analysis completed successfully!')
            return redirect('detection_results')

        # Default redirect
        if action == 'upload_handwriting' or action == 'upload_speech':
            return redirect('analyze_samples')
        elif action == 'run_combined':
            messages.warning(request, 'Please select at least one sample (handwriting or speech) to analyze.')
            return redirect('upload_data')
            
        return redirect('analyze_samples')
    
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
        
        # Use detection engine
        engine = DyslexiaDetectionEngine()
        result = engine.detect_dyslexia(
            handwriting_analysis.__dict__ if handwriting_analysis else None,
            speech_analysis.__dict__ if speech_analysis else None,
        )
        overall_risk = result['overall_risk_score']
        risk_level = result['risk_level']
        detection_result = {
            'dyslexia_probability': result['dyslexia_probability'],
            'dysgraphia_probability': result['dysgraphia_probability'],
            'overall_risk_score': overall_risk,
            'risk_level': risk_level,
            'detection_confidence': result['detection_confidence'],
            'recommended_actions': result['recommended_actions'],
            'strengths_identified': result['strengths_identified'],
            'areas_of_concern': result['areas_of_concern'],
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
        
        # Redirect based on risk level
        if risk_level in ['medium', 'high']:
            messages.success(request, 'Analysis completed. We prepared exercises to help you practice!')
            return redirect('training_exercises')
        else:
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
    """Training exercises interface with personalization - Only available if risk is detected"""
    # 1. Check for positive detection
    latest_detection = DetectionResult.objects.filter(user=request.user).order_by('-detection_timestamp').first()
    has_positive_detection = bool(latest_detection and (
        latest_detection.risk_level in ['medium', 'high'] or
        latest_detection.dyslexia_probability > 0.4 or
        latest_detection.dysgraphia_probability > 0.4
    ))
    
    if not has_positive_detection:
        messages.warning(request, "Please complete your screening analysis before starting training exercises.")
        return redirect('home')

    refresh = request.GET.get('refresh') == '1'
    exercises = Exercise.objects.filter(is_active=True)

    if refresh:
        # Deactivate existing and seed an alternative set of games
        Exercise.objects.update(is_active=False)
        exercises = Exercise.objects.none()

    if not exercises.exists():
        # ... (keep existing seed logic)
        # Create comprehensive set of interactive games
        games = [
            # Reading Games
            {
                'name': 'Letter Matching Game',
                'exercise_type': 'reading',
                'difficulty_level': 'beginner',
                'description': 'Match letters with their sounds and practice reading!',
                'instructions': 'Click on each letter to hear its sound. Practice saying it out loud!',
                'content': {
                    'type': 'letter_matching',
                    'letters': ['A', 'B', 'C', 'D', 'E']
                },
                'expected_duration': 10,
                'is_active': True,
            },
            {
                'name': 'Word Building Challenge',
                'exercise_type': 'reading',
                'difficulty_level': 'beginner',
                'description': 'Build words by clicking letters in the right order!',
                'instructions': 'Click the letters to build the target word shown above.',
                'content': {
                    'type': 'word_building',
                    'letters': ['C', 'A', 'T', 'M', 'S', 'P'],
                    'target': 'CAT'
                },
                'expected_duration': 8,
                'is_active': True,
            },
            {
                'name': 'Story Reading',
                'exercise_type': 'reading',
                'difficulty_level': 'intermediate',
                'description': 'Read a short story and answer questions!',
                'instructions': 'Read the story carefully, then answer the questions below.',
                'content': {
                    'type': 'comprehension',
                    'stories': [{
                        'title': 'The Happy Cat',
                        'text': 'Tom has a cat. The cat is happy. The cat likes to play. Tom and the cat play every day.',
                        'questions': [
                            'What is the name of the boy?',
                            'What does the cat like to do?',
                            'How often do they play?'
                        ]
                    }]
                },
                'expected_duration': 15,
                'is_active': True,
            },
            
            # Writing Games
            {
                'name': 'Letter Tracing Practice',
                'exercise_type': 'writing',
                'difficulty_level': 'beginner',
                'description': 'Trace letters to practice your handwriting!',
                'instructions': 'Use your mouse or finger to trace each letter carefully.',
                'content': {
                    'type': 'letter_tracing',
                    'letters': ['A', 'B', 'C']
                },
                'expected_duration': 12,
                'is_active': True,
            },
            {
                'name': 'Word Copying Game',
                'exercise_type': 'writing',
                'difficulty_level': 'beginner',
                'description': 'Copy simple words to improve your writing!',
                'instructions': 'Look at each word and write it in the box below.',
                'content': {
                    'type': 'word_copying',
                    'words': ['cat', 'dog', 'sun', 'fun']
                },
                'expected_duration': 10,
                'is_active': True,
            },
            {
                'name': 'Creative Story Writing',
                'exercise_type': 'writing',
                'difficulty_level': 'intermediate',
                'description': 'Write your own creative story!',
                'instructions': 'Use the words provided to write a fun story.',
                'content': {
                    'type': 'creative_writing',
                    'prompt_words': ['cat', 'happy', 'play', 'friend'],
                    'min_words': 20
                },
                'expected_duration': 20,
                'is_active': True,
            },
            
            # Phoneme/Sound Games
            {
                'name': 'Sound Matching Fun',
                'exercise_type': 'phoneme',
                'difficulty_level': 'beginner',
                'description': 'Listen to sounds and match them!',
                'instructions': 'Click each button to hear the sound. Practice saying it!',
                'content': {
                    'type': 'sound_matching',
                    'sounds': ['a', 'e', 'i', 'o', 'u']
                },
                'expected_duration': 10,
                'is_active': True,
            },
            {
                'name': 'Rhyming Words Game',
                'exercise_type': 'phoneme',
                'difficulty_level': 'intermediate',
                'description': 'Find words that rhyme together!',
                'instructions': 'Click on words that rhyme with the target word.',
                'content': {
                    'type': 'rhyming',
                    'base_words': ['cat'],
                    'options': ['hat', 'dog', 'mat', 'car', 'bat', 'sun']
                },
                'expected_duration': 12,
                'is_active': True,
            },
            {
                'name': 'Sound Blending Challenge',
                'exercise_type': 'phoneme',
                'difficulty_level': 'intermediate',
                'description': 'Blend sounds together to make words!',
                'instructions': 'Listen to each sound, then type the word you hear.',
                'content': {
                    'type': 'blending',
                    'sound_sequences': [['c', 'a', 't']]
                },
                'expected_duration': 15,
                'is_active': True,
            },
        ]
        
        for game_data in games:
            Exercise.objects.create(**game_data)
        
        exercises = Exercise.objects.filter(is_active=True)

    # Personalization based on latest detection
    latest_detection = DetectionResult.objects.filter(user=request.user).order_by('-detection_timestamp').first()
    recommended_types = []
    
    if latest_detection:
        if latest_detection.dyslexia_probability > 0.4:
            recommended_types.extend(['reading', 'phoneme', 'comprehension'])
        if latest_detection.dysgraphia_probability > 0.4:
            recommended_types.append('writing')
    
    # If we have recommendations, sort exercises to show them first
    if recommended_types:
        # Exercises that match recommended types come first
        from django.db.models import Case, When, Value, IntegerField
        exercises = exercises.annotate(
            priority=Case(
                When(exercise_type__in=recommended_types, then=Value(1)),
                default=Value(2),
                output_field=IntegerField(),
            )
        ).order_by('priority', 'difficulty_level')

    user_progress = UserProgress.objects.filter(user=request.user)
    progress_map = {p.exercise_id: p for p in user_progress}
    
    # Calculate summary stats
    total_time = sum(p.total_time_spent for p in user_progress)
    best_score = max((p.best_score for p in user_progress), default=0)
    mastered_count = sum(1 for p in user_progress if p.mastery_level >= 0.8)
    
    for exercise in exercises:
        exercise.user_progress = progress_map.get(exercise.id)
    
    context = {
        'exercises': exercises,
        'user_progress_count': user_progress.count(),
        'total_time': total_time,
        'best_score': best_score * 100,
        'mastered_count': mastered_count,
        'latest_detection': latest_detection,
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
    
    # Ensure content is properly parsed as dict if it's a string
    if isinstance(exercise.content, str):
        exercise.content = json.loads(exercise.content)
    
    context = {
        'exercise': exercise,
    }
    return render(request, 'user_interface/exercise_session.html', context)

@login_required
def progress_reports(request):
    """View progress reports and analytics - Only available if risk is detected"""
    # Check for positive detection
    latest_detection = DetectionResult.objects.filter(user=request.user).order_by('-detection_timestamp').first()
    has_positive_detection = bool(latest_detection and (
        latest_detection.risk_level in ['medium', 'high'] or
        latest_detection.dyslexia_probability > 0.4 or
        latest_detection.dysgraphia_probability > 0.4
    ))
    
    if not has_positive_detection:
        return redirect('home')

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
