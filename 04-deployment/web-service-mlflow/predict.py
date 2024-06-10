# code for loading the model and scoring.

import pickle

import mlflow
from mlflow.tracking import MlflowClient

from flask import Flask, request, jsonify

RUN_ID = 'b4d3bca8aa8e46a6b8257fe4541b1136'
MLFLOW_TRACKING_URI = 'http://127.0.0.1:5000'

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
client = MlflowClient(tracking_uri=MLFLOW_TRACKING_URI)
path = client.download_artifacts(run_id=RUN_ID, path='dict_vectorizer.bin')

print (f"downloading the dict vectorizer to {path}")

with open(path, 'rb') as f_out:
    dv = pickle.load(f_out)

logged_model = f'runs:/{RUN_ID}/model'

# Load model as a PyFuncModel.
model = mlflow.pyfunc.load_model(logged_model)


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