from flask import Flask, render_template, request, redirect, url_for, session
import util
from util import verify_password
import data_handler
import os
from datetime import datetime, date
from dotenv import load_dotenv
from util import generate_hash
from data_handler import add_new_user
from data_handler import get_user_password
import psycopg2
from datetime import date
from data_handler import get_questions_tags


load_dotenv()
app = Flask(__name__)
app.secret_key = b'lgheroh42_4243'


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'GET':
        return render_template('registration.html', already_taken=False)
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        password_hashed_text = generate_hash(password).decode()
        reg_date = date.today()
        try:
            add_new_user(email, password_hashed_text, reg_date)
        except psycopg2.errors.UniqueViolation:
            return render_template('registration.html', already_taken=True)
        else:
            return redirect('/')


@app.route('/index', methods=['GET', 'POST'])
def login():
    email = request.form.get("email")
    password_entered_by_user_text = request.form.get("password")
    if request.method == 'POST':
        password_hashed_text = get_user_password(email)["password"]  # get password from database
        user_id = get_user_password(email)["id"]
        try:

            if verify_password(password_entered_by_user_text,
                               password_hashed_text.encode()):  # checking password if given pw is the same as in DB
                session['email'] = request.form['email']
                session['user_id'] = user_id
                return redirect(url_for('questions_list', email=email))
            else:
                return render_template('login.html', log_in_failed=True)
        except:
            return render_template('login.html', log_in_failed=True)
    else:
        return render_template("login.html", log_in_failed=False)


@app.route("/logout")
def logout():
    session.pop("email")
    # session.pop("user_id")
    return redirect("/")


@app.route('/questions_list')
def questions_list():
    # alapvetően submit time desc és csak 5öt mutat, legördülő menüből választható mi alapján order-elje:
    if request.method == 'GET':
        submission_time = request.args.get('submission_time', 'view_number')
        # if submission_time:
        desc_by_time = data_handler.get_last_five_questions('submission_time')
        # views = data_handler.get_view_number('view_number')
        search_value = request.args.get('search')
        if search_value == None:
            ti = 'title'
            return render_template('questions_list.html', questions=desc_by_time, orderby='title', view_number='views',
                                   question_header=data_handler.QUESTION_HEADER, email=session["email"])
        else:
            found = data_handler.search_questions(search_value)
            print(found)
            return render_template('questions_list.html', questions=found, orderby='title', view_number='views',
                                   question_header=data_handler.QUESTION_HEADER, email=session["email"])


# Extra idea: #a többi "old" questions akkor legyen csak látható, ha az utolsó 5 alatti linkre kattint pl show all questions névvel


@app.route('/all-question')
def display_all_question():
    questions = data_handler.get_all_questions()
    search_value = request.args.get('search')
    if search_value == None:
        return render_template('questions_list.html', questions=questions, orderby='title', view_number='views',
                               question_header=data_handler.QUESTION_HEADER, email=session["email"])
    else:
        found = data_handler.search_questions(search_value)
        return render_template('questions_list.html', questions=found, orderby='title', view_number='views',
                               question_header=data_handler.QUESTION_HEADER, email=session["email"])


@app.route('/question/<q_id>/view')
def increase_view(q_id):
    data_handler.increase_view_number(q_id)
    return redirect(url_for('display_question', q_id=q_id))


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
        question['user_id'] = session['user_id']
        uploaded_file = request.files['image_file']
        if uploaded_file.filename != '':
            uploaded_file.save(os.path.join('static', uploaded_file.filename))
            question['image'] = uploaded_file.filename

        data_handler.save_new_question(question)

        return redirect(url_for('questions_list', email=session["email"]))


@app.route('/question/<id>/edit', methods=['GET', 'POST'])
def edit_question(id):
    if request.method == 'GET':
        question = data_handler.get_question(id)
        return render_template('edit_question.html', id=id, title=question['title'], message=question['message'],
                               image=question['image'])
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

        return redirect(url_for('display_question', q_id=id))


@app.route('/answer/<a_id>/edit', methods=['GET', 'POST'])
def edit_answer(a_id):
    if request.method == 'GET':
        answers = data_handler.get_all_answers()
        for answer in answers:
            if str(answer['id']) == a_id:
                return render_template('edit_answer.html', a_id=a_id, answer=answer)
    elif request.method == 'POST':
        message = request.form.get('add-answer')
        data_handler.update_answer(a_id, message)
        q_id_lst = data_handler.search_q_id_by_a_id(a_id)
        for q_id in q_id_lst:
            return redirect(url_for('display_question', q_id=q_id['question_id']))


@app.route('/display-question/<q_id>')
def display_question(q_id):
    q_comments = data_handler.read_q_comments_by_id(q_id)
    a_comments = data_handler.read_a_comments()
    questions = []
    answers = []

    question_tags = data_handler.get_question_tags(q_id)
    if len(question_tags) == 0:
        question_tags = None

    for question in data_handler.get_all_questions():
        for key, value in question.items():
            if key == 'id' and str(value) == q_id:
                questions.append(question)
    for answer in data_handler.get_all_answers():
        for key, value in answer.items():
            if key == 'question_id' and str(value) == q_id:
                answers.append(answer)
    return render_template('display_question.html', question=questions, answer=answers, q_id=q_id,
                           q_comments=q_comments,
                           a_comment=a_comments, question_tags=question_tags)


@app.route('/question/<q_id>/vote/<up_or_down>', methods=['POST'])
def add_vote(q_id, up_or_down):
    data_handler.change_vote_number(q_id, 'question', up_or_down)
    return redirect(url_for('questions_list', email=session["email"]))


@app.route('/question/<q_id>/<answer_id>/vote/<up_or_down>', methods=['POST'])
def add_answer_vote(q_id, answer_id, up_or_down):
    data_handler.change_vote_number(answer_id, 'answer', up_or_down)
    return redirect(url_for('display_question', q_id=q_id))


@app.route('/display-question/<q_id>/delete', methods=['GET', 'POST'])
def delete_question(q_id):
    if request.method == 'GET':
        return render_template('question_delete.html', q_id=q_id)
    else:
        question_image = data_handler.get_image_name_form_question(q_id)
        if question_image['image'] != None:
            data_handler.delete_image_file(question_image['image'])
        answer_images = data_handler.get_images_names(q_id)
        for row in answer_images:
            if row['image'] != None:
                data_handler.delete_image_file(row['image'])
        answers = data_handler.get_answers_with_question_id(q_id)
        for answer in answers:
            data_handler.delete_answer_comment_with_question_deleted(answer['id'])
        data_handler.delete_tag_with_question(q_id)
        data_handler.delete_comment_with_question(q_id)
        data_handler.delete_answer_with_question(q_id)
        data_handler.delete_question(q_id)
        return redirect(url_for('questions_list', email=session["email"]))


@app.route('/question/<q_id>/add-new-answer', methods=['GET', 'POST'])
def add_new_answer(q_id):
    if request.method == 'GET':
        return render_template('new_answer.html', q_id=q_id)
    elif request.method == 'POST':
        answer = util.create_empty_answer()
        now = datetime.now()
        answer['submission_time'] = now.strftime("%Y/%m/%d %H:%M:%S")
        answer['message'] = request.form.get('message')
        answer['question_id'] = q_id
        answer['user_id'] = session['user_id']
        uploaded_file = request.files['image_file']
        if uploaded_file.filename != '':
            uploaded_file.save(os.path.join('static', uploaded_file.filename))
            answer['image'] = uploaded_file.filename
        data_handler.add_answer_to_question(answer)
        return redirect(url_for('display_question', q_id=q_id))


@app.route('/display-question/<q_id>/delete_answer/<a_id>', methods=['GET', 'POST'])
def delete_answer(q_id, a_id):
    if request.method == 'GET':
        return render_template('answer_delete.html', q_id=q_id, a_id=a_id)
    else:
        answer_image = data_handler.get_image_name_from_answer(a_id)
        if answer_image['image'] != None:
            data_handler.delete_image_file(answer_image['image'])
        data_handler.delete_answer(a_id)
        return redirect(url_for('display_question', q_id=q_id, a_id=a_id))


@app.route('/question/<q_id>/comments', methods=['GET', 'POST'])
def add_comment_to_question(q_id):
    if request.method == 'GET':
        for question in data_handler.get_all_questions():
            for key, value in question.items():
                if key == 'id' and str(value) == q_id:
                    return render_template('add_comment_to_question.html', q_id=q_id, question=question)
    elif request.method == 'POST':
        now = datetime.now()
        comment = {'message': request.form.get('add-comment'), 'submission_time': now.strftime("%Y/%m/%d %H:%M:%S"),
                   'question_id': q_id, 'user_id': session['user_id']}
        data_handler.add_comment_to_question(comment)
        return redirect(url_for('display_question', q_id=q_id))


@app.route('/question/<q_id>/comment_delete/<c_id>', methods=['GET', 'POST'])
def delete_comment_from_question(q_id, c_id):
    if request.method == 'GET':
        return render_template('comment_delete_form_question.html', q_id=q_id, c_id=c_id)
    else:
        data_handler.delete_comment_from_question(q_id, c_id)
        return redirect(url_for('display_question', q_id=q_id))


@app.route('/answer/<a_id>/new-comment', methods=['GET', 'POST'])
def add_comment_to_answer(a_id):
    list_q_id = data_handler.search_q_id_by_a_id(a_id)
    if request.method == 'GET':
        for answer in data_handler.get_all_answers():
            for key, value in answer.items():
                if key == 'id' and str(value) == a_id:
                    return render_template('add_comment_to_answer.html', a_id=a_id, answer=answer)
    elif request.method == 'POST':
        for row in list_q_id:
            now = datetime.now()
            comment = {'message': request.form.get('add-comment'), 'submission_time': now.strftime("%Y/%m/%d %H:%M:%S"),
                       'answer_id': a_id, 'user_id': session['user_id']}
            data_handler.add_comment_to_answer(comment)
            return redirect(url_for('display_question', q_id=row['question_id']))


@app.route('/question/<q_id>/<a_id>/delete_comment/<c_id>', methods=['GET', 'POST'])
def delete_comment_from_answer(q_id, a_id, c_id):
    if request.method == 'GET':
        return render_template('comment_delete_from_answer.html', q_id=q_id, a_id=a_id, c_id=c_id)
    else:
        data_handler.delete_comment_from_answer(a_id, c_id)
        return redirect(url_for('display_question', q_id=q_id))


@app.route('/question/<question_id>/new-tag', methods=['GET', 'POST'])
def add_new_tag(question_id):
    question = data_handler.get_question(question_id)
    question_tags = data_handler.get_question_tags(question_id)
    tags = data_handler.get_tags()

    if request.method == 'GET':
        if len(question_tags) == 0:
            question_tags = None
        return render_template('add_tag.html', question_id=question_id, message=question['message'],
                               question_tags=question_tags, tags=tags)
    elif request.method == 'POST':
        new_tag = request.form.get('new_tag')
        choose_tag_id = request.form.get('choose_tag')
        if new_tag:
            data_handler.add_new_tag(new_tag)
            return redirect(url_for('add_new_tag', question_id=question_id))
        if choose_tag_id:
            data_handler.add_new_tag_to_question(question_id, choose_tag_id)
            return redirect(url_for('add_new_tag', question_id=question_id))


@app.route('/question/<question_id>/tag/<tag_id>/delete')
def delete_tag(question_id, tag_id):
    data_handler.delete_question_tag(question_id, tag_id)
    return redirect(url_for('display_question', q_id=question_id))


@app.route('/comment/<c_id>/edit', methods=['GET', 'POST'])
def edit_comment(c_id):
    a_comment = util.select_needed_data('id', c_id, data_handler.read_all_comments())
    if request.method == 'GET':
        for comment in a_comment:
            return render_template('edit_comment.html', comment=comment)
    if request.method == 'POST':
        now = datetime.now()
        message = request.form.get('add-comment')
        data_handler.update_commit(c_id, message, now.strftime("%Y/%m/%d %H:%M:%S"))
        for comment in a_comment:
            if comment['question_id'] is not None:
                return redirect(url_for('display_question', q_id=comment['question_id']))
            else:
                q_id = data_handler.get_qid_by_aid(comment['answer_id'])
                for id in q_id:
                    return redirect(url_for('display_question', q_id=id['question_id']))


@app.route('/users')
def users():
    all_info_by_mail = {}
    all_usermail = []
    for row in data_handler.get_all_username():
        for k, value in row.items():
            all_usermail.append(value)
    for user in all_usermail:
        counts = [
            data_handler.get_user_registration_date(user), data_handler.get_user_question_count(user),
            data_handler.get_user_answer_count(user), data_handler.get_user_comment_count(user)
        ]
        all_info_by_mail[user] = counts
    if 'email' in session:
        return render_template('user_information.html', users=all_info_by_mail)
    else:
        return redirect(url_for('index'))


@app.route('/tags')
def tags():
    questions_tags = get_questions_tags()
    return render_template('tags.html', questions_tags=questions_tags, email=session['email'])


@app.route('/user/<user>')
def get_user_info(user):
    user_id = data_handler.get_user_id_by_email(user)
    user_info = data_handler.get_user_info(user_id['id'])
    user_q_count = data_handler.get_user_question_count(user)
    user_a_count = data_handler.get_user_answer_count(user)
    user_c_count = data_handler.get_user_comment_count(user)
    user_questions = data_handler.get_questions_by_user_id(user_id['id'])
    user_answers = data_handler.get_answers_by_user_id(user_id['id'])
    user_comments = data_handler.get_comments_by_user_id(user_id['id'])
    return render_template('user_page.html', user_info=user_info, user_q_count=user_q_count, user_a_count=user_a_count,
                           user_c_count=user_c_count, user_questions=user_questions, user_answers=user_answers,
                           user_comments=user_comments)


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
    )
