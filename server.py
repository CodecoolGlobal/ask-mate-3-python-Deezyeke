from flask import Flask, render_template, request, redirect, url_for
import util
import data_handler
import os
from datetime import datetime


app = Flask(__name__)


@app.route('/')
def index():
    questions = data_handler.get_all_questions()

    return render_template('questions_list.html', orderby='id', questions=questions, question_header=data_handler.QUESTION_HEADER)


@app.route('/add_question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'GET':
        return render_template('add_question.html')
    elif request.method == 'POST':
        question = data_handler.create_empty_question()
        now = datetime.now()
        question['submission_time'] = now.strftime("%Y/%m/%d %H:%M:%S")
        question['title'] = request.form.get('title')
        question['message'] = request.form.get('text')
        uploaded_file = request.files['image_file']
        if uploaded_file.filename != '':
            uploaded_file.save(os.path.join('static', uploaded_file.filename))
            question['image'] = uploaded_file.filename

        data_handler.save_new_question(question)

        return redirect(url_for('index'))


@app.route('/question/<id>/edit', methods=['GET', 'POST'])
def edit_question(id):
    if request.method == 'GET':
        question = data_handler.get_question(id)
        return render_template ('edit_question.html', id=id, title=question['title'], message=question['message'], image=question['image'])
    elif request.method == 'POST':
        orig_question = data_handler.get_question(id)
        question = {}
        question['id'] = id
        now = datetime.now()
        question['submission_time'] = now.strftime("%Y/%m/%d %H:%M:%S")
        question['view_number'] = orig_question['view_number']
        question['vote_number'] = orig_question['vote_number']
        question['title'] = request.form.get('title')
        question['message'] = request.form.get('text')
        uploaded_file = request.files['image_file']

        if uploaded_file.filename != '':
            uploaded_file.save(os.path.join('static', uploaded_file.filename))
            question['image'] = uploaded_file.filename
            if orig_question['image'] is not None:
                data_handler.delete_image_file(orig_question['image'])
        else:
            question['image'] = orig_question['image']

        data_handler.replace_question(id, question)

        return redirect (url_for('display_question', q_id=id))


@app.route('/display-question/<q_id>')
def display_question(q_id):
    questions = []
    answers = []
    for question in data_handler.get_all_questions():
        for key, value in question.items():
            if key == 'id' and str(value) == q_id:
                questions.append(question)
    for answer in data_handler.get_all_answers():
        for key, value in answer.items():
            if key == 'question_id' and str(value) == q_id:
                answers.append(answer)
    return render_template('display_question.html', question=questions, answer=answers, q_id=q_id)


@app.route('/display-question/<q_id>/delete', methods=['GET', 'POST'])
def delete_question(q_id):
    if request.method == 'GET':
        return render_template('delete.html', q_id=q_id)
    else:
        data_handler.delete_answer_when_question(q_id)
        data_handler.delete_question(q_id)
        return redirect(url_for('index'))


@app.route('/question/<q_id>/add-new-answer', methods=['GET', 'POST'])
def add_new_answer(q_id):
    if request.method == 'GET':
        return render_template('new_answer.html', q_id=q_id)
    elif request.method == 'POST':
        answer = data_handler.create_empty_answer()
        now = datetime.now()
        answer['submission_time'] = now.strftime("%Y/%m/%d %H:%M:%S")
        answer['message'] = request.form.get('message')
        answer['question_id'] = q_id
        uploaded_file = request.files['image_file']
        if uploaded_file.filename != '':
            uploaded_file.save(os.path.join('static', uploaded_file.filename))
            answer['image'] = uploaded_file.filename
        data_handler.add_answer_to_question(answer)
        return redirect(url_for('display_question', q_id=q_id))


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
    )
