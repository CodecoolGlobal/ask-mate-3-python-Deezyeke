import csv
import os
from collections import OrderedDict

import connection
from connection import read_question

FILENAME_QUESTIONS = 'question.csv'
FILENAME_ANSWERS = 'answers.csv'
QUESTION_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']


def create_id():
    return os.urandom(4).hex()


def load_csv(csv_file):
    questions = OrderedDict()
    try:
        with open(csv_file, 'r') as f:
            f_csv = csv.DictReader(f, delimiter = ',')
            for row in f_csv:
                question ={}
                for key in row.keys():
                    if key != 'id':
                        question[key] = row[key]
                questions[row['id']] = question
            return questions
    except FileNotFoundError:
        with open(csv_file, 'w') as f:
            f_csv = csv.DictWriter(f, fieldnames = QUESTION_HEADER)
            f_csv.writeheader()
            return questions


def save_question(question):
    with open(FILENAME_QUESTIONS, 'a') as f:
        f_csv = csv.DictWriter(f, fieldnames = QUESTION_HEADER)
        f_csv.writerow(question)


def delete_id_question(id, dict):
    dict.pop(id)
    return dict



def load_answers():
    pass

