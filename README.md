[![Build Status](https://travis-ci.com/shk305/Prediction_with_Trends.svg?branch=master)](https://travis-ci.com/shk305/Prediction_with_Trends)

[![Maintainability](https://api.codeclimate.com/v1/badges/85ad543a13938bc969ba/maintainability)](https://codeclimate.com/github/shk305/Prediction_with_Trends/maintainability)

# Forecasting with Internet Trends



## Objective

This project aims to provide a framework that will allow a user to improve their forecast on time series data using 
internet trends. The ultimate goal of this is to completely automate the process of adding different internet trends 
information so that the user is provided with a final model that incorporates beneficial internet trends data without 
the user having to look for it explicitly. The final output of the project would be a model that forecasts the future
as shown in the plot below. 

![Alt text](images/output_data.JPG?raw="Title1")

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Pre-Requisites](#pre-requisites)
- [Initial setup](#initial-setup)
- [Basic Commands](#basic-commands)
- [High level Architecture](#high-level-architecture)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Pre-Requisites
To run on a basic dataset the app loads a dataset from Quandl. The user will need to create a free account at Quandl(ww.quandl.com
) and provide the API Key. 
 
For example an environment variable like this:

QUANDL_API_KEY = '29hyErz2TzC5oZFLCFke' 

The commands to set this is also described in the "Initial setup" section.


## Initial setup
To set up the project the user has to set up the environment and install all libraries required by typing:

Then cd into the directory of the repo and run the following commands:
```bash
# In repo:
pip install pipenv 
pipenv install --dev
```

The app uses some basic dataset from QUANDL and also needs to have the database location specified by some environment
variables.
Make sure this environment variable is set:
DATABASE_URL=sqlite:///data/db.sqlite
```bash
#In Windows :
set DATABASE_URL=sqlite:///data/db.sqlite
set QUANDL_API_KEY='29hyErz2TzC5oZFLCFke' # This is an example, your key will be different

#In Linux:
setenv  DATABASE_URL sqlite:///data/db.sqlite
setenv QUANDL_API_KEY '29hyErz2TzC5oZFLCFke' # This is an example, your key will be different
```

Then we need to create the initial database and the user accounts.

Then cd into the directory of the repo and run the following 
```bash
python manage.py migrate         # Creates the databases and migrates built in Django user authentication table
python manage.py createsuperuser # user:pass = admin:admin if you'd like
```
From then on, the user can run the commands described in the basic commands to run forecasts. 

## Basic Commands 

The following commands will run a basic run on a QUANDL dataset.
```bash
#In repo
python manage.py get_data      # Will fetch the data to run a forecast
python manage.py model_predict # Will model the data and output a plot with the forecast
```

The first command will fetch a dataset from QUANDL and load it into the Django Database.
It will load and display this dataset.
![Alt text](images/input_data.JPG?raw="Title2")

The second command will run a prediction model and display a plot of the provided data as well as the 
prediction from the model..
 
```
Or if the user wants to debug or inspect the databases involved. The user can also run the django server
```bash
pipenv run python manage.py runserver
```
Then the API data can be found at: 
http://127.0.0.1:8000/predictwithtrends/api/modelingdata/



## High level Architecture

![Alt text](images/Architecture.JPG?raw="Title3")
