"""
Flask API Application
"""

from flask import Flask, jsonify, request
from flasgger import Swagger, swag_from, LazyString, LazyJSONEncoder
from db import (
    create_connection, 
    insert_dictionary_to_db,
    insert_result_to_db,
    show_cleansing_result,
    insert_upload_result_to_db 
)
from Cleansing_function import text_cleansing, cleansing_files

# Prevent sorting keys in JSON response
import flask
flask.json.provider.DefaultJSONProvider.sort_keys = False


# Function to initialize database
# def initialize_database():
# Create database connection
db_connection = create_connection()
# Insert dictionaries into the database
insert_dictionary_to_db(db_connection)
# Close the connection
db_connection.close()

# Run the database initialization function
# initialize_database()

#initialize flask aplication
app = Flask(__name__) 
# assign LaziJSONEncoder to app.json_encoder for swagger UI
app.json_encoder = LazyJSONEncoder

# create Swagger config & swagger template
swagger_template = {
    "info":{ 
        "title" : LazyString(lambda: "Text Cleansing API"),
        "version" : LazyString(lambda: "1.0.0"),
        "description" : LazyString(lambda: "Dokumentasi API untuk membersihkan text")
    },
    "host": LazyString (lambda: request.host)
}
swagger_config = {
    "headers" : [],
    "specs": [
        {
            "endpoint": 'docs',
            "route": '/docs.json',
        }
    ],
    "static_url_path" : "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}

# initialize swatter from swagger template & config
swagger = Swagger(app, template= swagger_template, config=swagger_config)

# home page
@app.route('/', methods = ['GET'])
@swag_from ('docs/home.yml')
def home ():
    welcome_msg = {
        "version":"1.0.0",
        "message":"Welcome to Flask API",
        "author":"Sony Dertha S."
    }
    return jsonify(welcome_msg)

# Show Cleansing result
@app.route('/show_cleansing_result', methods = ['GET'])
@swag_from('docs/show_cleansing_result.yml', methods = ['GET'])
def show_cleansing_result_api():
    db_connection = create_connection()
    cleansing_result = show_cleansing_result(db_connection)
    return jsonify(cleansing_result)

# Cleansing text using form
@app.route('/cleansing_form',methods = ['POST'])
@swag_from ('docs/cleansing_form.yml',methods = ['POST'])
def cleansing_form():
    #GET Text from input user
    raw_text = request.form["raw_text"]
    #Cleansing text
    clean_text = text_cleansing(raw_text)
    result_response = {"raw_text": raw_text, "clean_text": clean_text}
    # Insert result to database
    db_connection = create_connection()
    insert_result_to_db(db_connection, raw_text, clean_text)
    return jsonify(result_response)

# Cleansing text using csv upload
@app.route('/cleansing_upload',methods = ['POST'])
@swag_from ('docs/cleansing_upload.yml',methods = ['POST'])
def cleansing_upload():
    #GET Text from upload to database
    upload_file = request.files['upload_file']
    # Read csv file to dataframe then cleansing
    df_cleansing = cleansing_files(upload_file) 
    # upliad result to database
    db_connection = create_connection()
    insert_upload_result_to_db(db_connection, df_cleansing)
    print("Upload result to database success!")
    result_response = df_cleansing.T.to_dict()
    return jsonify(result_response)


if __name__ == '__main__':
    # Run the Flask application
    app.run()