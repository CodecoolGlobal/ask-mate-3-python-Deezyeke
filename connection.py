import data_operations
import server


def init_answer(header):
    answer = {}
    for field in header:
        answer[field] = ' '
    answer['id'] = data_operations.create_id()
    answer['vote_number'] = 0
    return answer


def add_data_for_csv(q_id):
    answer = init_answer(data_operations.ANSWER_HEADER)
    now = server.datetime.now()
    answer['submission_time'] = now.strftime("%Y/%m/%d %H:%M:%S")
    answer['question_id'] = q_id
    answer['message'] = server.request.form.get('message')
    uploaded_file = server.request.files['image_file']
    if uploaded_file.filename != '':
        uploaded_file.save('./static/' + uploaded_file.filename)
    answer['image'] = uploaded_file.filename
    data_operations.save_data(answer, data_operations.FILENAME_ANSWERS, data_operations.ANSWER_HEADER)
