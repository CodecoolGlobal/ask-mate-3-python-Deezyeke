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


def create_empty_question():
    question = {}
    question['view_number'] = 0
    question['vote_number'] = 0
    return question


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

        data_handler.save_new_question()

        return redirect('/list')


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
    if request.method == 'POST':
        data_handler.delete_question(q_id)
        return redirect(url_for('index'))
    else:
        return redirect(url_for('display_question'))


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
    )
