from flask import Flask
from flask import render_template
from flask import request
from models.voice import api_process_return
from models.voice import api_server_play
from flask import jsonify
from flask import send_file
from models.userstatics import respone as userstatics_respone
from models.users import get_list_respone as users_get_list_respone
from models.users import get_list_respone_json as users_get_list_respone_json
from models.users import new_user_json
from models.users import edit_user_json
from models.record import get_list_respone as record_get_list_respone
from models.record import get_list_respone_json as record_get_list_respone_json
from models.files import get_list_respone as files_get_list_respone
from models.files import get_list_respone_json as files_get_list_respone_json
from models.files import upload
from models.files import edit_text
from models.words import get_list_respone as words_get_list_respone
from models.words import edit_words
from models.words import get_words
from models.sms import get_list_respone as sms_get_list_respone
from models.sms import get_list_respone_json as sms_get_list_respone_json
from models.home import main

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    respone = main()
    return render_template('index.html', respone=respone)


@app.route('/api/getmsg', methods=['GET'])
def get_voice():
    print("请求合成")
    text = request.args.get('text')
    select = request.args.get('select')
    uid = '1111'
    respone = api_process_return(text, select, uid)
    return jsonify(respone)


@app.route('/api/localplay/<filename>', methods=['GET'])
def get_local_play(filename):
    path = f"data/combined/{filename}"
    return send_file(path, mimetype="audio/wav")


@app.route('/api/serverplay', methods=['GET'])
def server_play():
    play = request.args.get('sound')
    respone = api_server_play(play)
    return jsonify(respone)

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/admin', methods=['GET'])
def admin_home():
    return render_template('admin.html')

@app.route('/admin/userstatics', methods=['GET'])
def admin_user_statics():
    respone = userstatics_respone()
    return render_template('userstatics.html', respone=respone)

@app.route('/admin/users', methods=['GET'])
def admin_users():
    page = 1
    respone = users_get_list_respone(page)
    return render_template('users.html', respone=respone)

@app.route('/admin/users/new',  methods=['POST'])
def admin_users_new():
    data = request.get_json()
    post_username = data.get('username')
    post_email = data.get('email')
    post_password = data.get('password')
    respone = new_user_json(post_username, post_email, post_password)
    return jsonify(respone)


@app.route('/admin/users/edit',  methods=['POST'])
def admin_users_edit():
    data = request.get_json()
    post_uid = data.get('uid')
    post_username = data.get('username')
    post_email = data.get('email')
    post_password = data.get('password')
    print(post_username)
    print(post_uid)
    respone = edit_user_json(post_uid, post_username, post_email, post_password)
    return jsonify(respone)


@app.route('/admin/users/page', methods=['GET'])
def admin_users_page():
    page = request.args.get('page')
    respone = users_get_list_respone_json(page)
    return jsonify(respone)

@app.route('/admin/record', methods=['GET'])
def admin_record():
    page = 1
    respone = record_get_list_respone(page)
    return render_template('record.html', respone=respone)

@app.route('/admin/record/page', methods=['GET'])
def admin_record_page():
    page = request.args.get('page')
    respone = record_get_list_respone_json(page)
    return jsonify(respone)

@app.route('/admin/voices', methods=['GET'])
def admin_voices():
    page = 1
    respone = files_get_list_respone(page)
    return render_template('voices.html', respone=respone)

@app.route('/admin/voices/page', methods=['GET'])
def admin_voices_page():
    page = request.args.get('page')
    respone = files_get_list_respone_json(page)
    return jsonify(respone)


@app.route('/admin/voices/upload', methods=['POST'])
def admin_voices_upload():
    file = request.files['file']
    respone = upload(file)
    return jsonify(respone)

@app.route('/admin/voices/edit', methods=['POST'])
def admin_voices_edit():
    data = request.get_json()
    input_id = data.get('id')
    input_text = data.get('edit_text')
    respone = edit_text(input_id, input_text)
    return jsonify(respone)

@app.route('/admin/words', methods=['GET'])
def admin_words():
    respone = words_get_list_respone()
    return render_template('words.html', respone=respone)

@app.route('/admin/words/edit', methods=['POST'])
def admin_words_edit():
    data = request.get_json()
    edit_text = data.get("text")
    respone = edit_words(edit_text)
    return jsonify(respone)

@app.route('/admin/words/get', methods=['GET'])
def admin_words_get():
    respone = get_words()
    return jsonify(respone)

@app.route('/admin/sms', methods=['GET'])
def admin_sms():
    page = 1
    respone = sms_get_list_respone(page)
    return render_template('sms.html', respone=respone)

@app.route('/admin/sms/page', methods=['GET'])
def admin_sms_page():
    page = request.args.get('page')
    respone = sms_get_list_respone_json(page)
    return jsonify(respone)

@app.route('/admin/logs', methods=['GET'])
def admin_logs():
    respone = None
    return render_template('logs.html')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="4567")