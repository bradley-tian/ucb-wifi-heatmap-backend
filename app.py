

from flask import Flask, jsonify, request
from flask_cors import CORS
from google.cloud import firestore
import json

app = Flask(__name__)
cors = CORS(app)
db = firestore.Client(project='ucb-m-app')

# Retrieve building data from the json file included in this directory.
# Note: please maintain consistency between building names between the json file and the database documents. 
f = open('buildings.json')
buildings = json.load(f)

with open('buildings.json') as b:
    buildings = json.load(b)

@app.route("/send-input", methods=['POST'])
def sendInput():
    report = json.loads(request.get_data(as_text=True))
    db.collection(u'heatmap-backend').add(report)
    return jsonify(message="SUCCESS")

@app.route("/get-inputs", methods=['GET'])
def getInputs():
    users_ref = db.collection(u'heatmap-backend')
    metrics = {building: 0 for building in buildings['Buildings']}
    bReports = users_ref.where(u"location", u'!=', '').stream()

    for report in bReports:
       metrics[report.to_dict()['location']] += 1
    
    return json.dumps(metrics)

if __name__ == '__main__':
    app.run(debug=True)


