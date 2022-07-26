from flask import Flask,render_template, request, redirect
import data_operations
from datetime import datetime
from collections import OrderedDict

app = Flask(__name__)


def init_questions():
    questions = OrderedDict()
    question = OrderedDict()
    for field in data_operations.QUESTION_HEADER():
        question[field] = ' '
    questions[data_operations.create_id()] = question


def init_question():
    question = {}
    for field in data_operations.QUESTION_HEADER:
        if field == 'id':
            question[field] = data_operations.create_id()
        else:
            question[field] = ' '
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
        data_operations.save_question(question)

## !!!  Ezt át kell majd írni   !!!
        return redirect('/list')


@app.route('/')
@app.route('/list')
def list():
    questions = data_operations.load_questions()
    questions_ordered = orderby(questions)
    return render_template('list.html', questions = questions_ordered, question_header = data_operations.QUESTION_HEADER)


def orderby(questions):
    question_list = []
    for id in questions.keys():
        question_list.append([ id, questions[id]['submission_time'] ])
    question_list.sort(reverse=True, key=lambda x : x[1])
    questions_ordered = OrderedDict()
    for item in question_list:
        questions_ordered[item[0]]=questions[item[0]]
    return questions_ordered


@app.route('/delete')
def delete_question():
    questions = data_operations.load_questions()
    questions_ordered = orderby(questions)
    return render_template('delete.html', questions=questions_ordered, questioins_header=data_operations.QUESTION_HEADER)


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
    )

