# Docs Conda Jupyter Lab
* Learning and experimenting with Conda package controller
* Apparently, it's easier to install certain packages as well on linux
  * i.e. nodejs
  * and sometimes more stable than brew
## V0 Steps
1. Install python3 / miniconda / anaconda
   * Mamba - same-same but much faster apparently
2. init conda env
3. Poetry


# Export Conda Env to yml
```bash
# https://anaconda.org/conda-forge/poetry
conda install -c "conda-forge/label/main" poetry
conda env export > .\old_env\environment.yml
conda env export --from-history > environment.yml
conda env export > .\old_env\environment_v1.yml
```


# Conda Notes From Tutorial
* there's also mamba
```bash
# https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html
conda create --name docs-conda-jupyter-lab
# defaults to ~/miniconda3\envs\docs-conda-jupyter-lab
# for project local... 
# conda create --prefix ./envs jupyterlab=3.2 matplotlib=3.5 numpy=1.21
# however, i'm guessing conda 

conda activate docs-conda-jupyter-lab

# list envs
conda env list
conda info --envs


# Add / Export to file
# creaets FROM from an env file
conda env create -f environment.yml # creates the env 



conda install --file requirements.txt

```

# Version Info
```bash
#https://docs.conda.io/projects/conda-build/en/stable/resources/package-spec.html
numpy 1.7.*
scipy ==0.14.2
```

# Other Package Managers
* also Poetry / pyproject.toml
* Poetry is like Yarn. Should Investigate

---
https://blog.jmswaney.com/poetry-a-yarn-like-package-manager-for-python

If you are familiar with the package.json in web-development, the pyproject.toml file is very similar. 
A package.json specifies package dependencies, development dependencies, and scripts for running tests and creating minified builds. 
Some rough analogies between Python and Javascript would be:

poetry = yarn / npm
pyproject.toml = package.json
poetry.lock = yarn.lock / package-lock.json
---

# Poetry Tutorial
```bash
# https://python-poetry.org/docs/basic-usage/
# pre-existing project like ours:
poetry init

poetry add pyyaml

poetry add pyyaml --dev
poetry add pyyaml -D

poetry remove pyyaml

# Wheel Creation
poetry build

# default is ther project name in snake case
# might need to change the default location
packages = [
    { include = "my_package" },
    { include = "extra_package/**/*.py" },
]

# .bash_completion support

```


# Jupyter Lab
```bash
jupyter lab

```