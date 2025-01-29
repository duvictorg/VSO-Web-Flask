# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 12:02:32 2025

@author: eljde
"""

import sqlite3

# Connexion à la base de données (créera books.db si elle n'existe pas)
conn = sqlite3.connect('books.db')
cursor = conn.cursor()

# Création de la table books
cursor.execute('''
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    fsentence TEXT,
    published TEXT
)
''')

# Données à insérer
books = [
    {'id': 0, 'title': 'A Fire Upon the Deep', 'author': 'Vernor Vinge',
     'fsentence': 'The coldsleep itself was dreamless.', 'published': '1992'},
    {'id': 1, 'title': 'The Ones Who Walk Away From Omelas', 'author': 'Ursula K. Le Guin',
     'fsentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 2, 'title': 'Dhalgren', 'author': 'Samuel R. Delany',
     'fsentence': 'to wound the autumnal city.', 'published': '1975'}
]

# Insertion des données
for book in books:
    cursor.execute('''
    INSERT OR REPLACE INTO books (id, title, author, fsentence, published)
    VALUES (:id, :title, :author, :fsentence, :published)
    ''', book)

# Sauvegarde des modifications et fermeture de la connexion
conn.commit()
conn.close()

print("La base de données 'books.db' a été créée avec succès.")
