# Job Central

The project's goal is to get several informations from JobBoards like Indeed or Monster. The app will refresh its data everyday at 9 AM.

Main target : [Indeed (FR)](https://www.indeed.fr/)

We're retrieving the essential information :
* Title
* Link
* City (City name + region/state/country)
* Job type and status
* **BONUS:** we'll be looking at required technological skills suited for the job and list them up

## Database

The main database will be a MongoDB database, which is not only useful for scalability, but also stocking subcollections.

Each collection will be named after a special query (ex. "data)

The database will be fed at the appropriate hours.

A PostgreSQL alternative is considered, but the whole process will be stocked inside a MongoDB database.

## App

Though a **Flask** app the user can do queries and fetch a job by certain criteria :
* Keywords
* City
* Title

## Messaging

We need to find an API that can send you notifications through your mail address.

## Project schedule

Available in French :

https://docs.google.com/spreadsheets/d/1GTKcRXZuHFAseyEYP8jcjEyoOOkH5gcijuvUz66B7jQ/edit?usp=sharing

