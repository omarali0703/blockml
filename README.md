# BlockML (Buggy-as-Hell)
1. Non-intrusive framework to run custom scripts in a clear and succinct order

Whilst some of the files are called MLFlow this isn't related to the actual MLFlow. The term is used literally as the ***flow*** of ML process defined and designed in this framework.

BlockML builder to create and edit ml flows in python. Run custom scripts using simple input/outputs 'blocks' defined in python



## Creating a New Project 🚀

> You can create either a blank project or a project with some blocks already pre-generated for specific machine learning flows e.g. tagging, supervised-learning etc.
>
### To create a new project: 🧠
>
> ```bash
> mlflow.py create [project] [project_type]
> ```
>
#### Example: 

> ##### Usage
> 
> ```bash
> mlflow.py create My_SVM_Classifier blank
> ```



### Adding Custom Blocks: 🧱

> All projects are different, machine learning flows are changing all the time, as such, feel free to delete or add custom blocks in the order of your choosing

#### Example:

> ##### Usage
> 
> ```bash
> mlflow.py add [project] [new_block_name]
> ```

### Adding Custom Sub-Blocks: 🧱

Sub-blocks allow your main-flow block's logic to have their own organised directory. Each subblock should have an \_\_init\_\_.py of its own to serve as the entry point. The rest of the sub-block's logic can be referenced separately in their own .py files or within the init file itself (either-way is fine).

#### Example sub-block File-Structure:

```
[project-name]
  ├── [block-1]
  |		├── __init__.py
  |		├── block-1-logic.py
  |		└── [sub-block-1]
  |		|		├── __init__.py
  | 	|		└── sub-block-1-logic.py
  ├── [block-2]
  |		├── __init__.py
  |		├── block-2-logic.py
  └── [block-3]
  |		├── block-3-logic.py
  |		├── [sub-block-1]
  |		|		├── __init__.py
  | 	|		└── sub-block-1-logic.py
  |		├── [sub-block-2]
  |		|		├── __init__.py
  | 	|		└── sub-block-2-logic.py
  |		└── __init__.py
	└── __init__.py
```



## Executing your project ⌛️

> You may run your project in one of two ways: `run-all` and `single-block` mode. Run-all will run the entire project block-by-block in the order specified in the `__init__.py` file. Single-block mode allows you to run a single block at a time to better debug your model step-by-step.
### Running the whole project
> ##### Usage
> 
> ```bash
> mlflow.py run [project-name]
> ```
### Running a single block

> ##### Usage
> 
> ```bash
> mlflow.py run [project-name] [block-name] [input-data-location]
> ```

Single block mode must have a location to either a directory of .json files, or a single.json file.

> ```python
>example_data = {
> file_name_1:[file-data-1],
> file_name_2:[file-data-2],
>  		...
>  file_name_n:[file-data-n]
>  }
>  ```
> 

### Block Settings

> Block settings can be specified via the command line when running in single-block mode or programmatically when running the entire flow.
>
> #### Example Settings Specification in Single-Block Mode
>
> ##### Usage
>
> ```
> mlflow.py run [project-name] [block-name] [input-data-location] [settings]
> ```
>
> 



## Flow Creation 🛠

> For more complex proceedures within your model, you should have a look the `flows.ini` file! Flows allow you to segment your model into standalone pieces that can be run independently to others. Consisting souly of a list of blocks, flows can be defined by specifying block orders, loops and input settings for each block. You can then run the flow in a far cleaner fashion in the command-line. Multiple flows for the same model can also be defined in this file. The order in which the blocks are specified in the flows.ini file will override the order specified in the __init__.py file for that project.
>
> ##### Example flows.ini File
>
> ```ini
> [example-flow]
> ; OVERRIDE for dependencies should this particular flow want/need its own set of dependencies that are
> ; separate from other flows (Preferable for neat and tidy house-keeping)
> DEPENDENCIES="flow_dependencies"
> 
> ; Specify the order that blocks are run (Not including any loops) using a csv-style format.
> BLOCKORDER = "block-1","block-2","block-3"
> 
> ; Specify the output file location for the results of the flow.
> OUTPUTLOCATION = "my-results.csv"
> ```
>
> 
>
> ##### Running the flows.ini file
>
> ```bash
> mlflow.py run-flow [project-name] [flow-name]
> ```
>
> ##### Usage
>
> ```bash
> mlflow.py run-flow my-project flow_1
> ```

