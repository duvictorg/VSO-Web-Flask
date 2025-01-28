import requests
import csv

# URL de l'API JSONPlaceholder pour récupérer les tâches
URL = "https://jsonplaceholder.typicode.com/todos"



def save_to_csv(todos):
    with open('todos.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["userId", "id", "title", "completed"])
        for todo in todos:
            writer.writerow([todo['userId'], todo['id'], todo['title'], todo['completed']])