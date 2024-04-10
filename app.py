from flask import Flask
from flask import render_template
from flask import request
from models.voice import api_process_return
from models.voice import api_server_play
from flask import jsonify
from flask import send_file

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/getmsg')
def get_voice():
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

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="4567")