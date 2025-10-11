# 🌟 Dyslexia Detection & Training System

A comprehensive Django-based system for detecting dyslexia/dysgraphia and providing interactive training exercises for children.

## 🚀 Features

### 📊 Data Collection
- **Handwriting Sample Upload**: Upload images of handwriting with text content
- **Speech Recording Upload**: Upload audio recordings with transcriptions
- **Eye Tracking Support**: Optional eye tracking coordinate capture
- **Secure File Storage**: All samples stored securely with user authentication

### ✍️ Handwriting Analysis
- **CNN-based Detection**: Analyzes irregular letter shapes and stroke patterns
- **Spacing Analysis**: Detects spacing issues between letters and words
- **Quality Scoring**: Overall handwriting quality assessment
- **Detailed Reports**: Specific recommendations for improvement

### 🎤 Speech Analysis
- **Audio Feature Extraction**: MFCC, spectral, and rhythm analysis
- **Pronunciation Assessment**: Identifies mispronunciations and fluency issues
- **Reading Speed Analysis**: Calculates words per minute
- **Phoneme Analysis**: Detailed speech pattern recognition

### 🧠 Detection Module
- **Combined Risk Assessment**: Integrates handwriting and speech analysis
- **Risk Level Classification**: Low, Medium, High risk categories
- **Personalized Recommendations**: Tailored suggestions for improvement
- **Progress Tracking**: Long-term monitoring of development

### 🎮 Training Module
- **Interactive Exercises**: 9 different learning activities
- **Adaptive Difficulty**: Adjusts based on user performance
- **Progress Tracking**: Mastery levels and achievement tracking
- **Exercise Types**:
  - Reading exercises (letter recognition, word building, comprehension)
  - Writing exercises (letter tracing, word copying, creative writing)
  - Phoneme exercises (sound matching, rhyming, blending)

### 👶 Child-Friendly Interface
- **Colorful Design**: Engaging visual interface with emojis
- **Simple Navigation**: Easy-to-use interface for children
- **Drag & Drop Upload**: Intuitive file upload system
- **Progress Visualization**: Clear progress indicators and achievements
- **Encouraging Feedback**: Positive reinforcement throughout

## 🛠️ Technology Stack

- **Backend**: Django 5.2.7
- **Database**: SQLite (easily configurable for PostgreSQL/MySQL)
- **AI/ML**: TensorFlow, OpenCV, Librosa, Scikit-learn
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Audio Processing**: Librosa, SoundFile
- **Image Processing**: OpenCV, Pillow

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Dyslexia
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create sample exercises**
   ```bash
   python manage.py create_sample_exercises
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start development server**
   ```bash
   python manage.py runserver
   ```

## 🎯 Usage

### For Users
1. **Register/Login**: Create an account or login
2. **Upload Samples**: Upload handwriting images and speech recordings
3. **Run Analysis**: Get AI-powered dyslexia/dysgraphia detection
4. **Practice**: Use interactive training exercises
5. **Track Progress**: Monitor improvement over time

### For Administrators
- Access Django admin at `/admin/`
- Manage users, exercises, and analysis results
- View system statistics and user progress

## 📱 User Interface

### Home Dashboard
- Welcome screen with quick access to all features
- Recent activity summary
- Progress overview

### Upload Interface
- Drag-and-drop file uploads
- Visual feedback for successful uploads
- Support for multiple file formats

### Training Exercises
- 9 different exercise types
- Adaptive difficulty levels
- Real-time progress tracking
- Achievement system

### Analysis Results
- Clear risk level indicators
- Personalized recommendations
- Detailed analysis breakdown
- Progress over time

## 🔧 Configuration

### Settings
- Database configuration in `settings.py`
- Media file handling
- Static file serving
- Security settings

### Customization
- Exercise content in `training_module/management/commands/`
- UI templates in `user_interface/templates/`
- Analysis algorithms in respective modules

## 📊 Database Schema

### Core Models
- **UserProfile**: User information and preferences
- **HandwritingSample**: Handwriting images and metadata
- **SpeechSample**: Audio recordings and transcriptions
- **HandwritingAnalysis**: CNN analysis results
- **SpeechAnalysis**: Audio feature analysis
- **DetectionResult**: Combined risk assessment
- **Exercise**: Training activities
- **UserProgress**: Individual progress tracking
- **ExerciseSession**: Session data and performance

## 🎨 Design Features

### Child-Friendly Elements
- Bright, colorful interface
- Large, easy-to-read fonts
- Emoji integration for engagement
- Simple navigation structure
- Encouraging messages and feedback

### Responsive Design
- Mobile-friendly interface
- Bootstrap 5 framework
- Adaptive layouts
- Touch-friendly controls

## 🔒 Security Features

- User authentication and authorization
- Secure file upload handling
- Data validation and sanitization
- CSRF protection
- SQL injection prevention

## 📈 Performance

- Optimized database queries
- Efficient file handling
- Caching for static content
- Background processing for analysis

## 🚀 Deployment

### Production Setup
1. Configure production database
2. Set up static file serving
3. Configure media file storage
4. Set up SSL/HTTPS
5. Configure environment variables

### Scaling Considerations
- Database optimization
- File storage solutions (AWS S3, etc.)
- Load balancing for multiple users
- Caching strategies

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Check the documentation
- Review the code comments
- Open an issue on GitHub
- Contact the development team

## 🎯 Future Enhancements

- Advanced ML models
- Mobile app development
- Real-time collaboration features
- Advanced analytics dashboard
- Integration with educational platforms
- Multi-language support

---

**Built with ❤️ for helping children with dyslexia and dysgraphia**
