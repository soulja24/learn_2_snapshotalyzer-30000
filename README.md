# learn_2_snapshotalyzer-30000
Demo learning project 2 to manage AWS EC2 instance snapshots


## About
This project is a deo, and uses boto3 to manage AW ECS2 instance snapshots

## Configuring
shotty uses the config file created by AWS cli e.g.

`aws configure --profile shotty`

## Running

`pipenv run "python shotty/shotty.py <command> <--project=PROJECT>"`

*command* is list, start, or stop
*project* is optional
