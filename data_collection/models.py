from django.db import models
from django.contrib.auth.models import User
import uuid

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    grade_level = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - Grade {self.grade_level}"

class HandwritingSample(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image_file = models.ImageField(upload_to='handwriting_samples/')
    text_content = models.TextField(help_text="The text that was written")
    timestamp = models.DateTimeField(auto_now_add=True)
    eye_tracking_data = models.JSONField(null=True, blank=True, help_text="Eye tracking coordinates")
    
    # Preprocessing flags
    is_preprocessed = models.BooleanField(default=False)
    preprocessed_image = models.ImageField(upload_to='preprocessed_handwriting/', null=True, blank=True)
    
    def __str__(self):
        return f"Handwriting Sample {self.id} - {self.user.username}"

class SpeechSample(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    audio_file = models.FileField(upload_to='speech_samples/')
    text_content = models.TextField(help_text="The text that was spoken")
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Preprocessing flags
    is_preprocessed = models.BooleanField(default=False)
    preprocessed_audio = models.FileField(upload_to='preprocessed_speech/', null=True, blank=True)
    
    def __str__(self):
        return f"Speech Sample {self.id} - {self.user.username}"

class EyeTrackingData(models.Model):
    sample = models.ForeignKey(HandwritingSample, on_delete=models.CASCADE, related_name='eye_tracking')
    x_coordinate = models.FloatField()
    y_coordinate = models.FloatField()
    timestamp = models.FloatField()  # Time in milliseconds
    pupil_diameter = models.FloatField(null=True, blank=True)
    
    class Meta:
        ordering = ['timestamp']

class VideoSample(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video_file = models.FileField(upload_to='video_samples/')
    description = models.TextField(blank=True, help_text="Context of the video (e.g., reading session)")
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Video Sample {self.id} - {self.user.username}"