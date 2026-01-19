import os

file_path = r'c:\Harishma\Maitexa\Project_ Dyslexia\Dyslexia\user_interface\templates\user_interface\detection_results.html'

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip_next = False

for i in range(len(lines)):
    if skip_next:
        skip_next = False
        continue
        
    line = lines[i]
    
    # Fix the specific if statement split
    if "{% if result.risk_level in 'medium,high' or result.dyslexia_probability > 0.4 or" in line and i + 1 < len(lines) and "result.dysgraphia_probability > 0.4 %}" in lines[i+1]:
        merged = line.strip() + " " + lines[i+1].strip() + "\n"
        new_lines.append(merged)
        skip_next = True
    # Fix confidence split
    elif "Detection Confidence:</strong> {{" in line and i + 1 < len(lines) and "result.detection_confidence|floatformat:1 }}" in lines[i+1]:
        merged = line.strip() + " " + lines[i+1].strip() + " </small>\n"
        # Since line 121 has indentation, we should keep it
        indent = line[:line.find("<small>")]
        new_lines.append(indent + merged)
        skip_next = True
    # Fix date split
    elif "Analysis Date:</strong> {{ result.detection_timestamp|date:\"M d, Y" in line and i + 1 < len(lines) and "H:i\" }}" in lines[i+1]:
        merged = line.strip() + " " + lines[i+1].strip() + " </small>\n"
        indent = line[:line.find("<small>")]
        new_lines.append(indent + merged)
        skip_next = True
    else:
        new_lines.append(line)

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Template tags fixed.")
