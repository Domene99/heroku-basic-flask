from flask import Flask, request, Response, jsonify
import json
import openai
import os
import random
from Color import *
from utils import *
app = Flask(__name__)

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