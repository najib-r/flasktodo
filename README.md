# FLASK To-do App
### Video Demo:  <https://youtu.be/2w2D-wDIu48>
### Description:
A simple Flask to-do list application made with vanilla HTML, CSS and JavaScript on the frontend, Python (Flask) for the backend and sqlite3 for the database. Database is used to be able to store user's information for easy access with different devices.
#### helpers.py:
Used to define login_required function used in app.py
#### app.py:
- Check for valid username and password for registration and login
- Altering database based on user input
- Getting data from database to be shown to the user (the user's current tasks)
- Routing for different pages and GET/POST methods
#### register.html:
Page for user to register a new account. It is a form which routes to /register through POST which app.py will take the username and hashed password and store it in the users table in database.db 
#### login.html
Page for user to login an existing account. HTML form which routes to /login by POST, then app.py will check for validity and log user in.
#### index.html
This is the homepage when the user has logged in. It has an input at the top where user can add a to-do task. All previous and incomplete tasks are shown below it with a done button beside each task to mark it as complete.
#### history.html
Shows a table of all the tasks that have been completed by the user ordered by most recent
#### script.js
Used to show the dropdown only when the account icon at top right is clicked, otherwise it is hidden.

