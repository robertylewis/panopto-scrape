import yaml
from datetime import datetime

class folded_str(str): pass

# class literal_str(str): pass

# def change_style(style, representer):
#     def new_representer(dumper, data):
#         scalar = representer(dumper, data)
#         scalar.style = style
#         return scalar
#     return new_representer

def str_presenter(dumper, data):
    try:
        dlen = len(data.splitlines())
        if (dlen > 1):
            return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    except TypeError as ex:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data)
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

yaml.add_representer(str, str_presenter)

# Load the lecture data from csci_1951x_lectures.yaml
with open('csci 1951x_lectures.yaml', 'r') as yaml_file:
    csci_1951x_lectures = yaml.safe_load(yaml_file)['lectures']

# Load the current lectures.yaml content
with open('lecture.yaml', 'r') as yaml_file:
    lectures_yaml = yaml.safe_load(yaml_file)

# Create a mapping of dates to recording URLs from csci_1951x_lectures.yaml
date_to_recording = {lecture['date']: lecture['recording'] for lecture in csci_1951x_lectures}

# Update recording URLs in lectures.yaml based on the mapping
for lecture in lectures_yaml['lectures']:
    lecture_date = datetime.strptime(lecture['date'], '%m/%d').strftime('%B %d')
    if lecture_date in date_to_recording:
        lecture['recording'] = {'url': date_to_recording[lecture_date]}

# Save the updated lectures.yaml content
with open('lecture.yaml', 'w') as yaml_file:
    yaml.dump(lectures_yaml, yaml_file, default_flow_style=False)

print('Updated lecture.yaml')
