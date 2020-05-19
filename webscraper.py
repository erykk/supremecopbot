from bs4 import BeautifulSoup
import requests
from flask import Flask, escape, request, render_template

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html', title = "About")

@app.route("/",methods=['POST'])
@app.route("/index",methods=['POST'])
def scrape():
    url = request.form['url']
    bittaArr = []
    response = requests.get(url,timeout=5)
    content = BeautifulSoup(response.content,"html.parser")
    for bitta in content.findAll('p'):
    	bittaObj = {"text" : bitta.text,"classes" : bitta.get('class')}
    	bittaArr.append(bittaObj)
    return render_template('index.html', result = bittaArr)


if __name__ == '__main__':
	app.run(Debug=true)


