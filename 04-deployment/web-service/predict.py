# code for loading the model and scoring.

import pickle

from flask import Flask, request, jsonify

with open('lin_reg.bin', 'rb') as f_in:
    (dv, model) = pickle.load(f_in)

def prepare_features(ride):
    features = {}
    features['PUD_DO'] = '%s_%s' % (ride['PULocationID'], ride['DOLocationID'])
    features['trip_distance'] = ride['trip_distance']
    return features

def predict(features):
    X = dv.transform(features)
    preds = model.predict(X)
    return float(preds[0])

# create a flask application

app = Flask('duration-prediction')

# this decorator adds extra functionality to the function
@app.route('/predict', methods=['POST']) # This will turn our function into an endpoint 
def predict_endpoint(): # in flask functions dont get parameters so we need to give it using flask
    ride = request.get_json() # this allows to get the data

    features = prepare_features(ride)
    pred = predict(features)

    result = {
        'duration': pred
    }

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)