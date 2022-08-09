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


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
    )
