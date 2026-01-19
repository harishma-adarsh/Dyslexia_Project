from django.db import models
from django.contrib.auth.models import User
import uuid

class DetectionResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Input samples
    handwriting_sample = models.ForeignKey('data_collection.HandwritingSample', on_delete=models.CASCADE, null=True, blank=True)
    speech_sample = models.ForeignKey('data_collection.SpeechSample', on_delete=models.CASCADE, null=True, blank=True)
    
    # Analysis results
    handwriting_analysis = models.ForeignKey('handwriting_analysis.HandwritingAnalysis', on_delete=models.CASCADE, null=True, blank=True)
    speech_analysis = models.ForeignKey('speech_analysis.SpeechAnalysis', on_delete=models.CASCADE, null=True, blank=True)
    
    # Combined Detection Results
    dyslexia_probability = models.FloatField(help_text="Probability of dyslexia (0-1)")
    dysgraphia_probability = models.FloatField(help_text="Probability of dysgraphia (0-1)")
    overall_risk_score = models.FloatField(help_text="Overall risk score (0-1)")
    
    # Risk Levels
    RISK_LEVELS = [
        ('low', 'Low Risk'),
        ('medium', 'Medium Risk'),
        ('high', 'High Risk'),
    ]
    risk_level = models.CharField(max_length=10, choices=RISK_LEVELS)
    
    # Detailed Results
    detection_confidence = models.FloatField(help_text="Overall detection confidence (0-1)")
    recommended_actions = models.JSONField(default=list, help_text="List of recommended actions")
    strengths_identified = models.JSONField(default=list, help_text="List of identified strengths")
    areas_of_concern = models.JSONField(default=list, help_text="List of areas requiring attention")
    
    # Timestamps
    detection_timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Detection Result {self.id} - Risk: {self.risk_level} ({self.overall_risk_score:.2f})"

    @property
    def identified_condition(self):
        conditions = []
        if self.dyslexia_probability > 0.4:
            conditions.append("Dyslexia")
        if self.dysgraphia_probability > 0.4:
            conditions.append("Dysgraphia")
        
        if not conditions:
            return "No specific condition identified"
        return " & ".join(conditions)

class DetectionModel(models.Model):
    name = models.CharField(max_length=100)
    version = models.CharField(max_length=20)
    model_file = models.FileField(upload_to='detection_models/')
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    accuracy_score = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} v{self.version}"