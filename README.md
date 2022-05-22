# Project manager

A Flask app for managing and timing your projects. The project is for University of Helsinki course Tietokantasovellus.

This app aims to make it easy to handle your work projects. It allows the user to use a stopwatch for saving workhours, comments for each session, choosing clients for projects etc.

## Features

- login to use app (maybe organizations and admin users)
- create and delete your projects
- stopwatch type timing for projects, times are saved
- stopwatch can be edited when ending session, if timer has been forgotten on or off
- create and delete clients and assing projects to them
- add comments after working sessions
- view statistics for different time ranges (matplotlib?)
- maybe export saved times in csv or some other format

## Implementation

### Tables

At least these database tables will be used
- users(id, username, passwd) maybe admin column
- clients(id, name) maybe more columns later
- projects(id, user_id, name)
- entries(id, project_id, duration, timestamp, comment)

### Code
- data is always in database, and accessed when needed
- main functionality in a service file