import os
from collections import OrderedDict
import psycopg2
import psycopg2.extras
from psycopg2 import sql
from psycopg2._psycopg import cursor
from data_connection import connection_handler

QUESTION_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


@connection_handler
def get_user_password(cursor, email):
    # query = """
    #         SELECT email, "password"
    #         FROM question"""
    # cursor.execute(query)
    # return cursor.fetchall()  # listában adja vissza a dict-eket
    query = sql.SQL('''SELECT id, password
        FROM users
        WHERE email={} ''').format(sql.Literal(email))
    cursor.execute(query)
    return cursor.fetchone()


@connection_handler
def get_all_questions(cursor):
    query = """
        SELECT *
        FROM question"""
    cursor.execute(query)
    return cursor.fetchall()


@connection_handler
def get_last_five_questions(cursor, submission_time):
    query = """
            SELECT * FROM question
            ORDER BY submission_time DESC
            lIMIT 5;"""
    cursor.execute(query)
    return cursor.fetchall()


@connection_handler
def increase_view_number(cursor, id, table='question'):
    query = sql.SQL('''UPDATE {}
        SET view_number = view_number + 1
        WHERE id = {}''').format(sql.Identifier(table), sql.Literal(str(id)))
    cursor.execute(query)


@connection_handler
def filter_questions(cursor, table='question'):
    pass
    query = sql.SQL('''SELECT * {}
    ORDER BY {}''').format(sql.Identifier(table), sql.Literal(str(id)))
    cursor.execute(query)


# Visszaadja az id alapján a megfelelő question-t, közvetlenül a dictonary-t, nem a listába ágyazott dictonary-t, amit a fetchall adna.
@connection_handler
def get_question(cursor, id):
    query = '''SELECT * 
    FROM  question
    WHERE id=%(id)s'''
    cursor.execute(query, {'id': id})
    return cursor.fetchall()[0]


@connection_handler
def save_new_question(cursor, question):
    query = """
    INSERT INTO question (submission_time, view_number, vote_number, title, message, image, user_id)
    VALUES ( %(st)s, %(vi)s, %(vo)s, %(ti)s, %(me)s, %(im)s , %(uid)s)"""
    cursor.execute(query,
                   {'st': question['submission_time'], 'vi': question['view_number'], 'vo': question['view_number'],
                    'ti': question['title'],
                    'me': question['message'], 'im': question['image'], 'uid': question['user_id']})


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
    question['user_id'] = None
    return question


def delete_image_file(filename):
    os.remove(os.path.join('static', filename))


@connection_handler
def replace_question(cursor, q_id, question):
    query = '''UPDATE question 
    SET  submission_time=%(sub)s, view_number=%(vie)s, vote_number=%(vot)s, title=%(ttl)s, message=%(msg)s, image=%(img)s
    WHERE id=%(qid)s'''
    cursor.execute(query, {'qid': q_id, 'sub': question['submission_time'], 'vie': question['view_number'],
                           'vot': question['vote_number'], 'ttl': question['title'], 'msg': question['message'],
                           'img': question['image']})


def create_empty_answer():
    answer = {'vote_number': 0, 'image': None}
    return answer


@connection_handler
def change_vote_number(cursor, id, table, up_or_down):
    if up_or_down == "up":
        query = sql.SQL("""UPDATE {}
        SET vote_number = vote_number + 1
        WHERE id = {}""").format(sql.Identifier(table), sql.Literal(str(id)))
    else:
        query = sql.SQL("""UPDATE {}
        SET vote_number = vote_number - 1
        WHERE id = {}""").format(sql.Identifier(table), sql.Literal(str(id)))
    cursor.execute(query)


@connection_handler
def search_questions(cursor, search, table='question'):
    query = sql.SQL("""SELECT * FROM {}
    WHERE title LIKE {}
    OR message LIKE {} """).format(sql.Identifier(table), sql.Literal('%' + search + '%'),
                                   sql.Literal('%' + search + '%'))
    cursor.execute(query)
    return cursor.fetchall()


@connection_handler
def add_answer_to_question(cursor, answer):
    query = """
            INSERT INTO answer (submission_time, vote_number, question_id, message, image, user_id)
            VALUES ( %(st)s, %(vo)s, %(qi)s, %(me)s, %(im)s, %(uid)s )"""
    cursor.execute(query, {'st': answer['submission_time'], 'vo': answer['vote_number'],
                           'qi': answer['question_id'], 'me': answer['message'], 'im': answer['image'], 'uid': answer['user_id']})



@connection_handler
def delete_question(cursor, id):
    cursor.execute("""
    DELETE FROM question
    WHERE id = %(id)s""",
                   {'id': id})


@connection_handler
def delete_answer_with_question(cursor, id):
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
def get_image_name_form_question(cursor, id):
    cursor.execute("""
    SELECT image
    FROM question
    WHERE id = %(id)s""",
                   {'id': id})
    return cursor.fetchone()


@connection_handler
def get_image_name_from_answer(cursor, id):
    cursor.execute("""
    SELECT image
    FROM answer
    WHERE id = %(id)s""",
                   {'id': id})
    return cursor.fetchone()


@connection_handler
def get_images_names(cursor, q_id):
    cursor.execute("""
    SELECT image
    FROM answer
    WHERE question_id = %(q_i)s""",
                   {'q_i': q_id})
    return cursor.fetchall()


@connection_handler
def add_comment_to_question(cursor, comment):
    query = """
            INSERT INTO comment (submission_time, question_id, message, user_id)
            VALUES ( %(st)s, %(qi)s, %(me)s, %(uid)s)"""
    cursor.execute(query, {'st': comment['submission_time'], 'qi': comment['question_id'], 'me': comment['message'], 'uid': comment['user_id']})



@connection_handler
def add_comment_to_answer(cursor, comment):
    query = """
            INSERT INTO comment (submission_time, answer_id, message, user_id)
            VALUES ( %(st)s, %(ai)s, %(me)s, %(uid)s)"""
    cursor.execute(query, {'st': comment['submission_time'],
                           'ai': comment['answer_id'], 'me': comment['message'], 'uid': comment['user_id']})


@connection_handler
def read_q_comments_by_id(cursor, q_id):
    query = """
        SELECT *
        FROM comment
        WHERE question_id = %(q_id)s"""
    cursor.execute(query, {'q_id': q_id})
    return cursor.fetchall()


@connection_handler
def search_q_id_by_a_id(cursor, a_id):
    query = """
        SELECT question_id
        FROM answer
        WHERE answer.id = %(a_id)s"""
    cursor.execute(query, {'a_id': a_id})
    return cursor.fetchall()


@connection_handler
def read_a_comments(cursor):
    query = """
            SELECT *
            FROM comment
            WHERE question_id is null"""
    cursor.execute(query)
    return cursor.fetchall()


@connection_handler
def get_question_tags(cursor, question_id):
    query = '''SELECT tag_id, name
            FROM question_tag
            JOIN tag ON question_tag.tag_id = tag.id
            WHERE question_id = %(q_id)s'''
    cursor.execute(query, {'q_id': question_id})
    return cursor.fetchall()


@connection_handler
def get_tags(cursor):
    query = """SELECT *
            FROM tag"""
    cursor.execute(query)
    return cursor.fetchall()


@connection_handler
def add_new_tag(cursor, tag):
    query = '''INSERT INTO tag (name)
    VALUES (%(nme)s)
    '''
    cursor.execute(query, {'nme': tag})


@connection_handler
def add_new_tag_to_question(cursor, question_id, tag_id):
    query = '''INSERT INTO question_tag (question_id, tag_id)
                VALUES (%(qid)s, %(tid)s)'''
    try:
        cursor.execute(query, {'qid': question_id, 'tid': tag_id})
    except psycopg2.errors.UniqueViolation:
        pass


@connection_handler
def delete_question_tag(cursor, question_id, tag_id):
    query = '''DELETE FROM question_tag
            WHERE question_id=%(qid)s and tag_id=%(tid)s'''
    cursor.execute(query, {'qid': question_id, 'tid': tag_id})


@connection_handler
def read_all_comments(cursor):
    query = """
            SELECT *
            FROM comment"""
    cursor.execute(query)
    return cursor.fetchall()


@connection_handler
def update_commit(cursor, c_id, new_message, current_time):
    query = '''UPDATE comment
            SET message = %(cmess)s, submission_time = %(c_time)s
            WHERE id = %(cid)s'''
    cursor.execute(query, {'cmess': new_message, 'cid': c_id, 'c_time': current_time})


@connection_handler
def get_qid_by_aid(cursor, a_id):
    query = """
            SELECT question_id
            FROM answer
            WHERE id = %(aid)s"""
    cursor.execute(query, {'aid': a_id})
    return cursor.fetchall()


@connection_handler
def update_answer(cursor, a_id, new_message):
    query = '''UPDATE answer
            SET message = %(cmess)s
            WHERE id = %(aid)s'''
    cursor.execute(query, {'cmess': new_message, 'aid': a_id})


@connection_handler
def delete_comment_from_question(cursor, question_id, comment_id):
    cursor.execute("""
    DELETE FROM comment
    WHERE question_id = %(q_i)s and id = %(c_i)s""",
                   {'q_i': question_id, 'c_i': comment_id})


@connection_handler
def delete_comment_from_answer(cursor, answer_id, comment_id):
    cursor.execute("""
    DELETE FROM comment
    WHERE answer_id = %(a_i)s and id = %(c_i)s""",
                   {'a_i': answer_id, 'c_i': comment_id})


@connection_handler
def delete_comment_with_question(cursor, question_id):
    cursor.execute("""
    DELETE FROM comment
    WHERE question_id = %(q_id)s""",
                   {'q_id': question_id})


@connection_handler
def delete_answer_comment_with_question_deleted(cursor, answer_id):
    cursor.execute("""
    DELETE FROM comment
    WHERE answer_id = %(a_i)s""",
                   {'a_i': answer_id})


@connection_handler
def get_answers_with_question_id(cursor, question_id):
    cursor.execute("""
    SELECT *
    FROM answer
    WHERE question_id = %(q_i)s""",
                   {'q_i': question_id})
    return cursor.fetchall()


@connection_handler
def delete_tag_with_question(cursor, q_id):
    cursor.execute("""
    DELETE FROM question_tag
    WHERE question_id = %(q_i)s""",
                   {'q_i': q_id})


@connection_handler
def sort_questions(cursor, order_by):
    query = sql.SQL('SELECT * FROM question ORDER_BY {col}').format(col=sql.Identifier(order_by))
    cursor.execute(query)
    return cursor.fetchall()


@connection_handler
def add_new_user(cursor, email, password_hashed_text, reg_date):
    query = sql.SQL('INSERT INTO users (email, password, reg_date, reputation) VALUES ({}, {}, {}, {})').format(sql.Literal(email),
                                                                                                sql.Literal(
                                                                                                    password_hashed_text),
                                                                                                sql.Literal(reg_date),
                                                                                                                sql.Literal(0))
    cursor.execute(query)


@connection_handler
def get_all_username(cursor):
    cursor.execute("""
    SELECT email FROM users	
    """)
    return cursor.fetchall()


@connection_handler
def get_user_question_count(cursor, user):
    cursor.execute('''
    SELECT COUNT(user_id) AS question FROM users
    INNER JOIN question ON users.id = question.user_id
    WHERE users.email = %(us)s''',
                   {'us': user})
    return cursor.fetchall()


@connection_handler
def get_user_answer_count(cursor, user):
    cursor.execute("""
    SELECT COUNT(answer.question_id) AS answer FROM users
    INNER JOIN answer ON users.id = answer.user_id
    WHERE users.email = %(us)s""",
                   {'us':user})
    return cursor.fetchall()


@connection_handler
def get_user_comment_count(cursor, user):
    cursor.execute("""
    SELECT COUNT(comment.question_id) AS comment FROM users
    INNER JOIN comment ON users.id = comment.user_id
    WHERE users.email = %(us)s""",
                   {'us': user})
    return cursor.fetchall()


@connection_handler
def get_user_registration_date(cursor, user):
    cursor.execute("""
    SELECT reg_date FROM users
    WHERE email = %(usr)s
    """, {'usr': user})
    return cursor.fetchall()


@connection_handler
def get_user_reputation(cursor, user):
    cursor.execute("""
    SELECT reputation
    FROM users
    WHERE email = %(usr)s""",
                   {'usr': user})
    return cursor.fetchall()


# query = sql.SQL("select {field} from {table} where {pkey} = %s").format(
#     field=sql.Identifier('my_name'),
#     table=sql.Identifier('some_table'),
#     pkey=sql.Identifier('id'))


@connection_handler
def get_user_info(cursor, user_id):
    cursor.execute("""
    SELECT id, email, reg_date, reputation FROM users WHERE %(u_id)s = id""",
    {'u_id': user_id})
    return cursor.fetchall()


@connection_handler
def get_user_id_by_email(cursor, user_email):
    cursor.execute("""
    SELECT id FROM users WHERE email = %(u_i)s""",
                   {'u_i': user_email})
    return cursor.fetchone()


@connection_handler
def get_questions_by_user_id(cursor, user_id):
    cursor.execute("""
    SELECT id, submission_time, view_number, vote_number, title, message FROM question WHERE user_id = %(u_i)s""",
                   {'u_i': user_id})
    return cursor.fetchall()


@connection_handler
def get_answers_by_user_id(cursor, user_id):
    cursor.execute("""
    SELECT id, submission_time, vote_number, question_id message FROM answer WHERE user_id = %(u_i)s""",
                   {'u_i': user_id})
    return cursor.fetchall()


@connection_handler
def get_comments_by_user_id(cursor, user_id):
    cursor.execute("""
    SELECT id, message, submission_time, question_id FROM comment WHERE user_id = %(u_i)s""",
                   {'u_i': user_id})
    return cursor.fetchall()


@connection_handler
def get_user_id_by_s_id(cursor, table, col, s_id):
    query = sql.SQL("""
    SELECT user_id FROM {} WHERE {} = {}""").format(sql.Identifier(table), sql.Identifier(col), sql.Literal(str(s_id)))
    cursor.execute(query)
    return cursor.fetchone()


@connection_handler
def change_reputation_number(cursor, u_id, table, up_or_down, numb):
    if up_or_down == 'up':
        query = sql.SQL("""
        UPDATE {} 
        SET reputation = reputation + {}
        WHERE id = {}""").format(sql.Identifier(table), sql.Literal(str(numb)), sql.Literal(str(u_id)))
    else:
        query = sql.SQL("""
        UPDATE {} 
        SET reputation = reputation - 2
        WHERE id = {}""").format(sql.Identifier(table), sql.Literal(str(u_id)))
    cursor.execute(query)
