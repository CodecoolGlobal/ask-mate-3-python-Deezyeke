import data_operations
import server
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

def write_questions(csv_file, dict, headers):
    temp_dict = {}
    with open(csv_file, 'w') as f:
        f_csv = csv.DictWriter(f, fieldnames=headers)
        f_csv.writeheader()
        for id in dict.keys():
            temp_dict['id'] = id
            for item in range(1, len(data_operations.QUESTION_HEADER)):
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
    now = server.datetime.now()
    answer['submission_time'] = now.strftime("%Y/%m/%d %H:%M:%S")
    answer['question_id'] = q_id
    answer['message'] = server.request.form.get('message')
    uploaded_file = server.request.files['image_file']
    if uploaded_file.filename != '':
        uploaded_file.save('./static/' + uploaded_file.filename)
    answer['image'] = uploaded_file.filename
    data_operations.save_data(answer, data_operations.FILENAME_ANSWERS, data_operations.ANSWER_HEADER)
