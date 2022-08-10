import os
from collections import OrderedDict
import psycopg2
import psycopg2.extras
from data_connection import connection_handler


QUESTION_HEADER = ['id', 'submission_time', 'view_number',
                   'vote_number', 'title', 'message', 'image']
ANSWER_HEADER = ['id', 'submission_time',
                 'vote_number', 'question_id', 'message', 'image']


@connection_handler
def get_all_questions(cursor):
    query = """
        SELECT *
        FROM question"""
    cursor.execute(query)
    return cursor.fetchall()

@connection_handler
def save_new_question(cursor, question):
    query = """
    INSERT INTO QUESTION ('submission_time', 'view_number', 'vote_number', 'title', 'message', 'image')
    VALUES ( %(st)s, %(vi)s, %(vo)s, %(ti)s, %(me)s, %(im)s )"""
    cursor.execute(query, {'st': question['submission_time'], 'vi': question['view_number'], 'vo': question['view_number'], 'ti': question['title'],
                           'me': question['message'], 'im': question['image']})


@connection_handler
def get_all_answers(cursor):
    query = """
        SELECT *
        FROM answer"""
    cursor.execute(query)
    return cursor.fetchall()


def create_empty_question():
    question = {}
    question['view_number'] = 0
    question['vote_number'] = 0
    question['image'] = None
    return question


@connection_handler
def add_answer_to_question(cursor, answer):
    query = """
            INSERT INTO answer (submission_time, vote_number, question_id, message, image)
            VALUES ( %(st)s, %(vo)s, %(qi)s, %(me)s, %(im)s )"""
    cursor.execute(query, {'st': answer['submission_time'], 'vo': answer['vote_number'],
                    'qi': answer['question_id'], 'me': answer['message'], 'im': answer['image']})


@connection_handler
def add_comment(cursor, comment):
    query = """
            INSERT INTO comment (submission_time, question_id, message)
            VALUES ( %(st)s, %(qi)s, %(me)s)"""
    cursor.execute(query, {'st': comment['submission_time'],
                        'qi': comment['question_id'], 'me': comment['message']})


@connection_handler
def read_q_comments(cursor):
    query = """
        SELECT *
        FROM comment
        WHERE answer_id is null"""
    cursor.execute(query)
    return cursor.fetchall()
