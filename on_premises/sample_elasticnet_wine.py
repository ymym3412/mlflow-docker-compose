"""
Sample based on the original mlflow/examples/sklearn_elasticnet_wine/train.py,
edited for explaining how to work with things.

URL: https://github.com/mlflow/mlflow/blob/master/examples/sklearn_elasticnet_wine/train.py
"""

import os
import warnings
import sys

import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet

from experiment_recorder import *
import mlflow.sklearn


warnings.filterwarnings("ignore")
np.random.seed(40)


def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2


def train(cwd, logger, in_alpha, in_l1_ratio):
    """Almost the same with the original example"""

    # Read the wine-quality csv file from the URL
    csv_url =\
        'http://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv'
    try:
        data = pd.read_csv(csv_url, sep=';')
    except Exception as e:
        logger.exception(
            "Unable to download training & test CSV, check your internet connection. Error: %s", e)

    # Split the data into training and test sets. (0.75, 0.25) split.
    train, test = train_test_split(data)

    # The predicted column is "quality" which is a scalar from [3, 9]
    train_x = train.drop(["quality"], axis=1)
    test_x = test.drop(["quality"], axis=1)
    train_y = train[["quality"]]
    test_y = test[["quality"]]

    # Set default values if no alpha is provided
    if float(in_alpha) is None:
        alpha = 0.5
    else:
        alpha = float(in_alpha)

    # Set default values if no l1_ratio is provided
    if float(in_l1_ratio) is None:
        l1_ratio = 0.5
    else:
        l1_ratio = float(in_l1_ratio)

    # Execute ElasticNet
    lr = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=42)
    lr.fit(train_x, train_y)

    # Evaluate Metrics
    predicted_qualities = lr.predict(test_x)
    (rmse, mae, r2) = eval_metrics(test_y, predicted_qualities)

    # Print out metrics
    logger.info("Elasticnet model (alpha=%f, l1_ratio=%f):" % (alpha, l1_ratio))
    logger.info("  RMSE: %s" % rmse)
    logger.info("  MAE: %s" % mae)
    logger.info("  R2: %s" % r2)

    return lr, rmse, mae, r2


@hydra.main(config_path='sample/config.yaml')
def main(cfg: DictConfig) -> None:
    """Main part of this sample."""

    ### 1. This set environment variables, starts a run and gets logger.
    recorder = ExperimentRecorder('sample_elasticnet_wine',
        run_name=f'alpha={cfg.alpha},l1={cfg.l1_ratio}')
    org_dir, run_dir, logger = recorder.get_things()  # Logging settings are all done by Hydra.
    logger.info(f'cwd was {org_dir}...')              # Note that Hydra changes cwd.
    logger.info(f'running cwd is {run_dir}...')       # 

    # 2. Do your job: this trains a model.
    lr, rmse, mae, r2 = train(org_dir, logger, cfg.alpha, cfg.l1_ratio)

    # 3. Record all you want to leave: parameters, metrics, and model to MLflow.
    recorder.log_all_params(cfg)    # To record all parameters, this is usuful.
    mlflow.log_metric("rmse", rmse) # To record each metric or parameter, use mlflow api.
    mlflow.log_metric("r2", r2)
    mlflow.log_metric("mae", mae)

    mlflow.sklearn.log_model(lr, "model")

    # Hydra's artifacts.
    mlflow.log_artifact('.hydra/config.yaml')
    mlflow.log_artifact('.hydra/hydra.yaml')
    mlflow.log_artifact('.hydra/overrides.yaml')
    mlflow.log_artifact('sample_elasticnet_wine.log')

    # 4. Let's finish.
    recorder.end_run()


if __name__ == "__main__":
    main() 
