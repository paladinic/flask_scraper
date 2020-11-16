# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, request, Response
import requests
from bs4 import BeautifulSoup

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/results', methods=['GET','POST'])
def results():
    url_input = request.form.get("url_input")
    element_input = request.form.get("element_input")
    property_input = request.form.get("property_input")
    tables = scrape(url_input,element_input,property_input)
    l = len(tables)

    return render_template("results.html",tables = tables,url_input = url_input,element_input = element_input,property_input = property_input, l = l)

def scrape(url,element="",arg="",skip_no_arg=True):
    response = requests.get(url)
    page = response.text
    soup = BeautifulSoup(page,"html.parser")
    if (element == "") | (element == None):
        elements = soup.find_all("p")
    else:
        elements = soup.find_all(element)
    element_tables = []
    for e in elements:
        if (arg != "") & (arg != None):
            try:
                e = e[arg]
                element_tables.append(str(e))
            except KeyError:
                print("arg not found in element")
                if not(skip_no_arg):
                    element_tables.append(str(e))
        else:
            element_tables.append(str(e))
    return element_tables
