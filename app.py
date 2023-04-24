from flask import Flask, request, Response, jsonify
import json
import openai
import os
import pdfplumber as pp
import mindsdb_sdk as mdb
import pandas as pd
import os
from Color import *
app = Flask(__name__)


MDB_EMAIL=os.getenv('mdb')
MDB_PWD=os.getenv('mdb-pass')
MODEL_NAME=os.getenv('mdb-model')


correct_schema = {
  "hex": "#000000",
  "rgb": [0, 0, 0],
  "hsl": [0, 0, 0]
}

def verifyResponse(response):
    result = True
    if response is None:
        return False
    for key, value in correct_schema.items():
        if key not in response:
            result = False
        if type(value) != type(response[key]):
            result = False
    return result

def color_pick(text):
    server=mdb.connect(login=MDB_EMAIL,password=MDB_PWD)
    model=server.get_project('mindsdb')
    query = model.query(f'select * from color_test_3 WHERE colorname = \'{text}\'')
    response = query.fetch()
    return response['color'][0]


MAX_RETRIES = 10
    

@app.route('/palette/<hexcolor>', methods=["GET"])
def palette(hexcolor):
    hex_color = request.view_args['hexcolor']
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    color = Color([r,g,b],"","")
    complementary = complementaryColor(color)
    triad = triadicColor(color)
    split = splitComplementaryColor(color)
    tetradic = tetradicColor(color)
    analogous = analogousColor(color)
    monochromatic = monochromaticColor(color)
    result = {
        "color": hexcolor,
        "complementary": complementary,
        "triad": triad,
        "split": split,
        "tetradic": tetradic,
        "analogous": analogous,
        "monochromatic": monochromatic
        }
    return jsonify(result), 200

@app.route('/color/<colorname>', methods=["GET"])
def nlpColorPicker(colorname):
    color_name = request.view_args['colorname']

    key = os.getenv('OPENAI_KEY')
    openai.api_key = key

    response = None
    retries = 0
    while retries < MAX_RETRIES and response is None:
        try:
            openai_response = color_pick(colorname)
            response = json.loads(openai_response)
            
        except ValueError:
            response = None
        retries += 1
    if not verifyResponse(response):
        return "Malformed json response from neural network.", 500
    
    return jsonify(response), 200



if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)