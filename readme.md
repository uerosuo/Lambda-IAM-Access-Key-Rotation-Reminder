# to install a python package
pip install <package name>

pip install boto3

# create python virtual environmnet 

python -m venv <virtual env name>

-> python3 -m venv .venv

source venv/bin/activate

# install AWS CLI

For macOS/Linux:

aws --version

macOS Installation:

Using Homebrew:

brew update
brew install awscli

For Ubuntu/Debian:

sudo apt update
sudo apt install awscli

# Configure AWS CLI (After Installation)

aws configure

You'll need to provide:

AWS Access Key ID

AWS Secret Access Key

Default region name

Default output format

# Verify Full Functionality

aws sts get-caller-identity

