from django.db import models
from django.contrib.auth.models import User
import uuid

class SpeechAnalysis(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sample = models.ForeignKey('data_collection.SpeechSample', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Audio Feature Analysis
    pronunciation_score = models.FloatField(help_text="Pronunciation accuracy score (0-1)")
    fluency_score = models.FloatField(help_text="Speech fluency score (0-1)")
    reading_speed = models.FloatField(help_text="Words per minute")
    pause_frequency = models.FloatField(help_text="Number of pauses per minute")
    
    # Detailed Analysis
    mispronunciations = models.JSONField(default=list, help_text="List of mispronounced words")
    fluency_issues = models.JSONField(default=list, help_text="List of fluency problems")
    phoneme_analysis = models.JSONField(default=dict, help_text="Phoneme-level analysis")
    
    # Audio Features
    pitch_variation = models.FloatField(help_text="Pitch variation score")
    volume_consistency = models.FloatField(help_text="Volume consistency score")
    rhythm_score = models.FloatField(help_text="Speech rhythm score")
    
    # Model confidence
    model_confidence = models.FloatField(help_text="Model confidence in analysis (0-1)")
    analysis_timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Speech Analysis {self.id} - Pronunciation: {self.pronunciation_score:.2f}"

class SpeechModel(models.Model):
    name = models.CharField(max_length=100)
    version = models.CharField(max_length=20)
    model_file = models.FileField(upload_to='speech_models/')
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    accuracy_score = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} v{self.version}"