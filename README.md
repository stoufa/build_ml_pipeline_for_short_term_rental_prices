# Build an ML Pipeline for Short-Term Rental Prices in NYC

## 📝 TODO

> - [ ] improve this README file!
> - [ ] add screenshots (or even better animated GIF images)
> - [ ] replace comments scattered over files in clean documentation here!
> - [x] set up black as a pre-commit hook to make sure that your Python code is compliant with the PEP 8 style guide
> - [x] improve your EDA notebook (add headers and markdown comments: hypotheses, experiments, results, ...)
> - [x] fix the MLproject of the `data_cleaning` step

- [🔗 link to the W&B project](https://wandb.ai/m-sahli/nyc_airbnb)
- [🔗 link to the GitLab repository](https://gitlab.com/m.sahli/build_ml_pipeline_for_short_term_rental_prices)

> This is the capstone project of the "Building a Reproducible Model Workflow" Udacity course within the ["Machine Learning DevOps Engineer"](https://learn.udacity.com/nanodegrees/nd0821/) nanodegree. Project instructions can be found in the `NOTES.md` file.

## Project Overview

You are working for a property management company renting rooms and properties for short periods of time on various platforms. You need to estimate the typical price for a given property based on the price of similar properties. Your company receives new data in bulk every week. The model needs to be retrained with the same cadence, necessitating an end-to-end pipeline that can be reused.

In this project you will build such a pipeline.

![](images/building-prices.jpeg)

## Setup

I used a `Taskfile` to document all the tasks of this project in one YAML file, read more about Taskfiles [here](https://taskfile.dev/). As follows, the list of tasks included:

| Task                    | Description                                                                                            |
| ----------------------- | ------------------------------------------------------------------------------------------------------ |
| create_env              | create the nyc_airbnb_dev conda environment                                                            |
| remove_env              | remove the nyc_airbnb_dev conda environment                                                            |
| list_envs               | list all available conda environments                                                                  |
| create_mlflow_step      | create a new mlflow step under the src/ directory using the template in the cookie-mlflow-step/ folder |
| install_precommit_hooks | install the pre-commit git hooks defined in .pre-commit-config.yaml                                    |
| remove_mlflow_envs      | remove \*\*all\*\* the environments having the mlflow prefix                                           |
| download                | run the download step of the pipeline                                                                  |
| eda                     | run the EDA step of the pipeline                                                                       |
| data_clean              | run the data cleaning step of the pipeline                                                             |
| data_check              | run the data testing step of the pipeline                                                              |
| data_split              | run the data splitting step of the pipeline                                                            |
| train_model             | run the model training step of the pipeline                                                            |
| opt_hyper_params        | run the hyper-parameters optimization step of the pipeline                                             |
| prod_model_test         | run tests against the model we wish to deploy in the prod environment                                  |
| train_model_new_data    | trains the released models on new data                                                                 |

> - to execute a particular task, you need to run the following command: `task <task_name>`, e.g. `task create_env`
> - to list all tasks, run `task --list`
> - to get more details on a particular task, run `task --summary <task_name>`, e.g. `task --summary create_env`
