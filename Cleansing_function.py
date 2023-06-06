"""
Function untuk membersihkan text
"""

import re

def text_cleansing(text):
    #bersihkan selain tanda baca 
    clean_text = re.sub(r'[^a-zA-Z0-9\s]', '', text)

    # yg lain
    clean_text = clean_text.lower()

    return clean_text