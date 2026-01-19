# Machine Learning Models Directory

This directory contains the trained ML models for dyslexia and dysgraphia detection.

## Model Files

Place the following model files in this directory:

1. **dyslexia_eye_movement_model.keras** (76.4 MB)
   - Purpose: Analyzes eye movement patterns from handwriting samples
   - Used by: Handwriting analysis module
   - Format: Keras model file

2. **dyslexia_audio_lstm_model_v2.keras** (2.1 MB)
   - Purpose: Analyzes speech patterns and phoneme recognition
   - Used by: Speech analysis module
   - Format: Keras LSTM model file

3. **dysgraphia_model.h5** (76.4 MB)
   - Purpose: Detects dysgraphia from handwriting features
   - Used by: Handwriting analysis module
   - Format: HDF5 model file

## File Structure

```
ml_models/
├── README.md (this file)
├── dyslexia_eye_movement_model.keras
├── dyslexia_audio_lstm_model_v2.keras
└── dysgraphia_model.h5
```

## How to Add Models

1. Copy the three model files to this directory
2. Ensure the files have the exact names listed above
3. The models will be automatically loaded by the detection engine

## Model Loading

Models are loaded in:
- `detection_module/detection_engine.py`
- `handwriting_analysis/analyzer.py`
- `speech_analysis/analyzer.py`

## Notes

- These files are large and should NOT be committed to Git
- Add `ml_models/*.keras` and `ml_models/*.h5` to `.gitignore`
- For production, store models in cloud storage (S3, Google Cloud Storage, etc.)
