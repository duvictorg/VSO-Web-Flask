"""
Routes and views for the flask application.
"""

from datetime import datetime
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

@app.route('/weather')
def weather():
    return render_template(
        'weather.html',
        title='Weather Page',
    ) 