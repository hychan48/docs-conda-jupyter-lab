#!/bin/bash
PROJECT_NAME=hello_world
# Install Python 3.10 / 3.11
# miniforge makes life easier
# https://github.com/conda-forge/miniforge
# https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh
# mamba comes with python 3.10
# wget -nc no-clobber. i.e dont download if exist
wget -nc "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
# bash Miniforge3-$(uname)-$(uname -m).sh
# auto accept default stuff
# Enter to continue
# 'enter' to licence
# yes
# default is ~/miniforge3
# i think this works:
bash Miniforge3-$(uname)-$(uname -m).sh <<END
enter
q
yes
q
no
END
~/miniforge3/bin/conda init bash
# conda config --set auto_activate_base false
# to disable afterwards
exec bash -l
# Using pip for now...
#conda create --name $PROJECT_DIR pip <<< y
conda create --name $PROJECT_NAME <<< y
conda activate $PROJECT_NAME
cd ~/git_repo/$PROJECT_NAME
#pip install -r requirements

# to remove env
# conda remove --name sqa-rasa-py --all
