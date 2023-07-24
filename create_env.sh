# note that I switched to Python 3.8.17 (using pyenv)
# https://realpython.com/intro-to-pyenv/#using-your-new-python
# EDIT: I had to REMOVE pyenv as it clashes with conda! This is the only solution that worked for me!

conda env create -f environment.yml -v
# conda env create -f environment.yml -vv

# conda env create -f environment.yml python=3.8 -v

# conda env create --help
#   -v, --verbose         Use once for info, twice for debug, three times for trace.

# conda create -n nyc_airbnb_dev python=3.8
# conda install mlflow=1.14.1 -c conda-forge

# remove conda environment
# conda env remove -n ENV_NAME

# we can't use spd-say in docker images!
# so we'll pass the --silent flag in Dockerfile
if [ $# -gt 0 ]; then
    # Argument is passed
    SILENT=1
else
    # No argument is passed
    SILENT=0
fi


# check the exit code
if [ $? -ne 0 ]; then
    echo "script failed with a non-zero exit code"
    if [ $SILENT -eq 0 ]; then
        # you'll hear this in case of error
        spd-say "script failed"
   fi
else
    echo "script executed successfully"
    if [ $SILENT -eq 0 ]; then
        # you'll hear this if everything went well
        spd-say "script completed successfully"
    fi
fi

