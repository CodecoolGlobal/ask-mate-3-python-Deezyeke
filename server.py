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

@app.route('/question/<id>/delete')
def delete_question(id):



if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
    )
