from flask import Flask, request, jsonify, json
import requests,json
from bs4 import BeautifulSoup
app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def welcome():
    return '<h1 style="text-align: center" >Yokoso, Lister api ye</h1>'

@app.route('/<string:name>/', methods=['GET','POST'])
def details(name):
    source = requests.get('https://ww1.9anime2.com/watch/'+name).text
    soup = BeautifulSoup(source, "html.parser")

    status = soup.select_one('div.col1').find_all('div')[2].text.split()[1]
    epstotal = len(soup.select_one('div.body').find_all('li'))

    return {
        'error' : False,
        'status' : status,
        'epstotal' : epstotal
    }

if __name__ == '__main__':
    app.run(threaded=True, port=5000)