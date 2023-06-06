"""
Flask API Application
"""

from flask import Flask, jsonify, request
from flasgger import Swagger, swag_from, LazyString, LazyJSONEncoder
from Cleansing_function import text_cleansing

# Prevent sorting keys in JSON response
import flask
flask.json.provider.DefaultJSONProvider.sort_keys = False

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

# Cleansing text using form
@app.route('/cleansing_form',methods = ['POST'])
@swag_from ('docs/cleansing_form.yml')
def celansing_form():
    #GET Text from input user
    raw_text = request.form["raw_text"]
    #Cleansing text
    clean_text = text_cleansing(raw_text)
    result_response = {"raw_text": raw_text, "clean_text": clean_text}
    return jsonify(result_response)

if __name__ == '__main__':
    app.run()