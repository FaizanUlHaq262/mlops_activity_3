import os
import requests
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'faizans-webapp-secret-key'

# Backend API URL
BACKEND_URL = os.environ.get('BACKEND_URL', 'http://localhost:5001')

@app.route('/')
def index():
    # Get income entries
    try:
        income_response = requests.get(f"{BACKEND_URL}/api/income")
        income = income_response.json()
    except requests.RequestException as e:
        print(f"Error connecting to backend: {e}")
        income = []
    
    return render_template('index.html', income=income)

@app.route('/add_income', methods=['POST'])
def add_income():
    income_data = {
        'source': request.form.get('source'),
        'amount': request.form.get('amount'),
        'date': request.form.get('date')
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/api/income", json=income_data)
        if response.status_code == 201:
            flash('Income added successfully!', 'success')
        else:
            flash('Error adding income. Please try again.', 'danger')
    except requests.RequestException:
        flash('Could not connect to backend service.', 'danger')
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 