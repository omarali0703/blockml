# MLFlow
1. Non-intrusive framework to run custom scripts in a clear and succinct order

ML flow builder to create and edit ml flows in python. Run custom scripts using simple input/outputs 'blocks' defined in python



## Creating a New Project 🚀

> You can create either a blank project or a project with some blocks already pre-generated for specific machine learning flows e.g. tagging, supervised-learning etc.
>
### To create a new project:
>
> ```bash
> mlflow.py create [project] [project_type]
> ```
>
#### Example: 

>
> ```bash
> mlflow.py create My_SVM_Classifier blank
> ```



### Adding Custom Block:

> All projects are different, machine learning flows are changing all the time, as such, feel free to delete or add custom blocks in the order of your choosing

#### Example:

> ```bash
> mlflow.py add [project] [new_block_name]
> ```



## Executing your project 

> You may run your project in one of two ways: `run-all` and `single-block` mode. Run-all will run the entire project block-by-block in the order specified in the `__init__.py` file. Single-block mode allows you to run a single block at a time to better debug your model step-by-step.
### Running the whole project
> ```bash
> mlflow.py run [project-name]
> ```
### Running a single block
> ```bash
> mlflow.py run [project-name] [block-name] [input-data-location]
> ```

Single block mode must have a location to either a directory of .json files, or a single .json file.

> ```python
>example_data = {
> file_name_1:[file-data-1],
> file_name_2:[file-data-2],
>  		...
>  file_name_n:[file-data-n]
>  }
>  ```
> 
> 
