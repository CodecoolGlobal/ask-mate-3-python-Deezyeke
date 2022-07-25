from flask import Flask,render_template, request, redirect
import data_operations
from datetime import datetime
from collections import OrderedDict

app = Flask(__name__)


@app.route('/add_question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'GET':
        return render_template('add_question.html')
    elif request.method == 'POST':
        question ={}
        now = datetime.now()
        question['id'] = data_operations.create_id()
        question['timestamp'] = now.strftime("%Y/%m/%d %H:%M:%S")
        question['text'] = request.form.get('text')
        data_operations.save_question(question)

## !!!  Ezt át kell majd írni   !!!
        return redirect('/list')


@app.route('/')
@app.route('/list')
def list():
    questions = data_operations.load_questions()
    questions_ordered = orderby(questions)
    return render_template('list.html', questions = questions_ordered)


def orderby(questions):
    question_list = []
    for id in questions.keys():
        question_list.append([ id, questions[id]['timestamp'] ])
    question_list.sort(reverse=True, key=lambda x : x[1])
    questions_ordered = OrderedDict()
    for item in question_list:
        questions_ordered[item[0]]=questions[item[0]]
    return questions_ordered


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
    )

