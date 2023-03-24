export PROJECT_NAME=hello_world
yes | conda create --name $PROJECT_NAME
conda activate $PROJECT_NAME
mkdir ~/git_repo/$PROJECT_NAME
cd ~/git_repo/$PROJECT_NAME

# conda remove --name $PROJECT_NAME --all
# conda update -n base -c conda-forge conda