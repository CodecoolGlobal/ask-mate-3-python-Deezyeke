import csv
import server
import data_operations
import os
from datetime import datetime
from collections import OrderedDict


def read_question(csv_file):
    questions = OrderedDict()
    with open(csv_file, 'r') as f:
        f_csv = csv.DictReader(f, delimiter=',')
        for row in f_csv:
            question = {}
            for key in row.keys():
                if key != 'id':
                    question[key] = row[key]
            questions[row['id']] = question
    return questions


def write_questions(csv_file, dict, headers):
    temp_dict = {}
    with open(csv_file, 'w') as f:
        f_csv = csv.DictWriter(f, fieldnames=headers)
        f_csv.writeheader()
        for id in dict.keys():
            temp_dict['id'] = id
            for item in range(1, len(headers)):
                temp_dict[headers[item]] = dict[id][headers[item]]
            f_csv.writerow(temp_dict)


def init_answer(header):
    answer = {}
    for field in header:
        answer[field] = ' '
    answer['id'] = data_operations.create_id()
    answer['vote_number'] = 0
    return answer


def add_data_for_csv(q_id):
    answer = init_answer(data_operations.ANSWER_HEADER)
    now = datetime.now()
    answer['submission_time'] = now.strftime("%Y/%m/%d %H:%M:%S")
    answer['question_id'] = q_id
    answer['message'] = server.request.form.get('message')
    uploaded_file = server.request.files['image_file']
    if uploaded_file.filename != '':
        uploaded_file.save('./static/' + uploaded_file.filename)
    answer['image'] = uploaded_file.filename
    data_operations.save_data(answer, data_operations.FILENAME_ANSWERS, data_operations.ANSWER_HEADER)


def create_empty_question():
    question = {}
    for field in data_operations.QUESTION_HEADER:
        question[field] = ' '
    question['id'] = data_operations.create_id()
    question['view_number'] = 0
    question['vote_number'] = 0
    return question


def fill_empty_question():
    question = create_empty_question()
    now = datetime.now()
    question['submission_time'] = now.strftime("%Y/%m/%d %H:%M:%S")
    question['title'] = server.request.form.get('title')
    question['message'] = server.request.form.get('text')
    uploaded_file = server.request.files['image_file']
    if uploaded_file.filename != '':
        uploaded_file.save(os.path.join('static', uploaded_file.filename))
        question['image'] = uploaded_file.filename
    data_operations.save_data(question, data_operations.FILENAME_QUESTIONS, data_operations.QUESTION_HEADER)


def orderby(questions, orderby, order):
    question_list = []
    if orderby != 'id':
        for id in questions.keys():
            question_list.append([questions[id][orderby], id])
            id = 1
    else:
        for id in questions.keys():
            question_list.append([id])
            id = 0
    question_list.sort(reverse=True if order == 'asc' else False, key=lambda x: x[0].lower())
    questions_ordered = OrderedDict()
    for item in question_list:
        questions_ordered[item[id]] = questions[item[id]]
    return questions_ordered
