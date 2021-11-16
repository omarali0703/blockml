import io
import sys
args=sys.args
run_type = "all"
project_name="untitled"
accepted_l1_commands = [
	"create",
	"run"
]
accepted_l2_commands = [
	"pre",
	"preprocess",
	"eval",
	"evaluate",
	"results",
	"generate_results",
	"blank",
	"tagging_flow"

]

mlflow_example_projects = "metadata/"

if args[0] not in accepted_l1_commands or args[1] not in accepted_l2_commands:
	sys.exit(f"command {arg[0]} {arg[1]}  does not exist."

if len(args) > 0:
	run_type=f"{args[1]}"
	if len(args) > 1 and run_type=="create":
		project_name=f"{args[0]}"
		create_project(project_name)
else:
	sys.exit("Please specify a project name")

def create_project(name=project_name,location=""):
	print("Creating new MLFlow project...")
	# Create folders here
	# ...
	pass

def __init__():
	pass

