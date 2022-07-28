import csv
import os
from collections import OrderedDict

import connection
from connection import read_questions

FILENAME_QUESTIONS = 'question.csv'
FILENAME_ANSWERS = 'answers.csv'
QUESTION_HEADER = ['id', 'submission_time', 'view_number',
                   'vote_number', 'title', 'message', 'image']
ANSWER_HEADER = ['id', 'submission_time',
                 'vote_number', 'question_id', 'message', 'image']


'''if Linux + Win:
QUESTION_FILE_PATH = os.getenv(
    'DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'question.csv'
ANSWER_FILE_PATH = os.getenv(
    'DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'answers.csv'''


def create_id():
    return os.urandom(4).hex()


def delete_image_file(filename):
    os.remove(os.path.join('static', filename))


def load_csv(csv_file):
    questions = OrderedDict()
    try:
        with open(csv_file, 'r') as f:
            f_csv = csv.DictReader(f, delimiter=',')
            for row in f_csv:
                question = {}
                for key in row.keys():
                    if key != 'id':
                        if (key == 'vote_number') or (key == 'view_number'):
                            question[key] = int(row[key])
                        else:
                            question[key] = row[key]
                questions[row['id']] = question
            return questions
    except FileNotFoundError:
        with open(csv_file, 'w') as f:
            f_csv = csv.DictWriter(f, fieldnames=QUESTION_HEADER)
            f_csv.writeheader()
            return questions


def save_data(datas, csv_file, header):
    with open(csv_file, 'a') as f:
        f_csv = csv.DictWriter(f, fieldnames=header)
        f_csv.writerow(datas)


def delete_id_question(id, questions):
    questions.pop(id)
    return dict


def delete_answer_with_question(id, dict):
    new_dict = {}
    for key, value in dict.items():
        if value['question_id'] != id:
            new_dict[key] = value
    return new_dict


def create_empty_question():
    question = {}
    for field in QUESTION_HEADER:
        question[field] = ' '
    question['id'] = create_id()
    question['view_number'] = 0
    question['vote_number'] = 0
    return question


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


def replace_question(questions, question):
    questions.pop(question['id'])
    to_insert_question = {}
    temp_question = {}
    for field in range(1, len(QUESTION_HEADER)):
        temp_question[QUESTION_HEADER[field]] = question[QUESTION_HEADER[field]]
    questions[ question['id'] ] = temp_question
    connection.write_questions(FILENAME_QUESTIONS, questions, QUESTION_HEADER)
