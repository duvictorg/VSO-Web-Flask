"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, jsonify
import requests
from markupsafe import escape
from flask import render_template
from VSO_Web_Flask import app
from .Tp.Exercice1.placeholder import *



@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
    )

@app.route('/weather/<Ville>')
def weather():
    URL = 'https://api.openweathermap.org/data/2.5/weather?q=' + str(Ville) + '&limit=1&appid=1446ca8783c1ae2790262ec9c1510b9c'
    return render_template(
        'weather.html',
        title='Weather Page',
    ) 

@app.route('/fetch_todos', methods=['GET'])
def fetch_todos():
    """
    Cette route récupère les tâches depuis l'API JSONPlaceholder et les stocke dans une liste.
    """
    response = requests.get(URL)
    todos = response.json()
    save_to_csv(todos)
    return jsonify(todos)