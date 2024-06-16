##  Batch deployment

* Turn the notebook for training a model intoa  notebook for applying the model )so we do not train, just apply the model
    Run the notebook outside codespaces.
* turn the notebook into a scriot
    jupyter nbconvert --to script score.ipynb
* clean it and parametrize
    then run it also outside of codespaces. we need also to fix the aws addresses.