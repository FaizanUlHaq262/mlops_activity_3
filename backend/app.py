import os
import json
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
CORS(app)

# Database setup
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///database/budget.db')
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Define database models
class Income(Base):
    __tablename__ = 'income'
    
    id = Column(Integer, primary_key=True)
    source = Column(String(100), nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'source': self.source,
            'amount': self.amount,
            'date': self.date.isoformat() if self.date else None
        }

# Create tables if they don't exist
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# Helper functions
def parse_date(date_str):
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return None

# API routes
@app.route('/api/income', methods=['GET'])
def get_income():
    session = Session()
    income_entries = session.query(Income).order_by(desc(Income.date)).all()
    session.close()
    return jsonify([entry.to_dict() for entry in income_entries])

@app.route('/api/income', methods=['POST'])
def add_income():
    data = request.json
    
    if not all(key in data for key in ['source', 'amount', 'date']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        amount = float(data['amount'])
    except ValueError:
        return jsonify({'error': 'Amount must be a number'}), 400
    
    date = parse_date(data['date'])
    if not date:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    
    session = Session()
    new_income = Income(
        source=data['source'],
        amount=amount,
        date=date
    )
    
    session.add(new_income)
    session.commit()
    result = new_income.to_dict()
    session.close()
    
    return jsonify(result), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True) 