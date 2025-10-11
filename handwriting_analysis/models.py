from django.db import models
from django.contrib.auth.models import User
import uuid

class HandwritingAnalysis(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sample = models.ForeignKey('data_collection.HandwritingSample', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # CNN Analysis Results
    irregular_shapes_score = models.FloatField(help_text="Score for irregular letter shapes (0-1)")
    spacing_issues_score = models.FloatField(help_text="Score for spacing problems (0-1)")
    stroke_pattern_score = models.FloatField(help_text="Score for stroke pattern irregularities (0-1)")
    overall_handwriting_score = models.FloatField(help_text="Overall handwriting quality score (0-1)")
    
    # Detailed Analysis
    letter_formation_issues = models.JSONField(default=list, help_text="List of specific letter formation problems")
    spacing_analysis = models.JSONField(default=dict, help_text="Detailed spacing analysis")
    stroke_analysis = models.JSONField(default=dict, help_text="Detailed stroke pattern analysis")
    
    # Model confidence
    model_confidence = models.FloatField(help_text="CNN model confidence in analysis (0-1)")
    analysis_timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Handwriting Analysis {self.id} - Score: {self.overall_handwriting_score:.2f}"

class HandwritingModel(models.Model):
    name = models.CharField(max_length=100)
    version = models.CharField(max_length=20)
    model_file = models.FileField(upload_to='handwriting_models/')
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    accuracy_score = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} v{self.version}"