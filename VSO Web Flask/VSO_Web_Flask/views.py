"""
Routes and views for the flask application.
"""

import requests
from markupsafe import escape
from flask import render_template
from VSO_Web_Flask import app

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