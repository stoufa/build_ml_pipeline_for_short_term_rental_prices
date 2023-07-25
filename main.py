import json

import tempfile
import os
import wandb
import hydra
from omegaconf import DictConfig
import mlflow

_steps = [
    "download",
    "basic_cleaning",
    "data_check",
    "data_split",
    "train_random_forest",
    # NOTE: We do not include this in the steps so it is not run by mistake.
    # You first need to promote a model export to "prod" before you can run this,
    # then you need to run this step explicitly
    #    "test_regression_model"
]


# This automatically reads in the configuration
@hydra.main(config_name='config')
def go(config: DictConfig):

    # Setup the wandb experiment. All runs will be grouped under this name
    os.environ["WANDB_PROJECT"] = config["main"]["project_name"]
    os.environ["WANDB_RUN_GROUP"] = config["main"]["experiment_name"]

    # You can get the path at the root of the MLflow project with this:
    root_path = hydra.utils.get_original_cwd()

    # Steps to execute
    steps_par = config['main']['steps']
    active_steps = steps_par.split(",") if steps_par != "all" else _steps
    print('[DEBUG]', active_steps)

    # Move to a temporary directory
    with tempfile.TemporaryDirectory() as tmp_dir:
        print('[DEBUG]', tmp_dir)

        if "download" in active_steps:
            # Download file and load in W&B
            print('[DEBUG]', os.path.join(root_path, "components", "get_data"))

            _ = mlflow.run(
                f"{config['main']['components_repository']}/get_data",
                # "get_data",
                # os.path.join(root_path, "components", "get_data"),
                "main",
                version='main',
                parameters={
                    "sample": config["etl"]["sample"],
                    "artifact_name": "sample.csv",
                    "artifact_type": "raw_data",
                    "artifact_description": "Raw file as downloaded"
                },
            )

        if "basic_cleaning" in active_steps:
            ##################
            # Implement here #
            ##################
            _ = mlflow.run(
                os.path.join(
                    root_path,
                    "src", "basic_cleaning"
                ),
                "main",
                parameters={
                    "input_artifact": "sample.csv:latest",
                    "output_artifact": "clean_sample.csv",
                    "output_type": "clean_sample",
                    "output_description": "Data with outliers and null values removed",
                    "min_price": config['etl']['min_price'],
                    "max_price": config['etl']['max_price']
                },
            )

        if "data_check" in active_steps:
            ##################
            # Implement here #
            ##################
            _ = mlflow.run(
                os.path.join(
                    root_path,
                    "src", "data_check"
                ),
                "main",
                parameters={
                    "csv": "clean_sample.csv:latest",
                    "ref": "clean_sample.csv:reference",
                    "kl_threshold": config["data_check"]["kl_threshold"],
                    "min_price": config["etl"]["min_price"],
                    "max_price": config["etl"]["max_price"]
                },
            )

        if "data_split" in active_steps:
            ##################
            # Implement here #
            ##################
            _ = mlflow.run(
                # when trying to access the step hosted in the remote GitHub repo, I get this error:
                # AttributeError: 'IterableList' object has no attribute 'origin/master'
                # Apparently, this is due to the change of the "master" branch to the "main" branch
                # since we don't have access to that repo, we'll be point to our local copy instead
                # f"{config['main']['components_repository']}/train_val_test_split",
                # https://github.com/gitpython-developers/GitPython/issues/910

                os.path.join(
                    root_path,
                    "components", "train_val_test_split"
                ),

                "main",
                parameters={
                    "input": "clean_sample.csv:latest",
                    "test_size": config['modeling']['test_size'],
                    "random_seed": config['modeling']['random_seed'],
                    "stratify_by": config['modeling']['stratify_by']
                },
            )

        if "train_random_forest" in active_steps:
            # NOTE: we need to serialize the random forest configuration into JSON
            rf_config = os.path.abspath("rf_config.json")
            with open(rf_config, "w+") as fp:
                # DO NOT TOUCH
                json.dump(
                    dict(config["modeling"]["random_forest"].items()), fp)

            # NOTE: use the rf_config we just created as the rf_config parameter for the train_random_forest
            # step

            ##################
            # Implement here #
            ##################

            _ = mlflow.run(
                os.path.join(
                    root_path,
                    "src", "train_random_forest"
                ),
                "main",
                parameters={
                    "trainval_artifact": "trainval_data.csv:latest",
                    "val_size": config["modeling"]["val_size"],
                    "random_seed": config["modeling"]["random_seed"],
                    "stratify_by": config["modeling"]["stratify_by"],
                    "rf_config": rf_config,
                    "max_tfidf_features": config["modeling"]["max_tfidf_features"],
                    # Use the name random_forest_export as output_artifact
                    "output_artifact": "random_forest_export"
                },
            )

        if "test_regression_model" in active_steps:

            ##################
            # Implement here #
            ##################

            _ = mlflow.run(
                os.path.join(
                    root_path,
                    "components", "test_regression_model"
                ),
                "main",
                parameters={
                    "mlflow_model": "random_forest_export:prod",
                    "test_dataset": "test_data.csv:latest",
                },
            )


if __name__ == "__main__":
    go()
