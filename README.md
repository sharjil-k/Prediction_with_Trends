[![Build Status](https://travis-ci.com/shk305/Home_Display_Project.svg?branch=master)](https://travis-ci.com/shk305/Home_Display_Project)

[![Maintainability](https://api.codeclimate.com/v1/badges/ed08d3b62bf4028200d3/maintainability)](https://codeclimate.com/github/shk305/Home_Display_Project/maintainability)


# Home Display



## Objective

This project is intended to provide useful and customizable information on a Home Display System.
The information is based on the users personal data such as finacial accounts (Banks, Credit Cards, Stock Brokerage Accounts) as well as Fitness related tracking data such as number of steps in the last few days, fitness goals, weight history etc.
The idea is that this app can aggregate all the relevant information and display it in a meaningful format. It is also capable of alerting the user based on events such as the users stocks loosing value, or the user achieving some fitness goal.  

![Alt text](images/Stock_Account_Changed.JPG?raw="Title1")

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Pre-Requisites](#pre-requisites)
- [Initial setup](#initial-setup)
- [Basic Commands](#basic-commands)
- [High level Architecture](#high-level-architecture)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Pre-Requisites
This is an app mainly designed and built for personal use. But it can be easily modified to support more 
general scenarios. But for now there are two basic apps/accounts a person has to be using to use this app effectively.

* [Personal Capital](https://www.personalcapital.com/): An app/website that helps people aggregate personal financial data.

* [Dakboard](https://dakboard.com/site/): A home display system that displays information like weather, time, pictures on a display screen
that someone can put on a wall.

## Initial setup
To set up the project the user has to set up the environment and install all libraries required by typing:

Make sure this environment variable is set:
DATABASE_URL=sqlite:///data/db.sqlite
```bash
#In Windows :
set DATABASE_URL=sqlite:///data/db.sqlite

#In Linux:
setenv  DATABASE_URL sqlite:///data/db.sqlite
```


Then cd into the directory of the repo and run the following commands:
```bash
# In repo:
pip install pipenv 
pipenv install --dev

python manage.py migrate         # Creates the databases and migrates built in Django user authentication table
python manage.py createsuperuser # user:pass = admin:admin if you'd like
```
From then on, the user can run the commands provided by the app or run the django server to investigate
or debug the app. 

## Basic Commands 
In case the user does not have a Personal Capital or Dakboard account, the app can still be executed with some fake data to run through its functions.

There are two main commands that should be executed to retrieve the data from the websites (or get fake data if in test mode)
and push the data to the Dakboard server so it displays on all the boards.
 
```bash
# In repo:
pipenv run python manage.py retrieve_financial_data 
pipenv run python manage.py display_financial_data
```
The first command above will authenticate the user into his personal capital account and retrieve relevant data using the API
and store it in a local database.

The second command will display the data on the Dakboard by pushing data onto its interface.
 
 
If the user does not have a personal capital account running with the -t option will load fake data.
```bash
pipenv run python manage.py retrieve_financial_data -t
```
Or if the user wants to debug or inspect the databases involved. The user can also run the django server
```bash
pipenv run python manage.py runserver
```
Then the API data can be found at: 
http://127.0.0.1:8000/home_display/api/financial/



## High level Architecture

![Alt text](images/Architecture.JPG?raw="Title2")
