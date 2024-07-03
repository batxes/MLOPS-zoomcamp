We will add unit test to this project

first install the libraries with and start a virtual environment: pipenv install
then, instal pytest: pipenv install --dev pytest (inside /code)

install python with vscode on the remote machine. "instal in SSH" if we do not have already
now configure python. ctrl + shift + p. -> python interpreter. We will chose the same as in pipenv --venv

(base) ibai@ibai-PC:~/work/mlops-zoomcamp/06-best-practices/code$ pipenv --venv
/home/ibai/.local/share/virtualenvs/code-R0NpjJgQ

add /home/ibai/.local/share/virtualenvs/code-R0NpjJgQ/bin/python and use that interpreter.

now we can uase the "Testing" icon in vscode in the leftmost panel.

if we write which pytest in the folder it gives as the base from conda. TO fix, do:

(if we get errors while installing in pipenv, just install setuptools in conda)
(if error persists, just install lower python version, not 3.12)

pipenv shell

which pytest

now we can configure it in vscode.
make a test file and inside mode_test.py and __init__.py

when running the tests, we got an error because of import lambda_function
that is because when running that function, we can see in the code of lambda_function.py that there are many htings being executed in the beggining, global variables, causing problems. Lets fix it. 
We can create an special class called model which will call all those variables first.

check what code we have in the files: model.py and lambda_function.py


now change Dockerfile so we also copy model.py

after that, build docker image

```bash
docker build -t stream-model-duration:v2 .
```

test with:

```bash
docker run -it --rm \
    -p 8080:8080 \
    -e PREDICTIONS_STREAM_NAME="ride_predictions" \
    -e RUN_ID="e1efc53e9bd149078b0c12aeaa6365df" \
    -e TEST_RUN="True" \
    -e AWS_DEFAULT_REGION="eu-west-1" \
    stream-model-duration:v2
```

Now we can check the test.

We will create another test for the decoding64. Put the logic in a function and add the test to model_test.py

we can also run the test through command line with pipenv run pytest tests/

we can also do a test for predict function. But here we do not want to download a model so we can create a mock Model.

Another test will be test_lambda_handler.

Finally we have the code about if not TEST_RUN: kinesis_client... in the model.py
IT is gonna be a lot of data that we have to pass to do the test but we can make it a little bit better. For that we will ad a callback to the model

Callbakcs are things that will be invocked after each prediction. We will add callback code and also create another model call KinesisCallback in the model.py


Video 6.2: Integration tests with docker-compose

We are going to tune test_docker.py into a proper test with asserts.

WHile adding code, at some point we want to compare dictionaries and say which keys are different. Install deepdiff

pipenv install --dev deepdiff

the idea is to run the model and also the tests.
we will create a bash script which first builds the docker image, then runs it and then we run the test with pipenv run python test_docker.py 
We will also crete a docker-compose.yaml to specify different images, path to volumnes, variables and other info.



   session 6.3

So far we covered unit test and integration tests. Unit tests are tests that use the test functions, with pytest.
Integration test we run the service inside docker and then we have pytho n script that we execute to see that what the model returns is ok.

We did not test though the part of the kinesis callback. For this we will use localstack (from github).
Localstack is a fully functional local AWS cloud stack.

We wil use localstack with docker-compose.
we add the code to the docker-compose.yaml and then execute with docker-compose up kinesis.

then, in a terminal:
aws --endpoint-url=http://localhost/4566 kinesis list-streams

there are no streams. We will create one:
aws --endpoint-url=http://localhost/4566 kinesis create-stream --stream-name ride_predictions --shard-count 1 

this will create the stream in localhost, not in AWS account.

we need to configure the code to access localstack. We will modify docker-compose.yaml for that. Modify also model.py with a function to create the client and run.sh

 session 6.4: good code quality: linting and formatting for good 






