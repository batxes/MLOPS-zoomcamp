## Comments

First thing to do is to check the exact version of scikit-learn that we used to create the model with pickle in the first module. (01-intro/models/lin_reg.bin)

For that we can do: 

```bash
pip freeze | grep scikit-learn
```

this gives me a weird output so I used the next command:

```bash
pip list --format=freeze > requirements.txt
```

we get 1.0.2

now we want a virtual environment. Write:
```bash
pipenv install scikit-learn==1.0.2 flask --python=3.9
```
and then:

```bash
pipenv shell
```
the prompt is very long, we can make it short with:
```bash
PS1="> "
```

now we write predict.py.

we can test it using python test.py

After modifying to wrap with flask, we can run it with python predict.py
Now we can add requests. For thtat we will modify test.py (I kept the original and created test_with_flask.py)

SO now we put our model in a flask application, we can interact with the flask application, we can send information about our ride and get prediction acout the ride. WHen launching the server we got:

```bash
python predict.py
 * Serving Flask app 'duration-prediction'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
```
To fix this waning we need to use a production server like Gunicorn, and use it instead of flask. Flask is only used for development purposes. 

So we start gunicorn:

```bash
gunicorn --bind=0.0.0.0:9696 predict:app
```
in localhost, go to the predict module and look for the app variable.

gunicorn is not installed in the environment. For that I will run:

```bash
pipenv install gunicorn
```

test again running:
```bash
python test_with_flask.py
```

the request library is installed in the (base) environment, and if we go to our environment with pipenv shell, requests library is not installed.
We want to have everything self contained so that we can use it as a module when predicting. We could install requests in the Pipfile, but we are only using it for development (as you can see predict.py doe snot import requests). For that we can install only in development

```bash
pipenv install --dev requests
```

Finally we want to package the app into a docker container
For taht, create a Dockerfile

in the docker file we added many things. We want the python image but slim version so it is smaller. We also upgrade pip so we can always have the latest libraries like xgboost. Install pipenv and then stablish the working directory in /app. We copy the PIPfiles there and then we want to install them, but with pipenv install it already creates another environment and in docker we are already isolated so we dont really need another environment. We can do taht adding --system
Then copy model and python code, expose 9696 so this port is open in the container and then run gunicorn

Finally build it and run it.

```bash
docker build -t ride-duration-prediction-service:v1 .
```

```bash
docker run -it --rm -p 9696:9696  ride-duration-prediction-service:v1
```


## Starting with web service mlflow

install mlflow in the environment with

```bash
pipenv install mlflow
```

run the remote server in AWS from Alexey (data talksclub)

```bash
mlflow server \
    --backend-store-uri=sqlite:///mlflow.db \
    --default-artifact-root=s3://mlflow-models-alexey/
```

I got: ModuleNotFoundError: No module named 'boto3'

install boto3 also with pipenv