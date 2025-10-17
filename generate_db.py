#!/usr/bin/env python3
"""
SQLite3 Database Generator Script
Creates a new SQLite database in the root directory with sample tables
"""

import sqlite3
import os
from datetime import datetime

def create_database():
   
    db_path = os.path.join(os.getcwd(), 'db.sqlite3')
  
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Removed existing database: {db_path}")
  
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Create sample tables
        print("Creating database tables...")
        
        # Users table
        cursor.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Food items table
        cursor.execute('''
            CREATE TABLE food_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL,
                calories_per_100g REAL NOT NULL,
                protein_per_100g REAL DEFAULT 0,
                carbs_per_100g REAL DEFAULT 0,
                fat_per_100g REAL DEFAULT 0,
                category VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # User meals table
        cursor.execute('''
            CREATE TABLE user_meals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                meal_name VARCHAR(255) NOT NULL,
                food_item_id INTEGER NOT NULL,
                quantity_grams REAL NOT NULL,
                meal_type VARCHAR(20) CHECK(meal_type IN ('breakfast', 'lunch', 'dinner', 'snack')),
                meal_date DATE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (food_item_id) REFERENCES food_items (id)
            )
        ''')
        
        # User profiles table
        cursor.execute('''
            CREATE TABLE user_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE NOT NULL,
                age INTEGER,
                gender VARCHAR(10),
                height_cm REAL,
                weight_kg REAL,
                activity_level VARCHAR(20),
                goal VARCHAR(50),
                daily_calorie_target INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        conn.commit()
       
    except Exception as e:
        print(f"Error creating database: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":

    create_database()
