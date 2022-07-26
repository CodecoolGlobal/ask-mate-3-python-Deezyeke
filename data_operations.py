import csv
import os
from collections import OrderedDict

FILENAME_QUESTIONS = 'question.csv'
QUESTION_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']


def create_id():
    return os.urandom(4).hex()

def load_questions():
    questions = OrderedDict()
    try:
        with open(FILENAME_QUESTIONS, 'r') as f:
            f_csv = csv.DictReader(f, delimiter = ',')
            for row in f_csv:
                question ={}
                for key in row.keys():
                    if key != 'id':
                        question[key] = row[key]
                questions[row['id']] = question
            return questions
    except FileNotFoundError:
        with open(FILENAME_QUESTIONS, 'w') as f:
            f_csv = csv.DictWriter(f, fieldnames = QUESTION_HEADER)
            f_csv.writeheader()
            return questions


def save_question(question):
    with open(FILENAME_QUESTIONS, 'a') as f:
        f_csv = csv.DictWriter(f, fieldnames = QUESTION_HEADER)
        f_csv.writerow(question)
