# Job Central

The project's goal is to get several informations from JobBoards like Indeed or Monster. The app will refresh its data everyday at 9 AM.

Main target : [Indeed (FR)](https://www.indeed.fr/)

We're retrieving the essential information :
* Title
* Link
* City (City name + region/state/country)
* Job type and status
* **BONUS:** we'll be looking at required technological skills suited for the job and list them up

### Requirements

Need Firefox installed, then the most recent version of GeckoDriver, as a PATH variable. On the long term, geckDriver is much more reliable than Chrome's driver due to less frequent updates.

* [Download Firefox](https://www.mozilla.org/fr/firefox/new/)
* [Download GeckoDriver](https://github.com/mozilla/geckodriver/releases)

Python 3.8.x is also needed on your system. Load the `requirements.txt` file in a separate environment (conda, venv, etc...) and launch

```shell
pip install -r requirements.txt
```

### Launch test

To start the database manager, follow these instructions

```shell
python db-update/jobscraping/jobscraping.py 
python db-update/model/clean_database.py 
python db-update/model/tfidf.py
```

For the app, launch `app.py` as if it was a regular Flask app :

```shell
#On Linux: shell
$ export FLASK_APP=jobcentral-app/app.py

#On Windows: cmd
C:\path\to\joboffers>set FLASK_APP=jobcentral-app\app.py

#On windows: powershell
$env:FLASK_APP = "hello.py"

flask run
```

## Database manager

The database is hosted on a MongoDB Atlas Database (free tier)

* Username: testuser
* Password: testuser

It's ruled by three operations repeating themselves at 9 AM :

* Inserting and updating data from one or multiple job boards
* Cleaning up the data in a clean collection
* Creating a TF-IDF model from the clean data, used in the app

The current schema of the database goes like this

| _id                 | string |
|---------------------|--------|
| url                 | string |
| title               | string |
| company             | string |
| address             | string |
| description         | string |
| job_type            | string |
| keyword_frequency   | Array  |
| descriptionLanguage | string |

## App

Though a **Flask** app the user can do queries and fetch a job by certain criteria :
* Keywords
* City

The algorithm will perform a cosine similarity over the vectorized keyword string and return on a result page the most relevant offers. The city argument will be used to perform a regex search on it.

## Messaging

We need to find an API that can send you notifications through your mail address.

## Project schedule

Available in French :

https://docs.google.com/spreadsheets/d/1GTKcRXZuHFAseyEYP8jcjEyoOOkH5gcijuvUz66B7jQ/edit?usp=sharing

## To-Dos 

[x] Implement a search engine
[] Implement a mail alert

[] Add more JobBoards
[] Customize template
[] Add more keywords
[] Adopt a class system for each JobBoard