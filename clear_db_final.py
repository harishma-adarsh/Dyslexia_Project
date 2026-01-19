import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Dyslexia.settings')
django.setup()

from data_collection.models import HandwritingSample, SpeechSample
from handwriting_analysis.models import HandwritingAnalysis
from speech_analysis.models import SpeechAnalysis
from detection_module.models import DetectionResult
from training_module.models import UserProgress, ExerciseSession, ProgressReport

print("Clearing all analysis and progress results...")

try:
    n1 = DetectionResult.objects.all().delete()[0]
    n2 = HandwritingAnalysis.objects.all().delete()[0]
    n3 = SpeechAnalysis.objects.all().delete()[0]
    n4 = HandwritingSample.objects.all().delete()[0]
    n5 = SpeechSample.objects.all().delete()[0]
    n6 = UserProgress.objects.all().delete()[0]
    n7 = ExerciseSession.objects.all().delete()[0]
    n8 = ProgressReport.objects.all().delete()[0]
    
    print(f"Cleared {n1} Detection Results")
    print(f"Cleared {n2} Handwriting Analyses")
    print(f"Cleared {n3} Speech Analyses")
    print(f"Cleared {n4} Handwriting Samples")
    print(f"Cleared {n5} Speech Samples")
    print(f"Cleared {n6} User Progress records")
    print(f"Cleared {n7} Exercise Sessions")
    print(f"Cleared {n8} Progress Reports")
    
    print("\nAll results have been successfully cleared!")
except Exception as e:
    print(f"Error clearing results: {e}")
