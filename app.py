from flask import Flask, Request, request, jsonify, json
from bs4 import BeautifulSoup
app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>Yokoso, Lister api ye</h1>"


@app.route('/<string:name>/')
def details(name):
    source = Request.get('https://animixplay.to/v1/'+name).text
    soup = BeautifulSoup(source, "html.parser")

    if soup.select_one('span.animetitle').get_text() == 'Generating...':
        return {
            'error' : True,
        }

    status = soup.select_one('span#status').get_text().split(' ')[2]
    epstotal = json.loads(soup.select_one('div#epslistplace').get_text())['eptotal']

    return {
        'error' : False,
        'status' : status,
        'epstotal' : epstotal
    }


if __name__ == '__main__':
    app.run(threaded=True, port=5000)