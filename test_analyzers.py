import os
import django
import sys

# Setup django
sys.path.append('c:\\Harishma\\Maitexa\\Project_ Dyslexia\\Dyslexia')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Dyslexia.settings')
django.setup()

from handwriting_analysis.cnn_analyzer import HandwritingCNNAnalyzer
from speech_analysis.audio_analyzer import SpeechAnalyzer

def test_analyzers():
    print("Testing HandwritingCNNAnalyzer...")
    try:
        hw_analyzer = HandwritingCNNAnalyzer()
        print("HandwritingCNNAnalyzer initialized successfully.")
    except Exception as e:
        print(f"Error initializing HandwritingCNNAnalyzer: {e}")

    print("\nTesting SpeechAnalyzer...")
    try:
        sp_analyzer = SpeechAnalyzer()
        print("SpeechAnalyzer initialized successfully.")
    except Exception as e:
        print(f"Error initializing SpeechAnalyzer: {e}")

if __name__ == "__main__":
    test_analyzers()
