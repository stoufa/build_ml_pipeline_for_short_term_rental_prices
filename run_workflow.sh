# for a complete stack trace (in case of errors)
export HYDRA_FULL_ERROR=1

# to hide the warnings that appear in the data_check step
export PYTHONWARNINGS="ignore"

# Fix for the following error
# > TypeError: Descriptors cannot not be created directly.
# > If this call came from a _pb2.py file, your generated code is out of date and must be regenerated with protoc >= 3.19.0.
# > If you cannot immediately regenerate your protos, some other possible workarounds are:
# >  1. Downgrade the protobuf package to 3.20.x or lower.
# >  2. Set PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python (but this will use pure-Python parsing and will be much slower).
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION="python"

# mlflow run . -P steps=download
# mlflow run . -P steps=basic_cleaning
# mlflow run . -P steps=data_check
# mlflow run . -P steps=data_split
# mlflow run . -P steps=train_random_forest

# "Optimize hyperparameters" sub step of the "Initial Training" step
# try setting the parameter modeling.max_tfidf_features to 10, 15 and 30,
# and the modeling.random_forest.max_features to 0.1, 0.33, 0.5, 0.75, 1
# mlflow run . \
#   -P steps=train_random_forest \
#   -P hydra_options="modeling.max_tfidf_features=10,15,30 modeling.random_forest.max_features=0.1,0.33,0.5,0.75,1 -m"

# "Test" sub step of the "Initial Training" step
# note that this step require a manual intervention to chose a model and add the "prod" tag to it
mlflow run . -P steps=test_regression_model
