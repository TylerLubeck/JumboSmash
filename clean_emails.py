import re
import json


def should_keep(data):
    match_string = '.*?\(([a-zA-Z]*?)\)'
    rg = re.compile(match_string, re.IGNORECASE | re.DOTALL)
    ok_degrees = ['BA', 'BS', 'BFA']

    if data['major'] == 'International Relations':
        return True

    match = rg.search(data['major'])
    if match:
        for degree in ok_degrees:
            if match.group(1).startswith(degree):
                return True

    return False

if __name__ == '__main__':
    with open('emails.json') as f:
        data = json.load(f)

    new_data = [d for d in data if should_keep(d)]

    for d in new_data:
        d['class_year'] = int(d['class_year']) + 2000

    with open('cleaned_emails.json', 'w') as f:
        json.dump(new_data, f)
