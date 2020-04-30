import os
try:
    from omegaconf import DictConfig, ListConfig
    import mlflow
    import hydra
except:
    raise Exception('Please make sure to install "pip install mlflow hydra-core".')
import logging


class ExperimentRecorder():
    """MLflow/Hydra simple wrapper for making easy to record experiment details.
    Thanks to https://ymym3412.hatenablog.com/entry/2020/02/09/034644
    """

    def __init__(self, experiment_name, run_name=None,
                 uri='http://0.0.0.0:5000', username='mlflow_user', password='mlflow_pwd'):
        os.environ['MLFLOW_TRACKING_URI']      = uri
        os.environ['MLFLOW_TRACKING_USERNAME'] = username
        os.environ['MLFLOW_TRACKING_PASSWORD'] = password

        mlflow.set_experiment(experiment_name)
        mlflow.start_run(run_name=run_name)

        logging.basicConfig(level=logging.WARN)
    
    def get_things(self):
        org_dir = hydra.utils.get_original_cwd()
        run_dir = os.path.abspath('.')
        return org_dir, run_dir, logging.getLogger(__name__)

    def log_all_params(self, root_param):
        self._explore_recursive('', root_param)

    def _explore_recursive(self, parent_name, element):
        if isinstance(element, DictConfig):
            for k, v in element.items():
                if isinstance(v, DictConfig) or isinstance(v, ListConfig):
                    self._explore_recursive(f'{parent_name}{k}.', v)
                else:
                    mlflow.log_param(f'{parent_name}{k}', v)
        elif isinstance(element, ListConfig):
            for i, v in enumerate(element):
                mlflow.log_param(f'{parent_name}{i}', v)
        else:
            print('ignored to log param:', element)

    # def log_param(self, key, value): # --> simply, `mlflow.log_param(...)`
    #     mlflow.log_param(key, value)

    # def log_metric(self, key, value, step=None):
    #     mlflow.log_metric(key, value, step=step)

    # def log_artifact(self, local_path):
    #     mlflow.log_artifact(local_path)

    def end_run(self):
        mlflow.end_run()
