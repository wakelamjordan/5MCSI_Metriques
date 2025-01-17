from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('hello.html')


@app.route("/contact/")
def contact():
    return render_template("contact.html")


@app.route("/tawarano/")
def meteo():
    response = urlopen(
        "https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx"
    )

    raw_content = response.read()

    json_content = json.loads(raw_content.decode("utf-8"))

    results = []

    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')

        temp_day_value = list_element.get('main', {}).get(
            'temp') - 273.15  # voir pourquoi çà permet de convertir en °c

        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)


@app.route("/rapport/")
def monGraphique():
    return render_template("graphique.html")


@app.route("/histogramme/")
def monHistogramme():
    return render_template("histogramme.html")


@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    minutes = date_object.minute
    return jsonify({'minutes': minutes})


@app.route("/commits/")
def commit():
    response = urlopen(
        "https://api.github.com/repos/wakelamjordan/5MCSI_Metriques/commits")

    raw_content = response.read()

    json_content = json.loads(raw_content.decode("utf-8"))

    results = []

    for list_element in json_content:
        value = list_element.get("commit", {}).get("author", {}).get("date")

        # temp_day_value = list_element.get('main', {}).get(
        #     'temp') - 273.15  # voir pourquoi çà permet de convertir en °c

        date_object = datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
        minutes = date_object.minute

        results.append({'date': minutes})

    return jsonify(results=results)


@app.route("/graphique_commits/")
def graphiqueCommit():
    return render_template("commits.html")


if __name__ == "__main__":
    app.run(debug=True)
