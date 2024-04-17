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
from models.record import get_list_respone as record_get_list_respone
from models.files import get_list_respone as files_get_list_respone
from models.words import get_list_respone as words_get_list_respone
from models.sms import get_list_respone as sms_get_list_respone

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/getmsg')
def get_voice():
    print("请求合成")
    text = request.args.get('text')
    select = request.args.get('select')
    respone = api_process_return(text, select)
    return jsonify(respone)


@app.route('/api/localplay/<filename>')
def get_local_play(filename):
    path = f"cache/combined/{filename}"
    return send_file(path, mimetype="audio/wav")


@app.route('/api/serverplay')
def server_play():
    play = request.args.get('sound')
    respone = api_server_play(play)
    return jsonify(respone)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/admin')
def admin_home():
    return render_template('admin.html')

@app.route('/admin/userstatics')
def admin_user_statics():
    respone = userstatics_respone()
    return render_template('userstatics.html', respone=respone)

@app.route('/admin/users')
def admin_users():
    page = 1
    respone = users_get_list_respone(page)
    return render_template('users.html', respone=respone)

@app.route('/admin/users/page')
def admin_users_page():
    page = request.args.get('page')
    respone = users_get_list_respone_json(page)
    return jsonify(respone)

@app.route('/admin/record')
def admin_record():
    page = 1
    respone = record_get_list_respone(page)
    return render_template('record.html', respone=respone)

@app.route('/admin/voices')
def admin_voices():
    page = 1
    respone = files_get_list_respone(page)
    return render_template('voices.html', respone=respone)

@app.route('/admin/words')
def admin_words():
    respone = words_get_list_respone()
    return render_template('words.html', respone=respone)

@app.route('/admin/sms')
def admin_sms():
    page = 1
    respone = sms_get_list_respone(page)
    return render_template('sms.html', respone=respone)

@app.route('/admin/logs')
def admin_logs():
    respone = None
    return render_template('logs.html')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="4567")