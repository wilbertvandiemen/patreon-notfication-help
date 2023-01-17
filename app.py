from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, send, emit
import emoji
import os
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Y0L379iswHNAB9LdkmBXePZyz5dcB'
# app.config['DEBUG'] = True
# app.config['HOST'] = '0.0.0.0'

socketio = SocketIO(app)

def xml_escape(chars, data_dict):
    return chars.encode('ascii', 'xmlcharrefreplace').decode()

@app.route('/')
def index():
    with open('data/teksten.txt') as bestand:
        data = bestand.read()
        data_into_list = data.split("\n")

    with open('data/emoticons.txt', mode="r") as bestand:
        emoticons = bestand.read().strip()

    patrons = ['Ryan', 'Timothy', 'Max', 'Radu', 'Thomas', 'Ciji', 'buddy', 'my friend', 'Jonathan', 'Ben', 'Marco', 'Mike', 'Carlos', 'Ronny']
    patrons = sorted(patrons)

    return render_template('index.html', emoticons=emoji.emojize(emoticons), patrons=patrons, teksten=data_into_list)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon/favicon.ico', mimetype='image/vnd.microsoft.icon')

@socketio.on('message')
def receive_message(json):

    # print(json)

    if not 'naam' in json:
        json['naam'] = 'onbekend'

    with open('data/teksten.txt') as bestand:
        data = bestand.read()
        data_into_list = data.split("\n")

    return_tekst = ''
    if 'tekst' in json:
        return_tekst = data_into_list[int(json['tekst'])]
        if return_tekst == '<<alleen emoticons>>':
            return_tekst = ''
        if not return_tekst.find('@@') == -1:
            return_tekst = return_tekst.replace('@@', json['naam'] )

    # schrijf emoticons weg
    with open('data/emoticons.txt', mode="w") as bestand:
        bestand.write(emoji.demojize(json["emoticons"]))

    # voor de respons slechts twee emoticons
    with open('data/emoticons.txt', mode="r") as bestand:
        emoticons = bestand.read().strip()

    emoticons_array = emoticons.split("::")
    emoticons_array = [item.replace(':','') for item in emoticons_array]
    random.shuffle(emoticons_array)
    emoticons_array = emoticons_array[:2]
    emoticons_array = [':' + item + ':' for item in emoticons_array]
    emoticons = ''.join(emoticons_array)

    if return_tekst:
        emit('from server', f'{return_tekst} {emoji.emojize(emoticons)}')
    else:
        emit('from server', emoji.emojize(emoticons))


if __name__ == '__main__':
    socketio.run(app)