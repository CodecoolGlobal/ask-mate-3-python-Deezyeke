import csv
import os
from collections import OrderedDict

import connection
from connection import read_question

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
    if filename not in os.path.join('static'):
        pass
    else:
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


def delete_id_question(id, dict):
    dict.pop(id)
    return dict


def delete_answer_with_question(id, answers):
    newanswer = OrderedDict()
    for answers_id, answer in answers.items():
        if answer['question_id'] != id:
            newanswer[answers_id] = answer
    return newanswer


def load_answers():
    pass
