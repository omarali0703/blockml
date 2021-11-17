import io,sys,os,shutil
args=sys.argv
run_type = "all"
project_name="mlflowproject"
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



def create_project(name=project_name,location="", project_type="blank"):
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

	print(f"Project, {name} created at {location}. Visit the github source to get started!")

mlflow_example_projects = "metadata/"
print (args)
if len(args) > 1:
	run_type=f"{args[1]}"
	if len(args) > 2 and run_type=="create":
		project_name=f"{args[2]}"
		location = f"mlflow_projects"
		create_project(project_name, location, "blank")
	elif args[2] not in accepted_l1_commands or args[2] not in accepted_l2_commands:
		sys.exit(f"command {args[1]} {args[2]}  does not exist.")

else:
	sys.exit("Please specify a project name")