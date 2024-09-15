from flask import Flask, request, redirect, url_for, render_template, session
from flask_session import Session
from datetime import datetime, timedelta
import os
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Verifică dacă directorul de date există și creează-l dacă nu
if not os.path.exists('data'):
    os.makedirs('data')

def get_expiry_time():
    if 'expiry_time' in session:
        return session['expiry_time']
    return None

@app.route('/')
def index():
    expiry_time = get_expiry_time()
    if expiry_time and datetime.now() > expiry_time:
        session.pop('expiry_time', None)
        return redirect(url_for('generate_link'))
    return render_template('index.html')

@app.route('/generate-link')
def generate_link():
    session['expiry_time'] = datetime.now() + timedelta(minutes=10)
    link = url_for('form', _external=True)
    return f"Link-ul generat: <a href='{link}'>Accesați formularul</a>"

@app.route('/form')
def form():
    expiry_time = get_expiry_time()
    if not expiry_time or datetime.now() > expiry_time:
        return "Link-ul a expirat. <a href='/'>Înapoi la pagină principală</a>"
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit_names():
    name = request.form['name']
    file_path = 'data/names.csv'

    # Verifică dacă fișierul CSV există și scrie headerul dacă este nou
    file_exists = os.path.isfile(file_path)
    with open(file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Name'])  # Header-ul fișierului CSV
        writer.writerow([name])

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
