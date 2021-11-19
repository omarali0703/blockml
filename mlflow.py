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

PROJECT_STRUCTURES = {
    "blank": ['preprocess', 'training', 'run', 'results'],
    "tagging": ['preprocess', 'tagging', 'training', 'run', 'results']
}


def run_project(project_to_run='untitled', block_to_run_from=None):
    try:
        project_module = __import__('mlflow_projects.' +
                                    str(project_to_run), fromlist=[''])
        blocks_in_flow = project_module.FLOW_ORDER
        if block_to_run_from not None and block_to_run_from in blocks_in_flow:
            current_block = __import__(
                'mlflow_projects.' + str(project_to_run) + '.' + block_to_run_from, fromlist=[''])
            current_block.start()
        elif block_to_run_from == None:
            input_data = None
            output_data = None
            for block in blocks_in_flow:
                current_block = __import__(
                    'mlflow_projects.' + str(project_to_run) + '.' + block, fromlist=[''])
                output_data = current_block.start(input_data)
                if output_data == None:
                    sys.exit(f"please make sure that block, {block} has output data returned.")
                input_data = output_data # Set the next inputdata to the last output
        else:
            sys.exit("Block doesn't exist.")
            
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
        shutil.copytree(f"metadata/example_project", path)

        for block in PROJECT_STRUCTURES[project_type]:
            shutil.copytree(f"metadata/example_block", f"{path}/{block}")

    except OSError as error:
        sys.exit(error)

    print(
        f"Project, {name} created at {location}. Visit the github source to get started!")


def create_new_block(project_name=None, name='unamed_block', ):
    if project_name == None:
        sys.exit('Please specify a project to create a new block for.')
    try:
        shutil.copytree(f"metadata/example_block",
                        f"mlflow_projects/{project_name}/{name}")
    except OSError as error:
        sys.exit(error)
    print ("Successfully create new block. Make sure to add the block name into the flow order to make sure it is run.")

mlflow_example_projects = "metadata/"
print(args)
if len(args) > 1:
    run_type = f"{args[1]}"
    if len(args) > 2:
        project_name = f"{args[2]}"
        location = f"mlflow_projects"
        project_type = "blank"
        if run_type == "create":
            if len(args) > 3:
                project_type = args[3]
                if project_type not in PROJECT_STRUCTURES:
                    sys.exit(
                        f"Project type: {project_type} is not a valid project type to generate")
            create_project(project_name, location, project_type)
        if run_type == "add":
            new_block_name = args[3]
            create_new_block(project_name, new_block_name)
        elif run_type == "run":
            project_name = f"{args[2]}"

            if len(args) > 3:
                block_to_run_from = args[3]
                run_project(project_name, block_to_run_from)
            else:
                run_project(project_name)
            print('Project finished running.')
    elif args[2] not in accepted_l1_commands or args[2] not in accepted_l2_commands:
        sys.exit(f"command {args[1]} {args[2]}  does not exist.")

else:
    sys.exit("Please specify a project name")
