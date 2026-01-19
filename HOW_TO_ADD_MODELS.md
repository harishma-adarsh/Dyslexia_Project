# How to Add ML Model Files to Your Project

## 📋 Overview

You have three machine learning model files that need to be integrated into your Dyslexia Helper project:

1. **dyslexia_eye_movement_model.keras** (76.4 MB)
2. **dyslexia_audio_lstm_model_v2.keras** (2.1 MB)
3. **dysgraphia_model.h5** (76.4 MB)

## 🚀 Quick Start Guide

### Step 1: Copy Model Files

Copy the three model files to the `ml_models` directory:

```
Project_ Dyslexia/
└── Dyslexia/
    └── ml_models/              ← Copy files here
        ├── dyslexia_eye_movement_model.keras
        ├── dyslexia_audio_lstm_model_v2.keras
        └── dysgraphia_model.h5
```

**Windows Command:**
```powershell
# Navigate to your project directory
cd "C:\Harishma\Maitexa\Project_ Dyslexia\Dyslexia"

# Copy files (replace SOURCE_PATH with actual location)
copy "C:\path\to\dyslexia_eye_movement_model.keras" "ml_models\"
copy "C:\path\to\dyslexia_audio_lstm_model_v2.keras" "ml_models\"
copy "C:\path\to\dysgraphia_model.h5" "ml_models\"
```

**Or use File Explorer:**
1. Open File Explorer
2. Navigate to where your model files are located
3. Copy all three files
4. Navigate to: `C:\Harishma\Maitexa\Project_ Dyslexia\Dyslexia\ml_models`
5. Paste the files

### Step 2: Verify Installation

Run the model check command:

```bash
python manage.py check_models
```

You should see:
```
============================================================
ML Models Status Check
============================================================

EYE MOVEMENT:
  Path: C:\...\ml_models\dyslexia_eye_movement_model.keras
  ✓ Status: Available
  Size: 76.42 MB
  Loaded: No

AUDIO LSTM:
  Path: C:\...\ml_models\dyslexia_audio_lstm_model_v2.keras
  ✓ Status: Available
  Size: 2.15 MB
  Loaded: No

DYSGRAPHIA:
  Path: C:\...\ml_models\dysgraphia_model.h5
  ✓ Status: Available
  Size: 76.41 MB
  Loaded: No

============================================================
Available Models: 3/3
✓ All models are available!
============================================================
```

### Step 3: Install Required Dependencies

Make sure TensorFlow is installed:

```bash
pip install tensorflow
```

Or if you prefer the CPU-only version (smaller):

```bash
pip install tensorflow-cpu
```

## 📁 Project Structure

After adding the files, your structure should look like:

```
Project_ Dyslexia/
└── Dyslexia/
    ├── ml_models/
    │   ├── __init__.py
    │   ├── model_loader.py
    │   ├── README.md
    │   ├── dyslexia_eye_movement_model.keras    ← Your file
    │   ├── dyslexia_audio_lstm_model_v2.keras   ← Your file
    │   └── dysgraphia_model.h5                  ← Your file
    ├── detection_module/
    ├── handwriting_analysis/
    ├── speech_analysis/
    └── ...
```

## 🔧 How to Use Models in Code

### Loading a Model

```python
from ml_models import load_model

# Load eye movement model
eye_model = load_model('eye_movement')

# Load audio LSTM model
audio_model = load_model('audio_lstm')

# Load dysgraphia model
dysgraphia_model = load_model('dysgraphia')
```

### Check if Model is Available

```python
from ml_models import is_model_available

if is_model_available('eye_movement'):
    print("Eye movement model is ready!")
else:
    print("Please add the eye movement model file")
```

### Get All Available Models

```python
from ml_models import get_available_models

available = get_available_models()
print(f"Available models: {available}")
# Output: ['eye_movement', 'audio_lstm', 'dysgraphia']
```

## 🎯 Integration with Existing Code

The models will be automatically used by:

1. **Handwriting Analysis** (`handwriting_analysis/analyzer.py`)
   - Uses: `eye_movement` and `dysgraphia` models
   
2. **Speech Analysis** (`speech_analysis/analyzer.py`)
   - Uses: `audio_lstm` model
   
3. **Detection Engine** (`detection_module/detection_engine.py`)
   - Combines results from all models

## ⚠️ Important Notes

### File Size Considerations

- Total size: ~155 MB
- These files are **NOT** committed to Git (already in `.gitignore`)
- For production deployment, consider:
  - Cloud storage (AWS S3, Google Cloud Storage)
  - Model versioning systems
  - Lazy loading to save memory

### Memory Management

Models are cached after first load. To clear cache:

```python
from ml_models import clear_model_cache
clear_model_cache()
```

### Error Handling

If a model file is missing, the system will:
- Log a warning
- Continue without the model
- Use fallback detection methods

## 🧪 Testing

Test if models load correctly:

```python
# In Django shell
python manage.py shell

>>> from ml_models import load_model, get_model_info
>>> 
>>> # Check model info
>>> info = get_model_info()
>>> print(info)
>>> 
>>> # Try loading a model
>>> model = load_model('eye_movement')
>>> print(f"Model loaded: {model is not None}")
```

## 🚨 Troubleshooting

### Problem: "Model file not found"

**Solution:**
- Check file names are exactly correct (case-sensitive)
- Verify files are in `ml_models/` directory
- Run `python manage.py check_models` to see paths

### Problem: "TensorFlow not installed"

**Solution:**
```bash
pip install tensorflow
```

### Problem: "Out of memory"

**Solution:**
- Models are large (76 MB each)
- Close other applications
- Use lazy loading (models load only when needed)
- Consider using TensorFlow Lite for smaller models

### Problem: "Model won't load"

**Solution:**
- Ensure TensorFlow version compatibility
- Check if files are corrupted (re-download)
- Verify file extensions (.keras, .h5)

## 📚 Additional Resources

- TensorFlow Documentation: https://www.tensorflow.org/
- Keras Model Saving: https://keras.io/guides/serialization_and_saving/
- Django Management Commands: https://docs.djangoproject.com/en/stable/howto/custom-management-commands/

## ✅ Checklist

- [ ] Created `ml_models/` directory
- [ ] Copied all 3 model files to `ml_models/`
- [ ] Verified file names are correct
- [ ] Installed TensorFlow (`pip install tensorflow`)
- [ ] Ran `python manage.py check_models`
- [ ] All models show as "Available"
- [ ] Tested loading a model in Django shell

---

**Need Help?** Check the logs or run the model check command for detailed status information.
