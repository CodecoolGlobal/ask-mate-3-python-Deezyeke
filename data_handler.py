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


@connection_handler
def delete_question(cursor, id):
    cursor.execute("""
    DELETE FROM question
    WHERE id = %(id)s""",
                   {'id': id})


@connection_handler
def delete_answer(cursor, id):
    cursor.execute("""
    DELETE FROM answer
    WHERE id = %(id)s""",
                   {'id': id})