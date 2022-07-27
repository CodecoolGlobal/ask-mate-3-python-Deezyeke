import csv
import os
from collections import OrderedDict

import data_operations


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

def write_questions(csv_file, dict):
    temp_dict = {}
    with open(csv_file, 'w') as f:
        f_csv = csv.DictWriter(f, fieldnames=data_operations.QUESTION_HEADER)
        f_csv.writeheader()
        for id in dict.keys():
            temp_dict['id'] = id
            for item in range(1, len(data_operations.QUESTION_HEADER)):
                temp_dict[data_operations.QUESTION_HEADER[item]] = dict[id][data_operations.QUESTION_HEADER[item]]
            f_csv.writerow(temp_dict)

