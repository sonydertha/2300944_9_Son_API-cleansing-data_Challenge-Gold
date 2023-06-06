"""
Utility function for intercationg with the database
including :
1. Connect to the database
2. Create table Kamus Alay & Abusive
3. Insert Result of data cleansing 
"""

import sqlite3

def create_connection():
    conn = sqlite3.connect('gold_challenge.db')
    return conn

def insert_dictionary_to_db(conn):
    