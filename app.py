from flask import Flask, render_template, send_from_directory, request
from flask_socketio import SocketIO, send, emit
import emoji
import os
import random
import pprint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Y0L379iswHNAB9LdkmBXePZyz5dcB'
app.config['DEBUG'] = True
# app.config['HOST'] = '0.0.0.0'

socketio = SocketIO(app)

def xml_escape(chars, data_dict):
    return chars.encode('ascii', 'xmlcharrefreplace').decode()

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

@app.route('/')
def index():

    if request.remote_addr != '77.173.18.159' and request.remote_addr != '127.0.0.1':
        return '*** !!! ***'

    with open('data/teksten.txt') as bestand:
        data = bestand.read()

    regels = data.split("\n")
    data_into_list = [{"id":item.split(";")[0], "tekst":item.split(";")[1]} for item in regels]

    gedeelte = int((len(data_into_list)+1)/2)
    # print(gedeelte)
    teksten_in_tweeen = list(chunks(data_into_list, gedeelte))


    with open('data/emoticons.txt', mode="r") as bestand:
        emoticons = bestand.read().strip()

    patrons = ['Ryan', 'Timothy', 'Max', 'Radu', 'Thomas', 'Ciji', 'buddy', 'my friend', 'Jonathan', 'Ben', 'Marco', 'Mike', 'Carlos', 'Ronny']
    patrons_to_sort = [{'naam' : item, 'upper_naam' : item.upper()} for item in patrons]
    patrons = sorted(patrons_to_sort, key=lambda d: d['upper_naam'])

    gedeelte = int((len(patrons)+2)/3)
    # print(gedeelte)
    in_drieen = list(chunks(patrons, gedeelte))

    # pprint.pprint(list(in_drieen))
    # print(in_drieen[0])

    return render_template('index.html', emoticons=emoji.emojize(emoticons), patrons=in_drieen, teksten=teksten_in_tweeen)

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

    teksten = [item.split(";")[1] for item in data_into_list]

    return_tekst = ''
    if 'tekst' in json:
        return_tekst = teksten[int(json['tekst'])]
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

    # return_tekst += request.remote_addr

    if return_tekst:
        emit('from server', f'{return_tekst} {emoji.emojize(emoticons)}')
    else:
        emit('from server', emoji.emojize(emoticons))


if __name__ == '__main__':
    socketio.run(app)