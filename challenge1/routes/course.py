"""Routes for the course resource.
"""
from configs.log import loggerClass
from configs.course_config import CourseConstants
from configs.data_model import ValidateDataModel
from run import app
from flask import request, jsonify
from http import HTTPStatus
import data
from datetime import datetime

lg = loggerClass()
all_courses = data.load_data()
courses = data.courses.copy()



@app.route("/course/<int:id>", methods=['GET'])
def get_course(id):
    """Get a course

    :param int id: The record id.
    :return: A single course (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------   
    1. Bonus points for not using a linear scan on your data structure.
    """
    # YOUR CODE HERE
    try:
        try:
            course_details = courses[id]
        except KeyError:
            lg.logger.error(f"GET FAILED[404] KeyNotFound Error !! Course Id: {id}")
            return jsonify({"message": f"Course {str(id)} does not exist"}), 404

        lg.logger.info(f"GET SUCCESS[200]: Processed Course Id: {id}")
        return jsonify({"data": course_details}), 200
    except Exception as e:
        lg.logger.error(msg=e, exc_info=True)
        raise e


@app.route("/course", methods=['GET'])
def get_courses():
    """Get a page of courses, optionally filtered by title words (a list of
    words separated by commas".

    Query parameters: page-number, page-size, title-words
    If not present, we use defaults of page-number=1, page-size=10

    :return: A page of courses (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    ------------------------------------------------------------------------- 
    1. Bonus points for not using a linear scan, on your data structure, if
       title-words is supplied. (USE Inverted Index)
    2. Bonus points for returning resulted sorted by the number of words which
       matched, if title-words is supplied.
    3. Bonus points for including performance data on the API, in terms of
       requests/second.
    """
    # YOUR CODE HERE
    try:
        title_words = []
        metadata = {'record_count': len(all_courses)}
        page_number = int(request.args.get('page-number', 1))
        page_size = int(request.args.get('page-size', 10))
        start_index = page_size*page_number-page_size
        end_index = start_index+page_size
        if request.args.get('title-words') is not None:
            title_words = request.args.get('title-words').split(',')
        filtered_courses = []
        sliced_courses = []
        if title_words:
            for course in all_courses:
                title = course["title"]
                for word in title_words:
                    if word.lower() in title.lower():
                        filtered_courses.append(course)
        if not filtered_courses and title_words:
            lg.logger.error(f"Courses Not Available!! ")
            return jsonify(({"message": "No courses available"})), 404
        elif not title_words:
            sliced_courses = all_courses[start_index:end_index]
        else:
            sliced_courses = filtered_courses[start_index:end_index]

        metadata["page_size"] = page_size
        metadata["page_number"] = page_number
        metadata["page_count"] = int(metadata["record_count"] / metadata["page_size"])
        if sliced_courses:
            return jsonify({"data": sliced_courses, "metadata": metadata}), 200
        elif filtered_courses:
            return jsonify({"data": filtered_courses, "metadata": metadata}), 200
        
        lg.logger.error(f"No Courses Available")
        return jsonify(({"message": "No courses available"})), 404
    except Exception as e:
        lg.logger.error(msg=e, exc_info=True)
        raise e


@app.route("/course", methods=['POST'])
def create_course():
    """Create a course.
    :return: The course object (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    1. Bonus points for validating the POST body fields
    """
    # YOUR CODE HERE
    try:
        post_data = request.get_json(force=True)
        create_course_schema = ValidateDataModel()
        errors = create_course_schema.validate(post_data)
        if errors:
            error_message = ''
            for key in errors:
                error_message += errors[key][0] + " "
            lg.logger.error(f"In valid data/message format - {error_message}")
            return jsonify(({"message": error_message})), 400

        data = post_data
        data['id'] = all_courses[-1]['id'] + 1
        data['date-created'] = datetime.now().strftime(CourseConstants.DATE_FORMAT)
        data['date-updated'] = datetime.now().strftime(CourseConstants.DATE_FORMAT)
        all_courses.append(data)
        courses[data["id"]] = data

        return jsonify({"data": data}), 201
    except Exception as e:
        lg.logger.error(msg=e, exc_info=True)
        raise e


@app.route("/course/<int:id>", methods=['PUT'])
def update_course(id):
    """Update a a course.
    :param int id: The record id.
    :return: The updated course object (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    1. Bonus points for validating the PUT body fields, including checking
       against the id in the URL

    """
    # YOUR CODE HERE
    try:
        _data = request.get_json(force=True)
        create_course_schema = ValidateDataModel()
        errors = create_course_schema.validate(_data)
        if errors:
            error_message = ''
            for key in errors:
                error_message += errors[key][0] + " "
            lg.logger.warning(f"In valid data/message format - {error_message}")
            return jsonify(({"message": error_message})), 400
        try:
            course_index = binary_search(arr=all_courses, low=0, high=len(all_courses) -1 , x=int(id))
        except KeyError:
            lg.logger.warning(f"No data found for id {id} in the payload")
            return jsonify({"message": "The id does not match the payload"}), 400
        if course_index == -1:
            lg.logger.warning(f"No data found for id {id} in the payload")
            return jsonify({"message": "The id does not match the payload"}), 400
        else:
            data = _data.copy()
            data["id"] = int(data["id"])
            updated_course = {
                **courses[course_index],
                **data,
                'date-updated': datetime.now().strftime(CourseConstants.DATE_FORMAT)
                }
            all_courses[course_index] = updated_course
            courses[id] = update_course
            return jsonify({"data": updated_course}), 200

    except Exception as e:
        lg.logger.error(msg=e, exc_info=True)
        raise e


@app.route("/course/<int:id>", methods=['DELETE'])
def delete_course(id):
    """Delete a course
    :return: A confirmation message (see the challenge notes for examples)
    """
    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    None
    """
    # YOUR CODE HERE
    try:
        try:
            course_location = binary_search(arr=all_courses, low=0, high=len(all_courses), x=int(id))
            if course_location:
                del all_courses[course_location]
                courses.pop(id)
                return jsonify({"message": "The specified course was deleted"}), 200
            else:
                lg.logger.warning(f"No data found for id {id} in the payload")
                return jsonify({"message": f"Course {id} does not exist"}), 404
        except KeyError:
            lg.logger.warning(f"No data found for id {id} in the payload")
            return jsonify({"message": f"Course {id} does not exist"}), 404
    except Exception as e:
        lg.logger.error(msg=e, exc_info=True)
        raise e


def binary_search(arr, low, high, x):
 
    # Check base case
    if high >= low:
        mid = (high + low) // 2
        # If element is present at the middle itself
        if arr[mid]["id"] == x:
            return mid
        # If element is smaller than mid, then it can only
        # be present in left subarray
        elif arr[mid]["id"] > x:
            return binary_search(arr, low, mid - 1, x)
        # Else the element can only be present in right subarray
        else:
            return binary_search(arr, mid + 1, high, x)
    else:
        # Element is not present in the array
        return -1

# def invertedIndex(line):
#     from nltk.tokenize import word_tokenize 
#     import nltk 
#     from nltk.corpus import stopwords 
#     nltk.download('stopwords') 
#     nltk.download('punkt')

#     array = []
#     pdb.set_trace()
#     punc = '''!()-[]{};:'"\, <>./?@#$%^&*_~'''
#     for read in line:
#         for ele in read:   
#             if ele in punc:   
#                 read = read.replace(ele, " ")

#     for i in range(1): 
#         # this will convert 
#         # the word into tokens 
#         text_tokens = word_tokenize(read) 
    
#     tokens_without_sw = [ 
#         word for word in text_tokens if not word in stopwords.words()] 
#     inverte_index_dict = {} 

#     for i in range(line): 
#         check = array[i].lower() 
#         for item in tokens_without_sw: 

#             if item in check: 
#                 if item not in dict: 
#                     inverte_index_dict[item] = [] 

#                 if item in dict: 
#                     inverte_index_dict[item].append(i+1)
    
#     return dict
# _test = []
# for i in all_courses:
#     _test.append(i['title'].split())

# inverted_index = invertedIndex(line=_test)