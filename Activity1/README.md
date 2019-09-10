# Scopus dataset creator
## Language
The language chosen for the task was [Python](https://www.python.org/) given its characteristics which allowed us to 
interact easily with the libs needed to accomplish our task.

However, due to the limitation of deploying python, a single executable is not feasible.

## Installation and use
This project requires a python version >= 3.7, given the language features we use.
We also need some libraries, which are specified in the requirements.txt file, and we recommend installing them in a 
virtual environment using pip
```
pip install -r requirements.txt
``` 
Rename the `config.example.ini` to `config.ini`, and substitute the values required for the program, which includes an apikey for Elsevier


After that, you should run the file `api_downloader.py` as follows:
```
python api_downloader.py
```
Which will download most of the data and sometimes asking for clarifications in which university you are looking for

After that, use `dataset_generator.py` as follows:
```
python dataset_generator.py
```
Which in turn will create the dataset by default in the Data subdirectory
