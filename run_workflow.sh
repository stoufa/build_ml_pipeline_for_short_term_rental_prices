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
mlflow run . -P steps=data_check
