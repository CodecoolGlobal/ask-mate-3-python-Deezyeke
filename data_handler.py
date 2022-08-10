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


def create_empty_answer():
    answer = {'vote_number': 0, 'image': None}
    return answer


@connection_handler
def add_answer_to_question(cursor, answer):
    query = """
            INSERT INTO answer (submission_time, vote_number, question_id, message, image)
            VALUES ( %(st)s, %(vo)s, %(qi)s, %(me)s, %(im)s )"""
    cursor.execute(query, {'st': answer['submission_time'], 'vo': answer['vote_number'],
                    'qi': answer['question_id'], 'me': answer['message'], 'im': answer['image']})


@connection_handler
def delete_question(cursor, id):
    cursor.execute("""
    DELETE FROM question
    WHERE id = %(id)s""",
                   {'id': id})


@connection_handler
def delete_answer_when_question(cursor, id):
    cursor.execute("""
    DELETE FROM answer
    WHERE question_id = %(id)s""",
                   {'id': id})


@connection_handler
def delete_answer(cursor, id):
    cursor.execute("""
    DELETE FROM answer
    WHERE id = %(id)s""",
                   {'id': id})


@connection_handler
def get_image_name_from_question(cursor, id):
    cursor.execute("""
    SELECT image
    FROM question
    WHERE id = %(id)s""",
                   {'id': id})
    return cursor.fetchone()


@connection_handler
def get_image_name_from_answer(cursor, q_id):
    cursor.execute("""
    SELECT image
    FROM answer
    WHERE question_id = %(q_i)s""",
                   {'q_i': q_id})
    return cursor.fetchall()


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


@connection_handler
def get_question_tags(cursor, question_id):
    query = '''SELECT name
            FROM question_tag
            JOIN tag ON question_tag.tag_id = tag.id
            WHERE question_id = %(q_id)s'''
    cursor.execute(query, {'q_id': question_id})
    return cursor.fetchall()


@connection_handler
def get_tags(cursor):
    query ="""SELECT *
            FROM tag"""
    cursor.execute(query)
    return cursor.fetchall()


@connection_handler
def add_new_tag(cursor, tag):
    query = '''INSERT INTO tag (name)
    VALUES (%(nme)s)
    '''
    cursor.execute(query, {'nme':tag})

@connection_handler
def add_new_tag_to_question(cursor, question_id, tag_id):
    query ='''INSERT INTO question_tag (question_id, tag_id)
                VALUES (%(qid)s, %(tid)s)'''
    try:
        cursor.execute(query, {'qid':question_id, 'tid':tag_id})
    except psycopg2.errors.UniqueViolation:
        pass
