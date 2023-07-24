FROM continuumio/miniconda3

# packages in conda-forge work well together (unlike the ones of the default channel!)
# https://stackoverflow.com/questions/57779829/command-to-display-active-conda-channels
# https://stackoverflow.com/questions/54150169/how-update-remove-conda-forge-channel-from-anaconda
RUN conda config --add channels conda-forge

# setting up the environment manually (instead of using the given YAML file)
# install all dependencies from conda-forge, to make sure that the packages work well together
RUN conda install -c conda-forge mlflow -y
RUN conda install -c conda-forge ipython -y
RUN conda install -c conda-forge notebook -y
RUN conda install -c conda-forge jupyterlab -y
RUN conda install -c conda-forge cookiecutter -y
RUN conda install -c conda-forge hydra-core -y
RUN conda install -c conda-forge matplotlib -y
RUN conda install -c conda-forge pandas -y
RUN conda install -c conda-forge git -y
RUN conda install -c conda-forge pip -y
RUN conda install -c conda-forge wandb -y

# fix for the following error: Could not load conda plugin `conda-libmamba-solver`
# might not be needed! this error message appeared during the manual installation without disturbing it!
# https://stackoverflow.com/questions/75703897/after-installing-libmamba-solver-i-get-warning-libmamba-could-not-parse-state-f
# EDIT: tried it, it didn't solve the problem, the error message appears
# even after running this command!
# RUN conda clean --all

RUN apt-get update
RUN apt-get install nano
RUN apt-get install less

# spd-say is needed for the create_env.sh script
# https://askubuntu.com/questions/501910/how-to-text-to-speech-output-using-command-line
RUN apt-get install speech-dispatcher -y

COPY environment.yml .
COPY create_env.sh .
RUN bash create_env.sh --silent

RUN conda init bash
# to make the following "source" command work
# https://stackoverflow.com/questions/20635472/using-the-run-instruction-in-a-dockerfile-with-source-does-not-work
SHELL ["/bin/bash", "-c"]
RUN source /root/.bashrc
# even after fixing the "source" issue, I still can't run the following command, so, I'll be running it mannually
# RUN conda activate nyc_airbnb_dev

# activating the created conda environment
# https://stackoverflow.com/questions/55123637/activate-conda-environment-in-docker
RUN /bin/bash -c "source activate nyc_airbnb_dev"
# to fix the AttributeError: module 'numpy' has no attribute 'object'
RUN pip install numpy==1.23.4


WORKDIR /project

COPY . .

CMD [ "bash" ]
