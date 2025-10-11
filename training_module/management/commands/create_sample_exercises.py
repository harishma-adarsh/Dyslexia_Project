from django.core.management.base import BaseCommand
from training_module.models import Exercise

class Command(BaseCommand):
    help = 'Create sample exercises for the training module'

    def handle(self, *args, **options):
        # Reading exercises
        reading_exercises = [
            {
                'name': 'Letter Recognition Game',
                'exercise_type': 'reading',
                'difficulty_level': 'beginner',
                'description': 'Match letters with their sounds and pictures!',
                'instructions': 'Look at each letter and click on the matching picture. Take your time!',
                'content': {
                    'type': 'letter_matching',
                    'letters': ['A', 'B', 'C', 'D', 'E'],
                    'images': ['apple', 'ball', 'cat', 'dog', 'elephant']
                },
                'expected_duration': 10
            },
            {
                'name': 'Word Building Challenge',
                'exercise_type': 'reading',
                'difficulty_level': 'intermediate',
                'description': 'Build words by combining letters and sounds!',
                'instructions': 'Drag and drop letters to form the word shown in the picture.',
                'content': {
                    'type': 'word_building',
                    'words': ['cat', 'dog', 'sun', 'moon', 'tree'],
                    'letters': ['c', 'a', 't', 'd', 'o', 'g', 's', 'u', 'n', 'm', 'o', 'o', 'n', 't', 'r', 'e', 'e']
                },
                'expected_duration': 15
            },
            {
                'name': 'Reading Comprehension Adventure',
                'exercise_type': 'comprehension',
                'difficulty_level': 'advanced',
                'description': 'Read stories and answer questions to test your understanding!',
                'instructions': 'Read the story carefully, then answer the questions about what happened.',
                'content': {
                    'type': 'comprehension',
                    'stories': [
                        {
                            'title': 'The Little Red Hen',
                            'text': 'Once upon a time, there was a little red hen who lived on a farm...',
                            'questions': [
                                'What color was the hen?',
                                'Where did the hen live?',
                                'What did the hen want to do?'
                            ]
                        }
                    ]
                },
                'expected_duration': 20
            }
        ]

        # Writing exercises
        writing_exercises = [
            {
                'name': 'Letter Tracing Practice',
                'exercise_type': 'writing',
                'difficulty_level': 'beginner',
                'description': 'Practice writing letters by tracing them!',
                'instructions': 'Follow the dotted lines to trace each letter. Go slowly and carefully!',
                'content': {
                    'type': 'letter_tracing',
                    'letters': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
                    'tracing_style': 'dotted'
                },
                'expected_duration': 15
            },
            {
                'name': 'Word Writing Challenge',
                'exercise_type': 'writing',
                'difficulty_level': 'intermediate',
                'description': 'Write words by copying them carefully!',
                'instructions': 'Look at each word and write it in the space provided. Make sure your letters are clear!',
                'content': {
                    'type': 'word_copying',
                    'words': ['cat', 'dog', 'sun', 'moon', 'tree', 'house', 'car', 'book'],
                    'font_size': 'large'
                },
                'expected_duration': 20
            },
            {
                'name': 'Story Writing Adventure',
                'exercise_type': 'writing',
                'difficulty_level': 'advanced',
                'description': 'Write your own short story using the given words!',
                'instructions': 'Use the provided words to write a creative story. Be as imaginative as you want!',
                'content': {
                    'type': 'creative_writing',
                    'prompt_words': ['magic', 'forest', 'friend', 'adventure', 'treasure'],
                    'min_words': 50
                },
                'expected_duration': 25
            }
        ]

        # Phoneme exercises
        phoneme_exercises = [
            {
                'name': 'Sound Matching Game',
                'exercise_type': 'phoneme',
                'difficulty_level': 'beginner',
                'description': 'Match sounds with letters and words!',
                'instructions': 'Listen to each sound and click on the matching letter or word.',
                'content': {
                    'type': 'sound_matching',
                    'sounds': ['/a/', '/b/', '/c/', '/d/', '/e/'],
                    'targets': ['A', 'B', 'C', 'D', 'E']
                },
                'expected_duration': 12
            },
            {
                'name': 'Rhyming Word Hunt',
                'exercise_type': 'phoneme',
                'difficulty_level': 'intermediate',
                'description': 'Find words that rhyme with the given word!',
                'instructions': 'Look at the word and find all the words that rhyme with it.',
                'content': {
                    'type': 'rhyming',
                    'base_words': ['cat', 'dog', 'sun', 'moon', 'tree'],
                    'options': ['hat', 'frog', 'fun', 'spoon', 'free', 'bat', 'log', 'run', 'tune', 'bee']
                },
                'expected_duration': 18
            },
            {
                'name': 'Phoneme Blending Challenge',
                'exercise_type': 'phoneme',
                'difficulty_level': 'advanced',
                'description': 'Blend sounds together to make words!',
                'instructions': 'Listen to the individual sounds and blend them together to form a word.',
                'content': {
                    'type': 'blending',
                    'sound_sequences': [
                        ['/c/', '/a/', '/t/'],
                        ['/d/', '/o/', '/g/'],
                        ['/s/', '/u/', '/n/']
                    ],
                    'target_words': ['cat', 'dog', 'sun']
                },
                'expected_duration': 20
            }
        ]

        # Create all exercises
        all_exercises = reading_exercises + writing_exercises + phoneme_exercises
        
        created_count = 0
        for exercise_data in all_exercises:
            exercise, created = Exercise.objects.get_or_create(
                name=exercise_data['name'],
                defaults=exercise_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created exercise: {exercise.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Exercise already exists: {exercise.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} new exercises!')
        )
