from detection_module.models import DetectionResult

def detection_status(request):
    if request.user.is_authenticated:
        # Check if any detection exists with a significant risk score or just if any exists
        # Usually "detected" means risk is not "low" or dyslexia/dysgraphia prob > 0.4
        latest_detection = DetectionResult.objects.filter(user=request.user).order_by('-detection_timestamp').first()
        
        has_detection = False
        if latest_detection:
            # You can adjust this logic: show training if risk is medium/high 
            # or if any probability is > 40%
            if latest_detection.risk_level in ['medium', 'high'] or \
               latest_detection.dyslexia_probability > 0.4 or \
               latest_detection.dysgraphia_probability > 0.4:
                has_detection = True
        
        return {
            'has_detection': has_detection,
            'latest_detection_result': latest_detection
        }
    return {}
