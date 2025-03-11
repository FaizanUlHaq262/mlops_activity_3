import os
import time
from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Wait for backend to be ready
time.sleep(5)

# Database setup
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///budget.db')
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Define database models (must match backend models)
class Income(Base):
    __tablename__ = 'income'
    
    id = Column(Integer, primary_key=True)
    source = Column(String(100), nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(Date, nullable=False)

# Create tables
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Check if we already have data
if session.query(Income).count() == 0:
    print("Initializing database with sample data...")
    
    # Sample income
    today = datetime.now().date()
    income = [
        Income(source="Salary", amount=3000.00, date=today - timedelta(days=15))
    ]
    
    # Add to database
    session.add_all(income)
    session.commit()
    
    print("Sample data added successfully!")
else:
    print("Database already contains data. Skipping initialization.")

session.close()
print("Database initialization complete.") 