import csv
import os

QUESTION_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'questions.csv'
ANSWER_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'answers.csv'
DATA_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title,message', 'image']


def count_votes(): # under process
    with open("questions.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            return dict(row)