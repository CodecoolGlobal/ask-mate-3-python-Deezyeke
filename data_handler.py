import os
from collections import OrderedDict
import psycopg2
import psycopg2.extras
from data_connection import connection_handler


QUESTION_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


@connection_handler
def get_all_questions(cursor):
    query = """
        SELECT *
        FROM question"""
    cursor.execute(query)
    return cursor.fetchall()

# Visszaadja az id alapján a megfelelő question-t, közvetlenül a dictonary-t, nem a listába ágyazott dictonary-t, amit a fetchall adna.
@connection_handler
def get_question(cursor, id):
    query ='''SELECT * 
    FROM  question
    WHERE id=%(id)s'''
    cursor.execute(query, {'id': id})
    return cursor.fetchall()[0]


@connection_handler
def save_new_question(cursor, question):
    query = """
    INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
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


def delete_image_file(filename):
    os.remove(os.path.join('static', filename))


@connection_handler
def replace_question(cursor, q_id, question):
    query ='''UPDATE question 
    SET  submission_time=%(sub)s, view_number=%(vie)s, vote_number=%(vot)s, title=%(ttl)s, message=%(msg)s, image=%(img)s
    WHERE id=%(qid)s'''
    cursor.execute(query, {'qid':q_id, 'sub':question['submission_time'], 'vie':question['view_number'], 'vot':question['vote_number'], 'ttl':question['title'], 'msg':question['message'], 'img':question['image']})
