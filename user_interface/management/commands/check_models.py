"""
Django management command to check ML model status
Usage: python manage.py check_models
"""

from django.core.management.base import BaseCommand
from ml_models import get_model_info, get_available_models


class Command(BaseCommand):
    help = 'Check the status of ML models'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('ML Models Status Check'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write('')
        
        model_info = get_model_info()
        available_models = get_available_models()
        
        for model_name, info in model_info.items():
            self.stdout.write(f"\n{model_name.upper().replace('_', ' ')}:")
            self.stdout.write(f"  Path: {info['path']}")
            
            if info['exists']:
                self.stdout.write(self.style.SUCCESS(f"  ✓ Status: Available"))
                self.stdout.write(f"  Size: {info['size_mb']} MB")
                self.stdout.write(f"  Loaded: {'Yes' if info['loaded'] else 'No'}")
            else:
                self.stdout.write(self.style.ERROR(f"  ✗ Status: NOT FOUND"))
                self.stdout.write(self.style.WARNING(f"  → Please copy the model file to: {info['path']}"))
        
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(f"Available Models: {len(available_models)}/{len(model_info)}")
        
        if len(available_models) == len(model_info):
            self.stdout.write(self.style.SUCCESS("✓ All models are available!"))
        elif len(available_models) > 0:
            self.stdout.write(self.style.WARNING(f"⚠ {len(model_info) - len(available_models)} model(s) missing"))
        else:
            self.stdout.write(self.style.ERROR("✗ No models found! Please add model files."))
        
        self.stdout.write(self.style.SUCCESS('=' * 60))
