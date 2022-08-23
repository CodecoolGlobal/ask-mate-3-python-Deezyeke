import csv
import os
import bcrypt


QUESTION_FILE_PATH = os.getenv(
    'DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'question.csv'
ANSWER_FILE_PATH = os.getenv(
    'DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'answers.csv'
ANSWER_HEADER = ['id', 'submission_time',
                 'vote_number', 'question_id', 'message', 'image']
QUESTION_HEADER = ['id', 'submission_time', 'view_number',
                   'vote_number', 'title', 'message', 'image']

def generate_hash(password_text):
    salt_bytes = bcrypt.gensalt()
    password_bytes = password_text.encode()
    password_hashed_bytes = bcrypt.hashpw(password_bytes, salt_bytes)
    return password_hashed_bytes


def verify_password(password_to_verify_text, password_hashed_bytes):
    password_to_verify_bytes = password_to_verify_text.encode()
    return bcrypt.checkpw(password_to_verify_bytes, password_hashed_bytes)


def read_questions():
    questions = []
    with open(QUESTION_FILE_PATH, 'r') as file:
        reader = csv.DictReader(file, fieldnames=QUESTION_HEADER)
        for line in reader:
            questions.append(line)
    return questions  # out: list of dictionaries, one row = one dictionary


def choose_data(id):  # return 1 dict
    questions = read_questions()
    data = {}
    for x in questions:
        if x['id'] == str(id):
            data = x
    return data


# under process - information=answer/question dict
def change_votenum(information, up_or_downvote):
    current_vote = int(information["vote_number"])
    if up_or_downvote == "+":
        current_vote += 1
    else:
        current_vote -= 1
    return current_vote


def add_view(information):
    view_number = int(information["view_number"])
    return view_number + 1


def update_data(data: list, data_id, data_key, new_data, csv):
    """
    Takes List of dictionaries;
    Update the indexed dictionary's given key's value with data_set
    Then update the csv files based on the csv parameter
    """
    for idx, item in enumerate(data):
        if item.get('id') == data_id:
            if data_key == 'question':
                data[idx] = new_data
            else:
                for key in item:
                    if key == data_key:
                        data[idx][key] = new_data
    if csv == 'question':
        update_question_csv(data)
    elif csv == 'answer':
        update_answer_csv(data)


def update_question_csv(question_data):
    with open(QUESTION_FILE_PATH, 'w') as file:
        writer = csv.DictWriter(file, fieldnames=QUESTION_HEADER)
        for line in question_data:
            writer.writerow(line)


def update_answer_csv(question_data):
    with open(ANSWER_FILE_PATH, 'w') as file:
        writer = csv.DictWriter(file, fieldnames=ANSWER_HEADER)
        for line in question_data:
            writer.writerow(line)


"""Dont delete above anything!!"""


def create_empty_answer():
    answer = {'vote_number': 0, 'image': None}
    return answer


def select_needed_data(db_key, db_value, database):
    found_data = []
    for data in database:
        for key, value in data.items():
            if key == db_key and str(value) == db_value:
                found_data.append(data)
    return found_data
