from flask import Flask
from flask import session
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect
from models.voice import api_process_return
from models.voice import api_server_play
from flask import jsonify
from flask import send_file
from models.userstatics import respone as userstatics_respone
from models.userstatics import online
from models.users import get_list_respone as users_get_list_respone
from models.users import get_list_respone_json as users_get_list_respone_json
from models.users import new_user_json
from models.users import edit_user_json
from models.users import user_auth
from models.users import query_update_login_time
from models.users import api_user_info_json
from models.users import admin_auth
from models.record import get_list_respone as record_get_list_respone
from models.record import get_list_respone_json as record_get_list_respone_json
from models.record import get_today_record_count
from models.files import get_list_respone as files_get_list_respone
from models.files import get_list_respone_json as files_get_list_respone_json
from models.files import upload
from models.files import edit_text
from models.words import get_list_respone as words_get_list_respone
from models.words import edit_words
from models.words import get_words
from models.sms import get_list_respone as sms_get_list_respone
from models.sms import get_list_respone_json as sms_get_list_respone_json
from models.sms import send_smss
from models.home import main
from loguru import logger

logger.add("logs/log.log", rotation="00:00", retention="7 days")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'zm239238kj8234jkfjisui'

@app.route('/', methods=['GET'])
def home():
    session_username = session.get('username')
    session_password = session.get('password')
    logger.info(f"{session_username}: /")
    auth = user_auth(str(session_username), str(session_password))
    if auth:
        respone = main()
        return render_template('index.html', respone=respone)
    else:
        session.clear()
        return render_template('nouser.html')


@app.route('/login/auth', methods=['GET'])
def login_auth():
    input_username = request.args.get('username')
    input_password = request.args.get('password')
    logger.info(f"{input_username}: /login/auth")
    auth = user_auth(str(input_username), str(input_password))
    usertype = admin_auth(input_username)
    if auth:
        session['username'] = input_username
        session['password'] = input_password
        session['usertype'] = usertype
        query_update_login_time(input_username)
        return redirect(url_for('home'))
    else:
        return render_template('nouser.html')


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/logout', methods=['GET'])
def logout():
    session_username = session.get('username')
    session_password = session.get('password')
    logger.info(f"{session_username}: /logout")
    session.clear()
    return redirect(url_for('login'))


@app.route('/api/getmsg', methods=['GET'])
def get_voice():
    text = request.args.get('text')
    select = request.args.get('select')
    session_username = session.get('username')
    session_password = session.get('password')
    logger.info(f"{session_username}: /api/getmsg")
    auth = user_auth(str(session_username), str(session_password))
    if auth:
        respone = api_process_return(text, select, session_username)
        return jsonify(respone)
    else:
        data = {}
        data['msg'] = 'not login'
        return jsonify(data)


@app.route('/api/localplay/<filename>', methods=['GET'])
def get_local_play(filename):
    session_username = session.get('username')
    session_password = session.get('password')
    logger.info(f"{session_username}: /api/localplay/{filename}")
    auth = user_auth(str(session_username), str(session_password))
    if auth:
        path = f"data/combined/{filename}"
        return send_file(path, mimetype="audio/wav")
    else:
        session.clear()
        data = {}
        data['msg'] = 'not login'
        return jsonify(data)


@app.route('/api/serverplay', methods=['GET'])
def server_play():
    session_username = session.get('username')
    session_password = session.get('password')
    logger.info(f"{session_username}: /api/serverplay")
    auth = user_auth(str(session_username), str(session_password))
    if auth:
        play = request.args.get('sound')
        respone = api_server_play(play)
        return jsonify(respone)
    else:
        session.clear()
        data = {}
        data['msg'] = 'not login'
        return jsonify(data)


@app.route('/api/online', methods=['POST'])
def api_online():
    session_username = session.get('username')
    session_password = session.get('password')
    logger.info(f"{session_username}: /api/online")
    auth = user_auth(str(session_username), str(session_password))
    if auth:
        respone = online(session_username)
        return jsonify(respone)
    else:
        session.clear()
        data = {}
        data['msg'] = 'not login'
        return jsonify(data)


@app.route('/api/userinfo/get', methods=['GET'])
def api_user_info():
    session_username = session.get('username')
    session_password = session.get('password')
    logger.info(f"{session_username}: /api/userinfo/get")
    auth = user_auth(str(session_username), str(session_password))
    if auth:
        respone = api_user_info_json(session_username)
        return jsonify(respone)
    else:
        session.clear()
        data = {}
        data['msg'] = 'not login'
        return jsonify(data)
    

@app.route('/api/combined/count/get', methods=['GET'])
def api_combined_count():
    session_username = session.get('username')
    session_password = session.get('password')
    logger.info(f"{session_username}: /api/combined/count/get")
    auth = user_auth(str(session_username), str(session_password))
    if auth:
        respone = get_today_record_count(session_username)
        return jsonify(respone)
    else:
        session.clear()
        data = {}
        data['msg'] = 'not login'
        return jsonify(data)

@app.route('/api/sendsms', methods=['GET'])
def api_sendsms():
    session_username = session.get('username')
    session_password = session.get('password')
    logger.info(f"{session_username}: /api/sendsms")
    auth = user_auth(str(session_username), str(session_password))
    if auth:
        respone = send_smss()
        return jsonify(respone)
    else:
        session.clear()
        data = {}
        data['msg'] = 'not login'
        return jsonify(data)


@app.route('/admin', methods=['GET'])
def admin_home():
    session_username = session.get('username')
    session_password = session.get('password')
    session_usertype = session.get('usertype')
    logger.info(f"{session_username}: /admin")
    auth = user_auth(str(session_username), str(session_password))
    if auth and session_usertype=="1":
        return render_template('admin.html')
    else:
        session.clear()
        return render_template('nouser.html')


@app.route('/admin/userstatics', methods=['GET'])
def admin_user_statics():
    session_username = session.get('username')
    session_password = session.get('password')
    session_usertype = session.get('usertype')
    logger.info(f"{session_username}: /admin/userstatics")
    auth = user_auth(str(session_username), str(session_password))
    if auth and session_usertype=="1":
        respone = userstatics_respone()
        return render_template('userstatics.html', respone=respone)
    else:
        session.clear()
        return render_template('nouser.html')
        

@app.route('/admin/users', methods=['GET'])
def admin_users():
    session_username = session.get('username')
    session_password = session.get('password')
    session_usertype = session.get('usertype')
    logger.info(f"{session_username}: /admin/users")
    auth = user_auth(str(session_username), str(session_password))
    if auth and session_usertype=="1":
        page = 1
        respone = users_get_list_respone(page)
        return render_template('users.html', respone=respone)
    else:
        session.clear()
        return render_template('nouser.html')


@app.route('/admin/users/new',  methods=['POST'])
def admin_users_new():
    session_username = session.get('username')
    session_password = session.get('password')
    session_usertype = session.get('usertype')
    logger.info(f"{session_username}: /admin/users/new")
    auth = user_auth(str(session_username), str(session_password))
    if auth and session_usertype=="1":
        data = request.get_json()
        post_username = data.get('username')
        post_email = data.get('email')
        post_password = data.get('password')
        respone = new_user_json(post_username, post_email, post_password)
        return jsonify(respone)
    else:
        session.clear()
        data = {}
        data['msg'] = 'not login'
        return jsonify(data)


@app.route('/admin/users/edit',  methods=['POST'])
def admin_users_edit():
    session_username = session.get('username')
    session_password = session.get('password')
    session_usertype = session.get('usertype')
    logger.info(f"{session_username}: /admin/users/edit")
    auth = user_auth(str(session_username), str(session_password))
    if auth and session_usertype=="1":
        data = request.get_json()
        post_uid = data.get('uid')
        post_username = data.get('username')
        post_email = data.get('email')
        post_password = data.get('password')
        respone = edit_user_json(post_uid, post_username, post_email, post_password)
        return jsonify(respone)
    else:
        session.clear()
        data = {}
        data['msg'] = 'not login'
        return jsonify(data)


@app.route('/admin/users/page', methods=['GET'])
def admin_users_page():
    session_username = session.get('username')
    session_password = session.get('password')
    session_usertype = session.get('usertype')
    logger.info(f"{session_username}: /admin/users/page")
    auth = user_auth(str(session_username), str(session_password))
    if auth and session_usertype=="1":
        page = request.args.get('page')
        respone = users_get_list_respone_json(page)
        return jsonify(respone)
    else:
        session.clear()
        data = {}
        data['msg'] = 'not login'
        return jsonify(data)

@app.route('/admin/record', methods=['GET'])
def admin_record():
    session_username = session.get('username')
    session_password = session.get('password')
    session_usertype = session.get('usertype')
    logger.info(f"{session_username}: /admin/record")
    auth = user_auth(str(session_username), str(session_password))
    if auth and session_usertype=="1":
        page = 1
        respone = record_get_list_respone(page)
        return render_template('record.html', respone=respone)
    else:
        session.clear()
        return render_template('nouser.html')


@app.route('/admin/record/page', methods=['GET'])
def admin_record_page():
    session_username = session.get('username')
    session_password = session.get('password')
    session_usertype = session.get('usertype')
    logger.info(f"{session_username}: /admin/record/page")
    auth = user_auth(str(session_username), str(session_password))
    if auth and session_usertype=="1":
        page = request.args.get('page')
        respone = record_get_list_respone_json(page)
        return jsonify(respone)
    else:
        session.clear()
        data = {}
        data['msg'] = 'not login'
        return jsonify(data)
    

@app.route('/admin/voices', methods=['GET'])
def admin_voices():
    session_username = session.get('username')
    session_password = session.get('password')
    session_usertype = session.get('usertype')
    logger.info(f"{session_username}: /admin/voices")
    auth = user_auth(str(session_username), str(session_password))
    if auth and session_usertype=="1":
        page = 1
        respone = files_get_list_respone(page)
        return render_template('voices.html', respone=respone)
    else:
        session.clear()
        return render_template('nouser.html')


@app.route('/admin/voices/page', methods=['GET'])
def admin_voices_page():
    session_username = session.get('username')
    session_password = session.get('password')
    session_usertype = session.get('usertype')
    logger.info(f"{session_username}: /admin/voices/page")
    auth = user_auth(str(session_username), str(session_password))
    if auth and session_usertype=="1":
        page = request.args.get('page')
        respone = files_get_list_respone_json(page)
        return jsonify(respone)
    else:
        session.clear()
        data = {}
        data['msg'] = 'not login'
        return jsonify(data)


@app.route('/admin/voices/upload', methods=['POST'])
def admin_voices_upload():
    session_username = session.get('username')
    session_password = session.get('password')
    session_usertype = session.get('usertype')
    logger.info(f"{session_username}: /admin/voices/upload")
    auth = user_auth(str(session_username), str(session_password))
    if auth and session_usertype=="1":
        file = request.files['file']
        respone = upload(file)
        return jsonify(respone)
    else:
        session.clear()
        data = {}
        data['msg'] = 'not login'
        return jsonify(data)


@app.route('/admin/voices/edit', methods=['POST'])
def admin_voices_edit():
    session_username = session.get('username')
    session_password = session.get('password')
    session_usertype = session.get('usertype')
    logger.info(f"{session_username}: /admin/voices/edit")
    auth = user_auth(str(session_username), str(session_password))
    if auth and session_usertype=="1":
        data = request.get_json()
        input_id = data.get('id')
        input_text = data.get('edit_text')
        respone = edit_text(input_id, input_text)
        return jsonify(respone)
    else:
        session.clear()
        data = {}
        data['msg'] = 'not login'
        return jsonify(data)


@app.route('/admin/words', methods=['GET'])
def admin_words():
    session_username = session.get('username')
    session_password = session.get('password')
    session_usertype = session.get('usertype')
    logger.info(f"{session_username}: /admin/words")
    auth = user_auth(str(session_username), str(session_password))
    if auth and session_usertype=="1":
        respone = words_get_list_respone()
        return render_template('words.html', respone=respone)
    else:
        session.clear()
        return render_template('nouser.html')


@app.route('/admin/words/edit', methods=['POST'])
def admin_words_edit():
    session_username = session.get('username')
    session_password = session.get('password')
    session_usertype = session.get('usertype')
    logger.info(f"{session_username}: /admin/words/edit")
    auth = user_auth(str(session_username), str(session_password))
    if auth and session_usertype=="1":
        data = request.get_json()
        edit_text = data.get("text")
        respone = edit_words(edit_text)
        return jsonify(respone)
    else:
        session.clear()
        data = {}
        data['msg'] = 'not login'
        return jsonify(data)


@app.route('/admin/words/get', methods=['GET'])
def admin_words_get():
    session_username = session.get('username')
    session_password = session.get('password')
    session_usertype = session.get('usertype')
    logger.info(f"{session_username}: /admin/words/get")
    auth = user_auth(str(session_username), str(session_password))
    if auth and session_usertype=="1":
        respone = get_words()
        return jsonify(respone)


@app.route('/admin/sms', methods=['GET'])
def admin_sms():
    session_username = session.get('username')
    session_password = session.get('password')
    session_usertype = session.get('usertype')
    logger.info(f"{session_username}: /admin/sms")
    auth = user_auth(str(session_username), str(session_password))
    if auth and session_usertype=="1":
        page = 1
        respone = sms_get_list_respone(page)
        return render_template('sms.html', respone=respone)
    else:
        session.clear()
        data = {}
        data['msg'] = 'not login'
        return jsonify(data)


@app.route('/admin/sms/page', methods=['GET'])
def admin_sms_page():
    session_username = session.get('username')
    session_password = session.get('password')
    session_usertype = session.get('usertype')
    logger.info(f"{session_username}: /admin/sms/page")
    auth = user_auth(str(session_username), str(session_password))
    if auth and session_usertype=="1":
        page = request.args.get('page')
        respone = sms_get_list_respone_json(page)
        return jsonify(respone)
    else:
        session.clear()
        return render_template('nouser.html')


@app.route('/admin/logs', methods=['GET'])
def admin_logs():
    session_username = session.get('username')
    session_password = session.get('password')
    session_usertype  =  session.get('usertype')
    logger.info(f"{session_username}: /admin/logs")
    auth = user_auth(str(session_username), str(session_password))
    if auth and session_usertype=="1":
        respone = None
        return render_template('logs.html')
    else:
        session.clear()
        return render_template('nouser.html')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="4567")