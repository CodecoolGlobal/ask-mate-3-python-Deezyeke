from flask import Flask, render_template, request, redirect, url_for
import util
import data_operations
import connection
import os
from datetime import datetime
from collections import OrderedDict

app = Flask(__name__)


def init_questions():
    questions = OrderedDict()
    question = OrderedDict()
    for field in data_operations.QUESTION_HEADER():
        question[field] = ' '
    question['view_number'] = '0'
    question['vote_number'] = '0'
    questions[data_operations.create_id()] = question


def init_question():
    question = {}

    for field in data_operations.QUESTION_HEADER:
        question[field] = ' '

    question['id'] = data_operations.create_id()
    question['view_number'] = 0
    question['vote_number'] = 0

    return question


@app.route('/add_question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'GET':
        return render_template('add_question.html')
    elif request.method == 'POST':

        question = init_question()
        now = datetime.now()
        question['submission_time'] = now.strftime("%Y/%m/%d %H:%M:%S")
        question['title'] = request.form.get('title')
        question['message'] = request.form.get('text')

        uploaded_file = request.files['image_file']
        if uploaded_file.filename != '':
            uploaded_file.save(os.path.join('static', uploaded_file.filename))
            question['image'] = uploaded_file.filename
        data_operations.save_data(question, data_operations.FILENAME_QUESTIONS, data_operations.QUESTION_HEADER)

## !!!  Ezt át kell majd írni   !!!
        return redirect('/list')


@app.route('/')
@app.route('/list')
def list():
    questions = data_operations.load_csv(data_operations.FILENAME_QUESTIONS)
    if request.args.get('orderby') == None:
        return render_template('questions_list.html', orderby='id', questions = questions, question_header = data_operations.QUESTION_HEADER)
    else:
        questions_ordered = orderby( questions, request.args.get('orderby'), request.args.get('order') )
        if request.args.get('order') == 'desc':
            return render_template('questions_list.html', orderby=request.args.get('orderby'), questions=questions_ordered, question_header=data_operations.QUESTION_HEADER)
        elif request.args.get('order') == 'asc':
            return render_template('questions_list_desc.html', orderby=request.args.get('orderby'), questions=questions_ordered, question_header=data_operations.QUESTION_HEADER)


def orderby(questions, orderby, order):
    question_list = []

    if orderby != 'id':
        for id in questions.keys():
            question_list.append([ questions[id][orderby], id ])
            id = 1
    else:
        for id in questions.keys():
            question_list.append([id])
            id = 0

    question_list.sort(reverse=True if order=='asc' else False, key=lambda x : x[0].lower() )
    questions_ordered = OrderedDict()

    for item in question_list:
        questions_ordered[item[id]]=questions[item[id]]

    return questions_ordered


@app.route('/questions/<id>', methods=['GET', 'POST'])
def questions_and_answers(id):
    questions = data_operations.load_csv(data_operations.FILENAME_QUESTIONS)
    answers = data_operations.load_csv(data_operations.FILENAME_ANSWERS)
    if request.method == 'GET':
        return render_template('display_question.html', question=questions, answer=answers, id=id)
    return redirect('display_question.html')


@app.route('/question/<question_id>/vote-up')
def question_vote_up(question_id):
    questions = util.read_questions()
    data = util.choose_data(question_id)
    current_vote_number = util.change_votenum(data, "+")
    util.update_data(questions, question_id, "vote_number", current_vote_number, "question")
    return redirect('/')


@app.route('/questions/<id>/delete')
def delete_question(id):
    return render_template('delete.html', id=id)


@app.route('/questions/<id>/delete/deleted')
def deleted_question(id):
    answers = connection.read_question(data_operations.FILENAME_ANSWERS)
    deleted_answers = data_operations.delete_answer_with_question(id, answers)
    connection.write_questions(data_operations.FILENAME_QUESTIONS, deleted_answers, data_operations.ANSWER_HEADER)
    questions = connection.read_question(data_operations.FILENAME_QUESTIONS)
    if questions[id]['image'] != ' ':
        data_operations.delete_image_file(questions[id]['image'])
    deleted_file = data_operations.delete_id_question(id, questions)
    connection.write_questions(data_operations.FILENAME_QUESTIONS, deleted_file, data_operations.QUESTION_HEADER)
    return render_template('deleted.html', id=id)


@app.route('/questions/<id>/new-answer', methods=['GET', 'POST'])
def add_new_answer(id):
    if request.method == 'GET':
        return render_template('new_answer.html', id=id)
    elif request.method == 'POST':
        connection.add_data_for_csv(id)
        return redirect(url_for('questions_and_answers', id=id))


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
    )
