## Getting the model for deployment from MLflow

* Take the code from the previous video
* Train another model, register with MLflow
* Put the model into a scikit-learn pipeline
* Model deployment with tracking server
* Model deployment without the tracking server

Starting the MLflow server with S3:

First we create a S3 bucket in AWS: https://eu-north-1.console.aws.amazon.com/s3/buckets?region=eu-north-1&bucketType=general&region=eu-north-1

and run:


```bash
pipenv shell
mlflow server --backend-store-uri=sqlite:///mlflow.db  --default-artifact- root=s3://mlflow-models-ibai/
```
next, run the notebook (not in codespaces!! important):

My run ID: 06e935a7b17943c4b9e95e9d012489d7

```bash
export MLFLOW_TRACKING_URI="http://127.0.0.1:5000"
export MODEL_RUN_ID="06e935a7b17943c4b9e95e9d012489d7"
```

Now we modify predict.py so that we download the model from the S3 bucket.
we run predict.py also outside codespaces.
and now we have already our server running.

we can test with test_with_flask.py
