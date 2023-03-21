from flask import Flask, request, Response, jsonify
import json
import openai
import os
import random
app = Flask(__name__)

MAX_RETRIES = 10

def pickNlpColor(colorname):
    COLOR_FORMAT_SCHEMA ="""
    title: Color Formats
type: object
properties:
  hex:
    type: string
    pattern: "^#[a-fA-F\\d]{3,6}$"
  rgb:
    items:
      type: number
  hsl:
    items:
      type: number
    """

    CONTENT = "Give me the most likely rgb, hex, and hsl values for the phrase or word \" " + colorname  + " \" following the schema \"" + COLOR_FORMAT_SCHEMA + "\". Include no added commentary, explanation, confirmation or preamble in your response. Include only the json response"

    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": CONTENT},
        ]
    )
    
    return response

# def mockNlpColor(colorname):
#     return """{
#   "hex": "#008080",
#   "rgb": [0, 128, 128],
#   "hsl": [180, 100, 25]
# }"""

# def mockNlpColorNotValid(colorname):
#     return """
#   "hex": "#008080",
#   "rgb": [0, 128, 128],
#   "hsl": [180, 100, 25]
# }"""

# def mockNlpColorMaybeValid(colorname):
#     number = random.randrange(0, 10)
#     print(number)
#     if number < 1:
#         return mockNlpColor(colorname)
#     return mockNlpColorNotValid(colorname)

@app.route('/color/<colorname>', methods=["GET"])
def nlpColorPicker(colorname):
    color_name = request.view_args['colorname']

    key = os.getenv('OPENAI_KEY')
    openai.api_key = key

    response = None
    retries = 0
    while retries < MAX_RETRIES and response is None:
        try:
            # mock_response = json.loads(mockNlpColorMaybeValid(colorname))
            openai_response = pickNlpColor(colorname)
            response = json.loads(openai_response["choices"][0]["message"]["content"])
            
        except ValueError:
            response = None
        retries += 1
    if response is None:
        return "Malformed json response from neural network.", 500
    
    return jsonify(response), 200



if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)