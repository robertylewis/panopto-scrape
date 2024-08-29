import json
import yaml
from datetime import datetime

# Load the JSON file
with open('panopto.json', 'r') as json_file:
    data = json.load(json_file)

# Group sessions by course code
courses = {}
for result in data['d']['Results']:
    folder_name = result['FolderName']
    course_code = folder_name.split('-')[1].strip()
    if course_code not in courses:
        courses[course_code] = []
    courses[course_code].append(result)

# Convert sessions to YAML format
for course_code, sessions in courses.items():
    yaml_data = []
    for session in sessions:
        session_date = datetime.fromtimestamp(int(session['StartTime'][6:-5])).strftime('%B %d')
        topic = "Topic description here"  # Replace with actual topic description or link
        recording_id = session["DeliveryID"]
        
        yaml_data.append({
            'date': session_date,
            # 'topic': topic,
            'recording': recording_id
        })

    yaml_data_sorted = sorted(yaml_data, key=lambda x: datetime.strptime(x['date'], '%B %d'))

    yaml_filename = f'{course_code.lower()}_lectures.yaml'
    with open(yaml_filename, 'w') as yaml_file:
        yaml.dump({'lectures': yaml_data_sorted}, yaml_file, default_flow_style=False)

    print(f'Saved {yaml_filename}')
