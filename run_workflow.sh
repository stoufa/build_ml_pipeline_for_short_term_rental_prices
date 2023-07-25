# for a complete stack trace (in case of errors)
export HYDRA_FULL_ERROR=1

# export PYTHONWARNINGS="ignore"
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION="python"

# mlflow run . -P steps=download
mlflow run . -P steps=basic_cleaning

