"""
Function untuk membersihkan text
"""

import re
import pandas as pd
from db import get_abusive_data, create_connection

def text_cleansing(text):
    # Bersihkan selain tanda baca 
    clean_text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    # lowercase text
    clean_text = clean_text.lower()
    # clean abusive
    conn = create_connection ()
    df_abusive = get_abusive_data (conn)
    abusive_words = df_abusive ['word'].tolist()
    for word in abusive_words:
        asterisks = '*' * len(word)
        clean_text = clean_text.replace(word, asterisks)

    # Clean alay words
    replacement_words = pd.read_sql('SELECT * FROM alay',conn)
    replacement_dict = dict(zip(replacement_words['alay_word'], replacement_words['formal_word']))
    words = clean_text.split()
    replaced_words = [replacement_dict.get(word, word) for word in words]
    clean_text = ' '.join(replaced_words)

    return clean_text

def cleansing_files (file_upload):
     # Read csv file upload, jika error dengan metode biasa, gunakan encoding
    try:
        df_upload = pd.read_csv(file_upload)
    except:
        file_upload.seek(0)  # Move the file pointer to the beginning
        df_upload = pd.read_csv(file_upload, encoding='ISO-8859-1')
    print("Read dataframe from Upload success!")
    # Ambil kolom pertama saja
    df_upload = pd.DataFrame(df_upload.iloc[:,0])
    #rename kolom menjadi "raw_text"
    df_upload.columns = ["raw_text"]
    #bersihkan text menggunakan fungsi text_cleansing
    #simpan di kolom "clean_text"
    df_upload["clean_text"] = df_upload["raw_text"].apply(text_cleansing)
    print("Cleansing text success!")
    return df_upload
