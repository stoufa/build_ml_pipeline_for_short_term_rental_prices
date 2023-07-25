#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import argparse
import logging
import wandb
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    ######################
    # YOUR CODE HERE     #
    ######################

    logger.info('Downloading the data from W&B ...')
    local_path = wandb.use_artifact("sample.csv:latest").file()
    df = pd.read_csv(local_path)

    logger.info('Cleaning raw data ...')
    # Drop outliers
    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()
    # Convert last_review to datetime
    df['last_review'] = pd.to_datetime(df['last_review'])

    # fix of the "test_proper_boundaries" test
    # drop rows in the dataset that are not in the proper geolocation
    idx = df['longitude'].between(-74.25, -73.50) & \
        df['latitude'].between(40.5, 41.2)
    df = df[idx].copy()

    logger.info('Exporting clean data as CSV ...')
    clean_data_file_name = 'clean_sample.csv'
    df.to_csv(clean_data_file_name, index=False)

    logger.info('Uploading clean data to W&B ...')
    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    artifact.add_file(clean_data_file_name)
    run.log_artifact(artifact)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")

    # All parameters should be of type str except min_price and max_price that should be float

    parser.add_argument(
        "--input_artifact",
        type=str,
        help="the input artifact",
        required=True
    )

    parser.add_argument(
        "--output_artifact",
        type=str,
        help="the name for the output artifact",
        required=True
    )

    parser.add_argument(
        "--output_type",
        type=str,
        help="the type for the output artifact",
        required=True
    )

    parser.add_argument(
        "--output_description",
        type=str,
        help="a description for the output artifact",
        required=True
    )

    parser.add_argument(
        "--min_price",
        type=float,
        help="the minimum price to consider",
        required=True
    )

    parser.add_argument(
        "--max_price",
        type=float,
        help="the maximum price to consider",
        required=True
    )

    args = parser.parse_args()

    go(args)
