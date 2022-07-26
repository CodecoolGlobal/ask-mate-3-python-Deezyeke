from flask import Flask, render_template, request, redirect
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
    if request.args.get('action') == None:
        return render_template('list.html', questions = questions, question_header = data_operations.QUESTION_HEADER)
    else:
        questions_ordered = orderby(questions, request.args.get('action'))
        return render_template('list.html', questions=questions_ordered, question_header=data_operations.QUESTION_HEADER)


def orderby(questions, orderby):
    question_list = []

    if orderby != 'id':
        for id in questions.keys():
            question_list.append([ questions[id][orderby], id ])
            id = 1
    else:
        for id in questions.keys():
            question_list.append([id])
            id = 0

    question_list.sort(reverse=True, key=lambda x : x[0])
    questions_ordered = OrderedDict()
    for item in question_list:
        questions_ordered[item[id]]=questions[item[id]]

    return questions_ordered



@app.route('/questions/<id>/delete')
def delete_question(id):
    return render_template('delete.html')


@app.route('/questions/<id>')
def questions_and_answers(id):
    questions = data_operations.load_questions()
    return render_template('display_question.html', question=questions, id=id)



if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
    )

