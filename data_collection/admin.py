from django.contrib import admin
from .models import UserProfile, HandwritingSample, SpeechSample, VideoSample, EyeTrackingData

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'grade_level', 'created_at')
    search_fields = ('user__username', 'grade_level')

@admin.register(HandwritingSample)
class HandwritingSampleAdmin(admin.ModelAdmin):
    list_display = ('user', 'id', 'timestamp')
    search_fields = ('user__username', 'text_content')

@admin.register(SpeechSample)
class SpeechSampleAdmin(admin.ModelAdmin):
    list_display = ('user', 'id', 'timestamp')
    search_fields = ('user__username', 'text_content')

@admin.register(VideoSample)
class VideoSampleAdmin(admin.ModelAdmin):
    list_display = ('user', 'id', 'timestamp')
    search_fields = ('user__username', 'description')

admin.site.register(EyeTrackingData)
