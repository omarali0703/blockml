import io
import sys
import os
import shutil
import mlflow_projects
args = sys.argv
run_type = "all"
project_name = "mlflowproject"
accepted_l1_commands = [
    "create",
    "run",

    "add"
]
accepted_l2_commands = [
    "pre",
    "preprocess",
    "eval",
    "evaluate",
    "results",
    "generate_results",
    "blank",
    "tagging_flow",

    "block"

]


def run_project(project_to_run='untitled'):
    try:
        project_module = __import__('mlflow_projects.' +
                                    str(project_to_run), fromlist=[''])

        starting_block = project_module.STARTING_BLOCK
        starting_block = __import__('mlflow_projects.' +
                                    str(project_to_run) + '.' + starting_block, fromlist=[''])
        starting_block.start()
    except ModuleNotFoundError as error:
        print(error)
        sys.exit(
            f"Project {project_to_run} not found. Please run 'mlflow.py create {project_to_run}' to create it.")


def create_project(name=project_name, location="", project_type="blank"):
    print("Creating new MLFlow project...")
    if location == "":
        sys.exit('Please specify a location for the project.')
    if project_type == "" or project_type == None:
        project_type = "blank"

    path = os.path.join(location, name)
    print("Cloning blank project template...")
    try:
        shutil.copytree(f"metadata/example_project_{project_type}", path)
    except OSError as error:
        sys.exit(error)

    print(
        f"Project, {name} created at {location}. Visit the github source to get started!")


mlflow_example_projects = "metadata/"
print(args)
if len(args) > 1:
    run_type = f"{args[1]}"
    if len(args) > 2:
        project_name = f"{args[2]}"

        if run_type == "create":
            location = f"mlflow_projects"
            create_project(project_name, location, "blank")

        elif run_type == "run":
            project_name = f"{args[2]}"
            run_project(project_name)

    elif args[2] not in accepted_l1_commands or args[2] not in accepted_l2_commands:
        sys.exit(f"command {args[1]} {args[2]}  does not exist.")

else:
    sys.exit("Please specify a project name")
