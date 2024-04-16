from flask import Flask
from flask import render_template
from flask import request
from models.voice import api_process_return
from models.voice import api_server_play
from flask import jsonify
from flask import send_file
from models.userstatics import respone as userstatics_respone

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
    respone = None
    return render_template('users.html')

@app.route('/admin/record')
def admin_record():
    respone = None
    return render_template('record.html')

@app.route('/admin/voices')
def admin_voices():
    respone = None
    return render_template('voices.html')

@app.route('/admin/words')
def admin_words():
    respone = None
    return render_template('words.html')

@app.route('/admin/sms')
def admin_sms():
    respone = None
    return render_template('sms.html')

@app.route('/admin/logs')
def admin_logs():
    respone = None
    return render_template('logs.html')



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="4567")