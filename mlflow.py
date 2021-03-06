import io
import json
import sys
import os
import shutil
import mlflow_projects
import configparser
args = sys.argv
run_type = "all"
project_name = "mlflowproject"
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
accepted_l1_commands = [
    "create",
    "run",
    "add",
    "run-flow"
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

# input_data_location is the location of the input data for a single block when running in single block mode.
def run_project(project_to_run='untitled', flow_to_run=None, block_to_run_from=None, input_data_location=None, block_settings=None):
    print(project_to_run, flow_to_run, block_to_run_from, input_data_location)
    try:  # Will always cancel the entire model if there's an error. We need to micro-manage issues that may occur. We can skip some fails and continue the model etc.
        project_module = __import__('mlflow_projects.' +
                                    str(project_to_run), fromlist=[''])
        blocks_in_flow = project_module.FLOW_ORDER
        dependencies_location = project_module.DEPENDENCIES
        if block_to_run_from != None and block_to_run_from in blocks_in_flow:
            if input_data_location == None:
                sys.exit("Please specify a location for input data ")
            input_data_dir = f"mlflow_projects/{project_to_run}/{dependencies_location}/{input_data_location}"
            is_dir = os.path.isdir(input_data_dir)
            if is_dir:
                batch_input_data = {}
                list_path = os.listdir(input_data_dir)
                for file in list_path:
                    input_data_file_name = file.split('.')[0]
                    input_data_file_data = open(
                        os.path.join(input_data_dir, file), 'r')
                    input_data_contents = input_data_file_data.read()
                    batch_input_data[file] = input_data_contents
                    input_data_file_data.close()
                input_data = batch_input_data
            else:
                input_data = open(input_data_dir, "r")
                input_data_file_name = input_data_dir.split(
                    '/')[-1].split('.')[0]
                input_file_data = input_data.read()
                input_data.close()
                input_data = {input_data_file_name: input_file_data}
                # Array with single element so batch and single input_data's can be processed the same way.
            
            current_block = __import__(
                'mlflow_projects.' + str(project_to_run) + '.' + block_to_run_from, fromlist=[''])
            block_settings = json.loads(block_settings)
            block_settings['root'] = f"mlflow_projects/{project_to_run}/{dependencies_location}"
            block_settings['input_data_location'] = input_data_dir
            print(
                f"{bcolors.OKCYAN}Running {block_to_run_from} in single-block mode...\nSettings: {block_settings}")
            output_data, loop_breaker = current_block.start(
                input_data, block_settings)
            print(f"{bcolors.OKGREEN} {output_data}")
        elif block_to_run_from == None and flow_to_run == None:
            input_data = None
            output_data = None
            for block in blocks_in_flow:
                print(f"{bcolors.OKCYAN} Block, {block} has started...")
                current_block = __import__(
                    'mlflow_projects.' + str(project_to_run) + '.' + block, fromlist=[''])
                output_data, loop_breaker = current_block.start(
                    input_data=input_data)
                if output_data == None:
                    sys.exit(
                        f"please make sure that block, {block} has output data returned.")
                print(f"{bcolors.OKCYAN} Block, {block} has finished.")
                input_data = output_data  # Set the next inputdata to the last output
            print(f"{bcolors.OKCYAN} Model has finished successfully.")
        elif flow_to_run != None and input_data_location == None:
            print(f"{bcolors.OKCYAN} Flow, {flow_to_run} has started...")
            input_data_dir = f"mlflow_projects/{project_to_run}/flows.ini"
            flows_config = configparser.ConfigParser()
            flows_config.read(input_data_dir)
            flows = flows_config.sections()
            print(f"{bcolors.OKCYAN} Flows {flows} initatiated.")
            if flow_to_run not in flows:
                sys.exit(
                    f"{bcolors.FAIL}Flow to run is not specified in flows.ini")
            print(flows_config[flow_to_run])
            dependencies_location = flows_config[flow_to_run][
                'DEPENDENCIES'] if "DEPENDENCIES" in flows_config[flow_to_run] else dependencies_location
            block_order = flows_config[flow_to_run]['BLOCKORDER'].split(',')
            loopable = True if flows_config[flow_to_run]['LOOP'] in (
                'on', 'yes', 'true') else False
            input_data = None
            output_data = None
            # TODO support for iterable models. (Quite important)
            iterable = False
            for block in block_order:
                print(f"{bcolors.OKCYAN} Block, {block} has started...")
                current_block = __import__(
                    'mlflow_projects.' + str(project_to_run) + '.' + block, fromlist=[''])
                if block_settings:
                    if not type (block_settings) is dict:
                        block_settings = json.loads(block_settings)
                    block_settings['root'] = f"mlflow_projects/{project_to_run}/{dependencies_location}"
                    block_settings['input_data_location'] = input_data_dir
                else:
                    block_settings={}

                output_data, loop_breaker = current_block.start(
                    input_data, block_settings)
                print(
                    f"{bcolors.OKGREEN} Data in flow...\nLast inputted data: {type(input_data)}\nLast outputted data: {type(output_data)},")
                input_data = output_data
                if output_data == None:
                    sys.exit(
                        f"{bcolors.WARNING}please make sure that block, {block} has output data returned.")
                print(f"{bcolors.OKCYAN} Block, {block} has finished.")
            print(f"{bcolors.OKCYAN} Flow, {flow_to_run} has finished successfully.")
            script = "osascript -e 'tell application \"Messages\" to send \"FuzzySeg has finished running.\" to buddy \"07948171108\"'"
            os.system(script)
        else:
            sys.exit("Block doesn't exist.")
    except ModuleNotFoundError as error:
        print(f"{bcolors.FAIL}{error}")
        sys.exit(
            f"{bcolors.FAIL}Project {project_to_run} Has thrown errors. These are most likely documented above.")


def create_project(name=project_name, location="", project_type="blank"):
    print("Creating new MLFlow project...")
    if location == "":
        sys.exit(f'{bcolors.FAIL}Please specify a location for the project.')
    if project_type == "" or project_type == None:
        project_type = "blank"
    path = os.path.join(location, name)
    print(f"{bcolors.OKCYAN}Cloning blank project template...")
    try:
        shutil.copytree(f"metadata/example_project", path)
        for block in PROJECT_STRUCTURES[project_type]:
            shutil.copytree(f"metadata/example_block", f"{path}/{block}")
    except OSError as error:
        sys.exit(error)
    print(
        f"{bcolors.OKCYAN}Project, {name} created at {location}. Visit the github source to get started!")


def create_new_block(project_name=None, name='unamed_block', ):
    if project_name == None:
        sys.exit('Please specify a project to create a new block for.')
    try:
        shutil.copytree(f"metadata/example_block",
                        f"mlflow_projects/{project_name}/{name}")
    except OSError as error:
        sys.exit(error)
    print(f"{bcolors.OKCYAN}Successfully create new block. Make sure to add the block name into the flow order to make sure it is run.")


mlflow_example_projects = "metadata/"
print(args)
if len(args) > 1:
    run_type = f"{args[1]}"
    if len(args) > 2:
        project_name = f"{args[2]}"
        location = f"mlflow_projects"
        project_type = "blank"
        if run_type == "create" and len(args) > 3:
            project_type = args[3]
            if project_type not in PROJECT_STRUCTURES:
                sys.exit(
                    f"Project type: {project_type} is not a valid project type to generate")
            create_project(project_name, location, project_type)
        elif run_type == "add":
            new_block_name = args[3]
            create_new_block(project_name, new_block_name)
        elif run_type == "run":
            project_name = f"{args[2]}"
            if len(args) > 3:
                block_to_run_from = args[3]
                input_data_location = args[4]
                settings = None
                if len(args) > 5:
                    settings = args[5]
                run_project(project_name, None, block_to_run_from,
                            input_data_location, settings)
            else:
                run_project(project_name)
            print(f'{bcolors.OKCYAN}Project finished running.')
        elif run_type == "run-flow":
            project_name = f"{args[2]}"
            if len(args) > 3:
                flow_name = args[3]
                settings = None
                if len(args) > 5:
                    settings = args[5]
                run_project(project_name, flow_name, None, None, settings)
            else:
                sys.exit(
                    f'{bcolors.WARNING}Please specify a flow to run on this project.')
    elif args[2] not in accepted_l1_commands or args[2] not in accepted_l2_commands:
        sys.exit(
            f"{bcolors.WARNING}command {args[1]} {args[2]}  does not exist.")
else:
    sys.exit(f"{bcolors.WARNING}Please specify a project name")
