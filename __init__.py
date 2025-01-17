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
    return "<h2>Ma page contact</h2>"


@app.route("/tawano/")
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


if __name__ == "__main__":
    app.run(debug=True)
