from flask import Flask
from flask import Flask, jsonify
from flask import request

from flask_swagger import swagger

import json

import analyzer.analyze

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/trip', methods=['POST'])
def trip():
    """
    Create a new user
    ---
    post:
      tags:
      - "Vehicle Trip Analyzer"
      summary: "analyze a vehicle trip"
      description: "this endpoints gets a list of data points from a vehicle. the whole list represents a trip from one location to another with several stops to refuel or just to eat some cookies."
      operationId: "analyze"
      consumes:
        - "application/json"
      produces:
        - "application/json"
      parameters:
        - in: "body"
          name: "body"
          description: "vehicle data that needs to be analyzed"
          required: true
          schema:
            $ref: "#/definitions/VehiclePush"
      responses:
        200:
            description: "returns analyzed vehicle data"
            schema:
            $ref: "#/definitions/VehiclePushAnalysis"
        401:
            description: "Unauthorized"
        403:
            description: "Forbidden"
        405:
            description: "Invalid input"
      security:
      - BasicAuth: []
"""
#    import pdb;pdb.set_trace()

    data = request.json
    
    return jsonify(analyzer.analyze.analyze(data))

@app.route("/spec")
def spec():
    return jsonify(swagger(app))
