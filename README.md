# Multichain GUI Tool

A GUI (Graphical User Interface) for multichain platform so that anyone can easily use multichain functionalities without having the knowledge of or having to use cli(command-line interface).

## Installation of pre-requisites

1. multichain v1.0.6
1. Python3.6, Python3.6-dev
1. virtualenv

If you have all the pre-requisites installed, skip this step and go to next step

### Install Multichain v1.0.6

```sh
su
cd /tmp
wget https://www.multichain.com/download/multichain-1.0.6.tar.gz
tar -xvzf multichain-1.0.6.tar.gz
cd multichain-1.0.6
mv multichaind multichain-cli multichain-util /usr/local/bin
````

### Install Python3.6

```sh
sudo apt-get install python3.6 python3.6-dev
python3 --version
```

### Install virtualenv

```sh
sudo apt-get install virtualenv
virtualenv --version
```

## Project Setup

```sh
# go to project root after cloning the project
cd PATH_TO_PROJECT_ROOT

# create virtual environment with python3.6 as default python and activate it
virtualenv -p python3.6 .venv
source .venv/bin/activate

# install api dependecies
pip install -r api/requirements.txt

# run the start file
python start.py
```
