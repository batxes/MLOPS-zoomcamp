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
next, run the notebook:

to delete an experiment permanently: rm -rf mlruns/.trash/*

Downloading the artifact

```bash
export MLFLOW_TRACKING_URI="http://127.0.0.1:5000"
export MODEL_RUN_ID="6dd459b11b4e48dc862f4e1019d166f6"

mlflow artifacts download \
    --run-id ${MODEL_RUN_ID} \
    --artifact-path model \
    --dst-path .
```



### My Notes

