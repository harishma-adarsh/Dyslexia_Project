from data_collection.models import HandwritingSample, SpeechSample
from handwriting_analysis.models import HandwritingAnalysis
from speech_analysis.models import SpeechAnalysis
from detection_module.models import DetectionResult
from training_module.models import UserProgress, ExerciseSession, ProgressReport

print("Clearing all analysis and progress results...")

# Order matters for some FKs, but CASCADE usually handles it
# We clear specific ones to be sure

try:
    DetectionResult.objects.all().delete()
    print("Cleared Detection Results")
    
    HandwritingAnalysis.objects.all().delete()
    print("Cleared Handwriting Analyses")
    
    SpeechAnalysis.objects.all().delete()
    print("Cleared Speech Analyses")
    
    HandwritingSample.objects.all().delete()
    print("Cleared Handwriting Samples")
    
    SpeechSample.objects.all().delete()
    print("Cleared Speech Samples")
    
    UserProgress.objects.all().delete()
    print("Cleared User Progress")
    
    ExerciseSession.objects.all().delete()
    print("Cleared Exercise Sessions")
    
    ProgressReport.objects.all().delete()
    print("Cleared Progress Reports")
    
    print("\nAll results have been successfully cleared!")
except Exception as e:
    print(f"Error clearing results: {e}")
