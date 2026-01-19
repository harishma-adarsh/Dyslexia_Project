from data_collection.models import HandwritingSample, SpeechSample
from handwriting_analysis.models import HandwritingAnalysis
from speech_analysis.models import SpeechAnalysis
from detection_module.models import DetectionResult
from training_module.models import UserProgress, ExerciseSession, ProgressReport

print(f"Detection Results: {DetectionResult.objects.count()}")
print(f"Handwriting Samples: {HandwritingSample.objects.count()}")
print(f"Speech Samples: {SpeechSample.objects.count()}")
print(f"User Progress: {UserProgress.objects.count()}")
