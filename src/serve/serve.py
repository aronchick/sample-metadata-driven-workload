from mlspeclib import MLSchema, MLObject
from random import randint, random, randrange
from pathlib import Path
import datetime
import uuid

# from interpret.blackbox import PartialDependence, MorrisSensitivity

from unittest.mock import MagicMock

# This file has the following variables:
#         workflow_object = an MLObject of the current workflow
#         input_object = an MLObject of the current input to this step
#         execution_object = an MLObject of the current execution to this step
#         step_name = string of the name of this step.
#         parameters.GITHUB_RUN_ID = a UUID of this run (provided by Github)
#
# Additionally, GitHub provides a number of variables as environement variables including:
#
#     CI	                Always set to true.
#     HOME	                The path to the GitHub home directory used to store user data. For example, /github/home.
#     GITHUB_WORKFLOW	    The name of the workflow.
#     GITHUB_RUN_ID	        A unique number for each run within a repository. This number does not change if you re-run the workflow run.
#     GITHUB_RUN_NUMBER	    A unique number for each run of a particular workflow in a repository. This number begins at 1 for the workflow's first run,
#                           and increments with each new run. This number does not change if you re-run the workflow run.
#     GITHUB_ACTION	        The unique identifier (id) of the action.
#     GITHUB_ACTIONS	    Always set to true when GitHub Actions is running the workflow. You can use this variable to differentiate when tests are
#                           being run locally or by GitHub Actions.
#     GITHUB_ACTOR	        The name of the person or app that initiated the workflow. For example, octocat.
#     GITHUB_REPOSITORY	    The owner and repository name. For example, octocat/Hello-World.
#     GITHUB_EVENT_NAME	    The name of the webhook event that triggered the workflow.
#     GITHUB_EVENT_PATH	    The path of the file with the complete webhook event payload. For example, /github/workflow/event.json.
#     GITHUB_WORKSPACE	    The GitHub workspace directory path. The workspace directory contains a subdirectory with a copy of your repository if your
#                           workflow uses the actions/checkout action. If you don't use the actions/checkout action, the directory will be empty.
#                           For example, /home/runner/work/my-repo-name/my-repo-name.
#     GITHUB_SHA	        The commit SHA that triggered the workflow. For example, ffac537e6cbbf934b08745a378932722df287a53.
#     GITHUB_REF	        The branch or tag ref that triggered the workflow. For example, refs/heads/feature-branch-1. If neither a branch or tag is
#                           available for the event type, the variable will not exist.
#     GITHUB_HEAD_REF	    Only set for forked repositories. The branch of the head repository.
#     GITHUB_BASE_REF	    Only set for forked repositories. The branch of the base repository.
#
# You can read more about these here - https://help.github.com/en/actions/configuring-and-managing-workflows/using-environment-variables

# The code below is for mocking to make the rest of the code look legit
subprocess = MagicMock()
popen_return = MagicMock()
popen_return.stdout.read.return_value = "Kubectl job result would go here."
subprocess.Popen.return_value = popen_return
timer = MagicMock()

# Below is for testing - comment out when live
# input_object = MagicMock()
# execution_object = MagicMock()
# results_ml_object = MagicMock()
# result_ml_object_schema_type = 'feature_engineering_result'
# result_ml_object_schema_version = '2.1.0'

results_ml_object.set_type(
    schema_type=result_ml_object_schema_type,  # noqa
    schema_version=result_ml_object_schema_version,  # noqa
)

results_ml_object = MLObject()
results_ml_object.set_type("2.2.0", "serve_result")

action_name = "deploy_model"
model_package = "contoso_bork_model:1.3.1"

# Below is how you would execute a Kubeflow Serving deployment
external_command = f"kubectl run pipeline {action_name} --container={model_package}"
result_of_deploy_to_kf_serving_command = subprocess.Popen(
    external_command, shell=True, stdout=subprocess.PIPE
).stdout.read()

results_ml_object.extended_properties = {}
results_ml_object.extended_properties[
    "result_of_start_kf_deploy_command"
] = result_of_deploy_to_kf_serving_command
model_service_name = subprocess.Popen(
    external_command, shell=True, stdout=subprocess.PIPE
).stdout.job_id()

return_dict = {}
finished_time = None
while finished_time is None:
    external_command = f"kubectl get svc f{model_service_name}"
    results_ml_object.extended_properties["deploy_finished"] = subprocess.Popen(
        external_command, shell=True, stdout=subprocess.PIPE
    ).stdout.read()
    if results_ml_object.extended_properties["deploy_finished"] is not None:
        finished_time = datetime.datetime.now()

#
# Swap out above if we want to deploy to AML
#

# # Deploying model
# print("::debug::Deploying model")
# try:
#     # Default service name
#     repository_name = os.environ.get("GITHUB_REPOSITORY").split("/")[-1]
#     branch_name = os.environ.get("GITHUB_REF").split("/")[-1]
#     default_service_name = f"{repository_name}-{branch_name}".lower().replace("_", "-")[:32]

#     service = Model.deploy(
#         workspace=ws,
#         name=parameters.get("name", default_service_name),
#         models=[model],
#         inference_config=inference_config,
#         deployment_config=deployment_config,
#         deployment_target=deployment_target,
#         overwrite=True
#     )
#     service.wait_for_deployment(show_output=True)
# except WebserviceException as exception:
#     print(f"::error::Model deployment failed with exception: {exception}")
#     service_logs = service.get_logs()
#     raise AMLDeploymentException(f"Model deployment failedlogs: {service_logs} \nexception: {exception}")

# Mocked up (you'd get this from the result of the deployment)
results_ml_object.serving_endpoint = "https://bork.models.svc.contoso.internal"
results_ml_object.serving_port = "8888"

finished_time = datetime.datetime.now()
results_ml_object.extended_properties = {"finished_time": finished_time}

# Execution metrics
results_ml_object.execution_profile.system_memory_utilization = random()
results_ml_object.execution_profile.network_traffic_in_bytes = randint(7e9, 9e10)
results_ml_object.execution_profile.gpu_temperature = randint(70, 130)
results_ml_object.execution_profile.disk_io_utilization = random()
results_ml_object.execution_profile.gpu_percent_of_time_accessing_memory = random()
results_ml_object.execution_profile.cpu_utilization = random()
results_ml_object.execution_profile.gpu_utilization = random()
results_ml_object.execution_profile.gpu_memory_allocation = random()
