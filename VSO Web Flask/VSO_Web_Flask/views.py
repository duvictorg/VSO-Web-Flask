"""
Routes and views for the flask application.
"""

from flask import render_template, jsonify, request
import requests
from markupsafe import escape
from VSO_Web_Flask import app
from .Tp.Exercice1.placeholder import *
from .user import UserModel



@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    user1 = UserModel()
    print(user1.get_role('Martin.P'))
    print(user1.get_role('Martin.P2'))
    return render_template(
        'index.html',
        title='Home Page',
    )

@app.route('/weather', methods = ['GET'])
def weather():
    ville = request.args.get('ville', default = 'Paris', type = str)
    api_weather = 'https://api.openweathermap.org/data/2.5/weather?q=' + ville + '&limit=1&appid=1446ca8783c1ae2790262ec9c1510b9c'
    return render_template(
        'weather.html',
        title='Weather Page',
        meteo_ville = requests.get(api_weather).json()
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

@app.route('/main')
def main():
    """Renders the main page."""
    return render_template(
        'main.html',
        title='Main Page',
    )