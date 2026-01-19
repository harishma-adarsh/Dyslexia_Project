
import os

file_path = 'user_interface/templates/user_interface/exercise_session.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Define the bad sequence
bad_seq = """<i class="fas fa-pen-nib me-2"></i> Word Count: <span id="word-count">0</span> / {{
                                    exercise.content.min_words }}"""

# Define the good sequence
good_seq = """<i class="fas fa-pen-nib me-2"></i> Word Count: <span id="word-count">0</span> / {{ exercise.content.min_words }}"""

# Normalize content to handle potential CRLF issues
content = content.replace(bad_seq, good_seq)

# Also try a regex approach just in case whitespace is slightly different
import re
pattern = re.compile(r'Word Count: <span id="word-count">0</span> / {{\s+exercise\.content\.min_words }}')
content = pattern.sub('Word Count: <span id="word-count">0</span> / {{ exercise.content.min_words }}', content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("File updated successfully.")
