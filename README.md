# Project manager

A Flask app for easily saving workhours and managing projects. The project is for University of Helsinki course Tietokantasovellus.

This app aims to make it easy to handle your work projects. It allows the user to use a stopwatch for saving workhours, comments for each session, choosing clients for projects etc. App is made for use in work, but it can be used for studies as well. Companies can be thought as courses, and projects as assignments.

Latest version can be tested in [Heroku](https://tsoha-project-manager.herokuapp.com). Instructions can be found below as well as in help-page of the app.

[SQL scheme](/schema.sql)

[Instructions](https://github.com/Capslock01/project-manager#instructions)

[Development progress](https://github.com/Capslock01/project-manager#development-progress)

[Known issues](https://github.com/Capslock01/project-manager#known-issues)

## Instructions

### Quick start

1. Create a user by selecting "register" from user menu in top right.
2. Log in to your new user, and open "app" from navbar.
3. Create a company to which you can assign your first project.
4. Create a project. If you don't find a good worktype, create a new one.
5. Start timing your project. You can also create more projects to create a todo-list on the active projects page.
6. When the project is finished, click the red "stop" button, and the project can be found by clicking the link below active projects list.

### Worktypes

Worktypes are used to round project times when finishing project. Worktypes have a name, a minimum time, a rounding time and price per hour. Projects are always rounded to the next full multiple of the rounding time. If you don't want to round the times, you can give worktype rounding/minimum time of 0. Project prices are yet to be shown anywhere, but it's WIP. Worktype data will also be shown more clearly later.

Current premade work types:
- Default: minimum 30 minutes, rounded to next full 30 minutes, priced at 20 €/h
- Short task: min 10 min, rounded to 1 min, 30 €/h
- Free: min 1 min, rounded to 1 min, 0 €/h

### Commenting project and editing a project/entry

You can click the "edit project" button with a pencil icon to view projet editing options. You can add a comment to the project as a note for the next time you work on that project. You can also rename the project, change worktype or change the client compay. You can also see all timed entries for the project. You can see when you have worked on that project, view comments and also edit entries. You also have 2 buttons to change the project's time easily. The amount is determined by chosen worktype. The change is same as worktype's rounding time. Entries have a similar edit button, and you can change start and end times, edit comment or delete entry.

### Deleting data

Projects can be deleted from editing view. This also deletes all entries for that said project. Entries can be deleted one-by-one from entry editing view. Deleting users or companies is yet to be implemented.

## Development progress

The app aims to be simple to use, yet versatile. Almost all planned features are done, and work very well in testing. Code has been checked using pylint, pycodestyle and flake8, and has very few errors.

### Planned features

- login to use app (done)
- create and delete your projects (done)
- time project using start/pause/stop, stop rounds time according to worktype (done)
- times saved using stopwatch can be edited, if timer has been forgotten on or off (done)
- add comments after working sessions (done)
- finished (stopped) projects are not shown in default view, but can shown separately (done)
- create and delete client companies and assing projects to them (partly done, companies can't be deleted yet)
- view statistics for different time ranges (matplotlib?)
- maybe export saved times in csv or some other format
- manually created worktypes to determine rounding of times (done)
- edit and delete timed entries (done)
- pause all projects easily using a single button in case of phonecalls or other interruptions
- restart project after saving it (done)
- when creating a project allow user to create it, create and start it, or create and stop, which automatically saves an entry with minimum time for that worktype (done)

### Tables

At least these database tables will be used
- users(id, username, passwd)
- clients(id, name) maybe more columns later
- projects(id, status, comment, user_id, company_id, type_id)
- entries(id, project_id, starttime, endtime, comment)
- worktype(id, name, rounding, minimum, price)

# Known issues:

- Project timers and today's worktime are only updated when reloading page
