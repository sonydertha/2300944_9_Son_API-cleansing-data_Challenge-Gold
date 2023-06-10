"""
Utility function for intercationg with the database
including :
1. Connect to the database
2. Create table Kamus Alay & Abusive
3. Insert Result of data cleansing 
"""

import pandas as pd
import sqlite3

def create_connection():
    conn = sqlite3.connect('gold_challenge.db')
    return conn

def insert_dictionary_to_db(conn):
    abusive_csv_data = "csv_data/abusive.csv"
    alay_csv_data = "csv_data/new_kamusalay.csv"

    # read csv file to dataframe
    print("reading csv file to dataframe...")
    df_abusive = pd.read_csv(abusive_csv_data, encoding='ISO-8859-1')
    df_alay = pd.read_csv(alay_csv_data, encoding='ISO-8859-1')

    # standardize column name
    print("standardize column name...")
    df_abusive.columns = ['word']
    df_alay.columns = ['alay_word', 'formal_word']

    # insert dataframe to database
    print("insert dataframe to database...")
    df_abusive.to_sql('abusive', conn, if_exists='replace', index=False)
    df_alay.to_sql('alay', conn, if_exists='replace', index=False)
    print("Inserting dataframe to database success!")

def insert_result_to_db(conn, raw_text, clean_text):
    # Insert result to database
    print("Inserting result to database...")
    df = pd.DataFrame({'raw_text': [raw_text], 'clean_text': [clean_text]})
    df.to_sql('cleansing_result', conn, if_exists='append', index=False)
    print("Inserting result to database success!")