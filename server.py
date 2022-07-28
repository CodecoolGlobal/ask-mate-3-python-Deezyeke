from flask import Flask, render_template, request, redirect, url_for
import util
import data_operations
import connection


app = Flask(__name__)


@app.route('/add_question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'GET':
        return render_template('add_question.html')
    elif request.method == 'POST':
        connection.fill_empty_question()
        return redirect('/list')


@app.route('/')
@app.route('/list')
def list():
    questions = data_operations.load_csv(data_operations.FILENAME_QUESTIONS)
    if request.args.get('orderby') is None:
        return render_template('questions_list.html', orderby='id', questions = questions, question_header = data_operations.QUESTION_HEADER)
    else:
        questions_ordered = connection.orderby(questions, request.args.get('orderby'), request.args.get('order'))
        if request.args.get('order') == 'desc':
            return render_template('questions_list.html', orderby=request.args.get('orderby'), questions=questions_ordered, question_header=data_operations.QUESTION_HEADER)
        elif request.args.get('order') == 'asc':
            return render_template('questions_list_desc.html', orderby=request.args.get('orderby'), questions=questions_ordered, question_header=data_operations.QUESTION_HEADER)


@app.route('/questions/<id>', methods=['GET', 'POST'])
def questions_and_answers(id):
    questions = data_operations.load_csv(data_operations.FILENAME_QUESTIONS)
    answers = data_operations.load_csv(data_operations.FILENAME_ANSWERS)
    if request.method == 'GET':
        # increase_view(id)
        return render_template('display_question.html', question=questions, answer=answers, id=id)
    return redirect('display_question.html')


@app.route('/questions/<question_id>/view')
def increase_view(question_id):
    questions = util.read_questions()
    data = util.choose_data(question_id)
    current_view_number = util.add_view(data)
    util.update_data(questions, question_id, "view_number", current_view_number, "question")
    return redirect(url_for("questions_and_answers", id=question_id))


@app.route('/question/<question_id>/vote-up', methods=['POST'])
def question_vote_up(question_id):
    questions = util.read_questions()
    data = util.choose_data(question_id)
    current_vote_number = util.change_votenum(data, "+")
    util.update_data(questions, question_id, "vote_number", current_vote_number, "question")
    return redirect('/')


@app.route('/question/<question_id>/vote-down', methods=['POST'])
def question_vote_down(question_id):
    questions = util.read_questions()
    data = util.choose_data(question_id)
    current_vote_number = util.change_votenum(data, "-")
    util.update_data(questions, question_id, "vote_number", current_vote_number, "question")
    return redirect('/')


@app.route('/questions/<id>/delete')
def delete_question(id):
    return render_template('delete.html', id=id)


@app.route('/questions/<id>/delete/deleted')
def deleted_question(id):
    answers = connection.read_question(data_operations.FILENAME_ANSWERS)
    deleted_answers = data_operations.delete_answer_with_question(id, answers)
    connection.write_questions(data_operations.FILENAME_ANSWERS, deleted_answers, data_operations.ANSWER_HEADER)

    questions = connection.read_question(data_operations.FILENAME_QUESTIONS)
    if questions[id]['image'] != ' ':
        data_operations.delete_image_file(questions[id]['image'])
    deleted_file = data_operations.delete_id_question(id, questions)
    connection.write_questions(data_operations.FILENAME_QUESTIONS, deleted_file, data_operations.QUESTION_HEADER)
    return render_template('deleted.html', id=id)


@app.route('/questions/<id>/answer_delete')
def delete_answer(id):
    answers = connection.read_question(data_operations.FILENAME_ANSWERS)
    deleted_answers = data_operations.delete_id_question(id, answers)
    connection.write_questions(data_operations.FILENAME_ANSWERS, deleted_answers, data_operations.ANSWER_HEADER)
    return render_template('answer_delete.html', id=id)


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
