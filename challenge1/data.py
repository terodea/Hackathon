"""Routines associated with the application data.
"""
import json, os
courses = {}

def load_data():
    """Load the data from the json file.
    """
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    with open(SITE_ROOT + "/json/course.json") as out_file:
        data = json.load(out_file)

    for each_record in data:
        courses[each_record['id']] = each_record
    return data
    
if __name__ == '__main__':
    load_data()