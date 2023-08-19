from flask import Flask, request, jsonify, json
import requests,json,re
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
    title = soup.find_all('h2',{'itemprop':'name'})[0].text

    source = requests.get('https://animeschedule.net/').text
    soup = BeautifulSoup(source, "html.parser")

    weeks = soup.find_all('div',{'class':'timetable-column'})

    if status == "Ongoing":

        days = {
            'Monday' : 0,
            'Tuesday' : 1,
            'Wednesday' : 3,
            'Thursday' : 4,
            'Friday' : 5,
            'Saturday' : 6,
            'Sunday' : 7
        }
        for i in range(len(weeks)):
            if re.search(title, weeks[i].text, re.IGNORECASE) != None:
                airDay = days[weeks[i].attrs['class'][-1]]
                break

        return {
            'error' : False,
            'status' : status,
            'epstotal' : epstotal,
            'airDay' : airDay
        }
    else:
        return {
            'error' : False,
            'status' : status,
            'epstotal' : epstotal
        }

if __name__ == '__main__':
    app.run(threaded=True, port=5000)