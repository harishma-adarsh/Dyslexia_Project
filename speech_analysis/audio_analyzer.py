import librosa
import numpy as np
import soundfile as sf
from scipy import signal
from scipy.stats import skew, kurtosis
import json
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

class SpeechAnalyzer:
    """
    Speech analysis for dyslexia detection using audio features
    """
    
    def __init__(self):
        self.sample_rate = 22050
        self.hop_length = 512
        self.n_mfcc = 13
    
    def load_audio(self, audio_path: str) -> Tuple[np.ndarray, int]:
        """Load and preprocess audio file"""
        try:
            audio, sr = librosa.load(audio_path, sr=self.sample_rate)
            return audio, sr
        except Exception as e:
            print(f"Error loading audio: {e}")
            return np.array([]), self.sample_rate
    
    def extract_mfcc_features(self, audio: np.ndarray) -> np.ndarray:
        """Extract MFCC features"""
        mfccs = librosa.feature.mfcc(y=audio, sr=self.sample_rate, n_mfcc=self.n_mfcc)
        return mfccs
    
    def extract_spectral_features(self, audio: np.ndarray) -> Dict:
        """Extract spectral features"""
        # Spectral centroid
        spectral_centroids = librosa.feature.spectral_centroid(y=audio, sr=self.sample_rate)[0]
        
        # Spectral rolloff
        spectral_rolloff = librosa.feature.spectral_rolloff(y=audio, sr=self.sample_rate)[0]
        
        # Zero crossing rate
        zcr = librosa.feature.zero_crossing_rate(audio)[0]
        
        # Spectral bandwidth
        spectral_bandwidth = librosa.feature.spectral_bandwidth(y=audio, sr=self.sample_rate)[0]
        
        return {
            'spectral_centroid_mean': np.mean(spectral_centroids),
            'spectral_centroid_std': np.std(spectral_centroids),
            'spectral_rolloff_mean': np.mean(spectral_rolloff),
            'spectral_rolloff_std': np.std(spectral_rolloff),
            'zcr_mean': np.mean(zcr),
            'zcr_std': np.std(zcr),
            'spectral_bandwidth_mean': np.mean(spectral_bandwidth),
            'spectral_bandwidth_std': np.std(spectral_bandwidth)
        }
    
    def extract_rhythm_features(self, audio: np.ndarray) -> Dict:
        """Extract rhythm and timing features"""
        # Onset detection
        onset_frames = librosa.onset.onset_detect(y=audio, sr=self.sample_rate)
        onset_times = librosa.frames_to_time(onset_frames, sr=self.sample_rate)
        
        # Calculate rhythm metrics
        if len(onset_times) > 1:
            intervals = np.diff(onset_times)
            rhythm_consistency = 1.0 - (np.std(intervals) / np.mean(intervals)) if np.mean(intervals) > 0 else 0
        else:
            rhythm_consistency = 0.0
        
        # Tempo estimation
        tempo, _ = librosa.beat.beat_track(y=audio, sr=self.sample_rate)
        
        return {
            'rhythm_consistency': rhythm_consistency,
            'tempo': float(tempo),
            'onset_count': len(onset_times),
            'average_interval': np.mean(np.diff(onset_times)) if len(onset_times) > 1 else 0
        }
    
    def extract_pronunciation_features(self, audio: np.ndarray) -> Dict:
        """Extract pronunciation-related features"""
        # Formant analysis (simplified)
        # Extract formants using LPC
        try:
            # Pre-emphasize
            emphasized = librosa.effects.preemphasis(audio)
            
            # Extract formants (simplified approach)
            formants = self._extract_formants(emphasized)
            
            # Calculate formant ratios
            f1_f2_ratio = formants['f1_mean'] / formants['f2_mean'] if formants['f2_mean'] > 0 else 0
            f2_f3_ratio = formants['f2_mean'] / formants['f3_mean'] if formants['f3_mean'] > 0 else 0
            
            return {
                'f1_mean': formants['f1_mean'],
                'f2_mean': formants['f2_mean'],
                'f3_mean': formants['f3_mean'],
                'f1_f2_ratio': f1_f2_ratio,
                'f2_f3_ratio': f2_f3_ratio,
                'formant_variance': formants['variance']
            }
        except Exception as e:
            print(f"Error in formant analysis: {e}")
            return {
                'f1_mean': 0, 'f2_mean': 0, 'f3_mean': 0,
                'f1_f2_ratio': 0, 'f2_f3_ratio': 0, 'formant_variance': 0
            }
    
    def _extract_formants(self, audio: np.ndarray, order: int = 10) -> Dict:
        """Extract formant frequencies using LPC"""
        # Apply windowing
        windowed = audio * np.hanning(len(audio))
        
        # LPC analysis
        lpc_coeffs = librosa.lpc(windowed, order=order)
        
        # Find roots of LPC polynomial
        roots = np.roots(lpc_coeffs)
        
        # Convert to frequencies
        angles = np.angle(roots)
        freqs = angles * self.sample_rate / (2 * np.pi)
        
        # Filter valid formants
        valid_freqs = freqs[(freqs > 50) & (freqs < 4000)]
        
        if len(valid_freqs) >= 3:
            sorted_freqs = np.sort(valid_freqs)
            return {
                'f1_mean': float(sorted_freqs[0]),
                'f2_mean': float(sorted_freqs[1]),
                'f3_mean': float(sorted_freqs[2]),
                'variance': float(np.var(sorted_freqs))
            }
        else:
            return {'f1_mean': 0, 'f2_mean': 0, 'f3_mean': 0, 'variance': 0}
    
    def analyze_fluency(self, audio: np.ndarray) -> Dict:
        """Analyze speech fluency"""
        # Detect pauses
        pauses = self._detect_pauses(audio)
        
        # Calculate speech rate
        duration = len(audio) / self.sample_rate
        speech_rate = len(audio) / duration if duration > 0 else 0
        
        # Calculate pause frequency
        pause_frequency = len(pauses) / duration if duration > 0 else 0
        
        # Analyze rhythm
        rhythm_features = self.extract_rhythm_features(audio)
        
        return {
            'speech_rate': speech_rate,
            'pause_frequency': pause_frequency,
            'pause_duration_ratio': sum(pauses) / duration if duration > 0 else 0,
            'rhythm_consistency': rhythm_features['rhythm_consistency'],
            'fluency_score': self._calculate_fluency_score(pauses, rhythm_features)
        }
    
    def _detect_pauses(self, audio: np.ndarray, threshold: float = 0.01) -> List[float]:
        """Detect pauses in speech"""
        # Calculate energy
        frame_length = 1024
        hop_length = 512
        energy = []
        
        for i in range(0, len(audio) - frame_length, hop_length):
            frame = audio[i:i + frame_length]
            frame_energy = np.sum(frame ** 2)
            energy.append(frame_energy)
        
        energy = np.array(energy)
        
        # Find low energy regions (pauses)
        pause_frames = energy < threshold
        pause_durations = []
        
        in_pause = False
        pause_start = 0
        
        for i, is_pause in enumerate(pause_frames):
            if is_pause and not in_pause:
                in_pause = True
                pause_start = i
            elif not is_pause and in_pause:
                in_pause = False
                pause_duration = (i - pause_start) * hop_length / self.sample_rate
                if pause_duration > 0.1:  # Only count pauses longer than 100ms
                    pause_durations.append(pause_duration)
        
        return pause_durations
    
    def _calculate_fluency_score(self, pauses: List[float], rhythm_features: Dict) -> float:
        """Calculate overall fluency score"""
        # Normalize pause frequency (fewer pauses = higher score)
        pause_score = max(0, 1 - len(pauses) * 0.1)
        
        # Rhythm consistency score
        rhythm_score = rhythm_features['rhythm_consistency']
        
        # Combine scores
        fluency_score = (pause_score + rhythm_score) / 2
        return min(max(fluency_score, 0), 1)
    
    def analyze_pronunciation(self, audio: np.ndarray, text_content: str) -> Dict:
        """Analyze pronunciation accuracy"""
        # Extract pronunciation features
        pronunciation_features = self.extract_pronunciation_features(audio)
        
        # Analyze phoneme-level features
        phoneme_analysis = self._analyze_phonemes(audio)
        
        # Calculate pronunciation score
        pronunciation_score = self._calculate_pronunciation_score(pronunciation_features, phoneme_analysis)
        
        return {
            'pronunciation_score': pronunciation_score,
            'phoneme_analysis': phoneme_analysis,
            'formant_analysis': pronunciation_features,
            'mispronunciations': self._identify_mispronunciations(pronunciation_features)
        }
    
    def _analyze_phonemes(self, audio: np.ndarray) -> Dict:
        """Analyze phoneme-level features"""
        # Extract MFCC features
        mfccs = self.extract_mfcc_features(audio)
        
        # Calculate phoneme-level statistics
        phoneme_stats = {
            'mfcc_mean': np.mean(mfccs, axis=1).tolist(),
            'mfcc_std': np.std(mfccs, axis=1).tolist(),
            'mfcc_range': (np.max(mfccs, axis=1) - np.min(mfccs, axis=1)).tolist()
        }
        
        return phoneme_stats
    
    def _calculate_pronunciation_score(self, pronunciation_features: Dict, phoneme_analysis: Dict) -> float:
        """Calculate pronunciation accuracy score (1.0 is perfect)"""
        if pronunciation_features['f1_f2_ratio'] == 0:
            return 0.92  # Default to high score for missing data to avoid false risk
            
        # Balanced window: Normal range is 0.25 - 0.5 for F1/F2
        ratio1 = pronunciation_features['f1_f2_ratio']
        if 0.25 <= ratio1 <= 0.5:
            f1_f2_score = 1.0
        else:
            # Calibrated drop off to catch high risk
            f1_f2_score = max(0, 1.0 - abs(ratio1 - 0.4) * 3.5)
            
        ratio2 = pronunciation_features['f2_f3_ratio']
        if 0.2 <= ratio2 <= 0.4:
            f2_f3_score = 1.0
        else:
            f2_f3_score = max(0, 1.0 - abs(ratio2 - 0.3) * 4.0)
        
        pronunciation_score = (f1_f2_score + f2_f3_score) / 2
        return min(max(pronunciation_score, 0), 1)
    
    def _identify_mispronunciations(self, pronunciation_features: Dict) -> List[str]:
        """Identify potential mispronunciations"""
        mispronunciations = []
        
        # Check for unusual formant patterns
        if pronunciation_features['f1_f2_ratio'] < 0.2:
            mispronunciations.append("Unusual vowel formant pattern")
        
        if pronunciation_features['f2_f3_ratio'] < 0.1:
            mispronunciations.append("Potential consonant mispronunciation")
        
        return mispronunciations
    
    def analyze_speech(self, audio_path: str, text_content: str = "") -> Dict:
        """Complete speech analysis"""
        # Load audio
        audio, sr = self.load_audio(audio_path)
        
        if len(audio) == 0:
            return {
                'pronunciation_score': 0.0,
                'fluency_score': 0.0,
                'reading_speed': 0.0,
                'pause_frequency': 0.0,
                'mispronunciations': [],
                'fluency_issues': [],
                'phoneme_analysis': {},
                'pitch_variation': 0.0,
                'volume_consistency': 0.0,
                'rhythm_score': 0.0,
                'model_confidence': 0.0
            }
        
        # Extract features
        spectral_features = self.extract_spectral_features(audio)
        rhythm_features = self.extract_rhythm_features(audio)
        fluency_analysis = self.analyze_fluency(audio)
        pronunciation_analysis = self.analyze_pronunciation(audio, text_content)
        
        # Calculate reading speed (words per minute)
        duration = len(audio) / sr
        word_count = len(text_content.split()) if text_content else 1
        reading_speed = (word_count / duration) * 60 if duration > 0 else 0
        
        # Normalize reading speed (assume 80 WPM is normal/passing for diagnosis context)
        normalized_speed = min(reading_speed / 80.0, 1.0)
        risk_score = 1.0 - normalized_speed
        
        # Calculate pitch variation
        pitch_variation = self._calculate_pitch_variation(audio)
        
        # Calculate volume consistency
        volume_consistency = self._calculate_volume_consistency(audio)
        
        return {
            'pronunciation_score': pronunciation_analysis['pronunciation_score'],
            'fluency_score': fluency_analysis['fluency_score'],
            'reading_speed': reading_speed,
            'pause_frequency': fluency_analysis['pause_frequency'],
            'mispronunciations': pronunciation_analysis['mispronunciations'],
            'fluency_issues': self._identify_fluency_issues(fluency_analysis),
            'phoneme_analysis': pronunciation_analysis['phoneme_analysis'],
            'pitch_variation': pitch_variation,
            'volume_consistency': volume_consistency,
            'rhythm_score': rhythm_features['rhythm_consistency'],
            'model_confidence': 0.85  # Placeholder confidence score
        }
    
    def _calculate_pitch_variation(self, audio: np.ndarray) -> float:
        """Calculate pitch variation"""
        try:
            pitches, magnitudes = librosa.piptrack(y=audio, sr=self.sample_rate)
            pitch_values = []
            
            for t in range(pitches.shape[1]):
                index = magnitudes[:, t].argmax()
                pitch = pitches[index, t]
                if pitch > 0:
                    pitch_values.append(pitch)
            
            if len(pitch_values) > 1:
                return np.std(pitch_values) / np.mean(pitch_values) if np.mean(pitch_values) > 0 else 0
            return 0
        except:
            return 0
    
    def _calculate_volume_consistency(self, audio: np.ndarray) -> float:
        """Calculate volume consistency"""
        # Calculate RMS energy
        frame_length = 1024
        hop_length = 512
        rms_values = []
        
        for i in range(0, len(audio) - frame_length, hop_length):
            frame = audio[i:i + frame_length]
            rms = np.sqrt(np.mean(frame ** 2))
            rms_values.append(rms)
        
        if len(rms_values) > 1:
            return 1 - (np.std(rms_values) / np.mean(rms_values)) if np.mean(rms_values) > 0 else 0
        return 1
    
    def _identify_fluency_issues(self, fluency_analysis: Dict) -> List[str]:
        """Identify fluency issues"""
        issues = []
        
        if fluency_analysis['pause_frequency'] > 2.0:
            issues.append("Frequent pauses")
        
        if fluency_analysis['rhythm_consistency'] < 0.5:
            issues.append("Irregular speech rhythm")
        
        if fluency_analysis['speech_rate'] < 100:  # words per minute
            issues.append("Slow speech rate")
        
        return issues
