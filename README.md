# data-engineering-nanodegree-data-warehouse
An imaginary music startup Sparkify has grown their user base and want to move their processes to the cloud.
As their new Data Engineer the task is to move their data which resides in log files on Amazon S3 
into Amazon Redshift staging tables.
the data will then be preprocessed and moved from staging tables into a dimensional model.

# Project Objective
The objective of this project is to apply acquired knowledge on an actual project.
Concepts include:

 - cloud data warehouse modeling specifically for Amazon Redshift
 - Moving data from S3 buckets into Redshift
 - Troubleshooting and debugging with cloud technology
 
# Project Structure

## sql_queries.py
This script contains all sql queries that will be executed on amazon Redshift.
Queries include:

 - Creating all staging tables
 - Creating data warehouse models
 - Copy data from S3 into staging tables
 - Move data from staging tables into data warehouse models

All queries are saved into python variables and regrouped into lists.

## create_tables.py
This script connects to the data warehouse using the `dwg.cfg` configuration file.
It then creates both staging and data warehouse models using queries present in `sql_queries.py`.

## etl.py
This script moves data from Amazon S3 into staging tables. It process the data handling null values and duplicate
inserts. It then moves the data into the data warehouse model.

## dwh.cfg
This file contains all configuration elements relevant to the data warehouse and log files location on S3.
Data warehouse configuration options and AWS credits are omitted for obvious security reasons.

## requirement.yml
This file contains all environment dependencies.
It has been generated using conda through the following command:
`conda env export > requirements.yml`

## spec-file.txt
A specification file can be used to build an identical conda environment either on the same machine or on a different
one. System specification used to generate the spec-file:
```
Distributor ID:	Ubuntu
Description:	Ubuntu 16.04.6 LTS
Release:	16.04
Codename:	xenial
```
The command line to create a spec list:

`conda list --explicit > spec-file.txt`

## .gitignore
Has ignoration rules to ignore some files from being mistakenly added to git.

## README.md
This file. Contains Project description, instruction to build environment and run scripts. 

# Creating environment

## Using requirements.yml
`conda env create -f requirements.yml -n myenv`

OR install on an existing one

`conda install -f requirements.yml`


# Using a spec file/list
`conda create --name myenv --file spec-file.txt`

OR install on an existing one

`conda install --name myenv --file spec-file.txt`

# Running scripts
To run the project successfully two scripts need to be run in the appropriate order:

1. `create_tables.py`: to create all tables schema in Amazon Redshift
2. `etl.py`: to move data from S3 into staging area and then into data warehouse models.

## Running create_tables.py
To run `create_tables.py` run the following in any terminal:

```
cd /project/directory/
conda activate myenv
python create_table.py
```

This changes into project directory, activate the conda environment to get access to the python interpreter,
then run the python script.

## Running etl.py
To run `etl.py` simply run the following:

```
cd /project/directory/
conda activate myenv
python etl.py
```  

running `etl.py` might take sometime since there are a lot of files in amazon S3.
