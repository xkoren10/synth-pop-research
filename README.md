# Synthetic population research
## Matej Koreň, 2025
This poject explores how different parameter settings influence large language models
ability to create and represent population in a variety of psychometrics tests.

To run this project, a `.env` file with the definition of API endpoints and keys is needed.

The dependencies as well as a virtual environment is supported by the `poetry` library.
Executing the scripts is recommended in this environment:

>$ potery run python [script name]

### Project structure
In `outputs/`, each model has its own folder, containing subfolders for each test with responses for each temperature.
The `pop_traits/` folder contains graphs for the best matching model settings for each test.

```
├── outputs
│   ├── graphs................ graphs of response variation by temperature for each person 
│   ├── plots................. boxplots of response variations for each question
│   ├── populations........... synthetic population personal profiles
│   ├── reports............... responses of model for each test type
│   └── statistics............ responses converted to dataframes
├── pop_traits................ plots of best matching model setting for baseline results
│   └── test_mapping.......... question to trait evaluation mapping for each test type
│
├── main.py................... main module of the application
├── poetry.lock............... poetry dependencies list
├── pyproject.toml............ project definition for poetry
├── README.md
└── other scripts............. (described below)
```


### Module description
#### main.py
Main script for generating populations and executing tests.
#### send_prompt.py
Defines the logic of sending prompts to a model and gathering the responses.
#### config.py
Contains the model and test type definition for each script that imports them.
#### prompts.py
Here are all the prompts for psychological tests and population generation (in a string format).
#### stats.py
This script creates dataframes from all collected results of a given test.
#### statistical_tests.py
Linear regression for temperature influence on response variation.
#### compare_models.py
T-test for model response variation comparison.
#### pop_graphs.py
Visualisation of population distribution.
#### pop_traits.py
Converting model responses to single traits and comparing them to a baseline result.
