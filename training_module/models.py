from django.db import models
from django.contrib.auth.models import User
import uuid

class Exercise(models.Model):
    EXERCISE_TYPES = [
        ('reading', 'Reading Exercise'),
        ('writing', 'Writing Exercise'),
        ('phoneme', 'Phoneme Practice'),
        ('comprehension', 'Reading Comprehension'),
    ]
    
    DIFFICULTY_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    exercise_type = models.CharField(max_length=20, choices=EXERCISE_TYPES)
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS)
    description = models.TextField()
    instructions = models.TextField()
    
    # Exercise content
    content = models.JSONField(help_text="Exercise content and materials")
    expected_duration = models.IntegerField(help_text="Expected duration in minutes")
    
    # Metadata
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.exercise_type})"

class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    
    # Progress tracking
    attempts = models.IntegerField(default=0)
    successful_attempts = models.IntegerField(default=0)
    best_score = models.FloatField(default=0.0)
    total_time_spent = models.IntegerField(default=0, help_text="Total time in seconds")
    
    # Adaptive learning
    current_difficulty = models.CharField(max_length=20, choices=Exercise.DIFFICULTY_LEVELS)
    mastery_level = models.FloatField(default=0.0, help_text="Mastery level (0-1)")
    
    # Timestamps
    first_attempt = models.DateTimeField(null=True, blank=True)
    last_attempt = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['user', 'exercise']
    
    def __str__(self):
        return f"{self.user.username} - {self.exercise.name}"

class ExerciseSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    
    # Session data
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True, help_text="Duration in seconds")
    
    # Performance metrics
    score = models.FloatField(null=True, blank=True)
    accuracy = models.FloatField(null=True, blank=True)
    speed = models.FloatField(null=True, blank=True, help_text="Speed metric")
    
    # Session details
    session_data = models.JSONField(default=dict, help_text="Detailed session data")
    feedback = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"Session {self.id} - {self.user.username} - {self.exercise.name}"

class ProgressReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    report_date = models.DateField()
    
    # Overall progress
    total_exercises_completed = models.IntegerField(default=0)
    average_score = models.FloatField(default=0.0)
    total_time_spent = models.IntegerField(default=0, help_text="Total time in minutes")
    
    # Skill development
    reading_improvement = models.FloatField(default=0.0)
    writing_improvement = models.FloatField(default=0.0)
    phoneme_improvement = models.FloatField(default=0.0)
    
    # Detailed metrics
    detailed_metrics = models.JSONField(default=dict)
    recommendations = models.JSONField(default=list)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'report_date']
    
    def __str__(self):
        return f"Progress Report - {self.user.username} - {self.report_date}"