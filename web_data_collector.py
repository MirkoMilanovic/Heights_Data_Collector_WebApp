"""
1st try to make an idea for the program how to make it (separate it into smaller steps):
- building a frontend web page with an entry for a mail and height input (html+css+[js]), and a "Submit" button
- building a flask function (virtual environment first!!!)
- sending that to the backhand (string and num) PostgreSQL database (create it), say "Thank you to the frontend"
- calculating the median value
- send it to the mail of the users
- put the program on the web

FRONTEND
We should remember that with Flask we have this web structure, these folders that we first need to make:
- STATIC FOLDER (CSS FOLDER, IMAGES FOLDER)
- TEMPLATES FOLDER (HTML files)
- (.GIT FOLDER)                                     - When uploading to git
- program.PY

We did create HTML pages (index, success) and a CSS file (main.css), then:
create a virtual environment and activate it:
    pip3 install virtualenv.......... pip3 install flask
from flask import:
    Flask               - to make a flask, web application
    render_template     - to go to the different pages
    request             - access requests from the browser and read them
to run the prorgam:
    ...site> virtual\Scripts\activate                - to activate virtenv
    <virtual>...site> python web_data_collector.py          - execute the script with a python from virtual env
the app can be opened on the browser localhost, but we need to make a decorator for every page!
After making Flask, you should try if it works, it can't work without proper attributes in HTML:
        <form action="success.html" method="POST">             -> URL NOT FOUND   CHANGE TO:
        <form action="{{url_for('success')}}" method="POST">   -> URL METHOD NOT ALLOWED, decorators are by default GET!
Because the decorators are GET by default we need to declare POST in the decorator as a list, to make sure that it is
a POST request (URL found as a request, not by different means), and to capture the inputs.
    @app.route("/success/", methods=['POST']):

________________________________________________________________________________________________
DATABASE
We create a database in the PgAdmin4 called "height_collector", but instead of creating tables there, we use Python
instead. Creating tables and working with them using SQL we can use "psycopg2" library, but, most common is to use
"SQLAlchemy" library for Flask! It is a higher level, fewer lines of code (ex: not needed to connect to DB), it is based
on "psychopg2" though, so you need to install it first.
    <virtual>...site> pip3 install psychopg2
        - if it can't install, then search for precompiled python library, find the "38" ver if the Python3.8 is
        installed, put the ".whl "file next to ".py", and then:
            <virtual>...site> pip3 install  psycopg2-2.8.6-cp38-cp38-win32.whl
    <virtual>...site> pip3 install Flask-SQLAlchemy

    import sqlalchemy

We have to make a DB MODEL: contains tables. Model is the instance of the class.

Set the connection parameters to the database:
    app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:741m369@localhost/height_collector'
                                                         USER      PASS     PORT     DATABASE NAME
Creating a SQLAlchemy object from the Flask app called "app", store it in a variable "db":
    db=SQLAlchemy(app)
Creating a class for tables' "Data", we need to give it the Model class of the SQLAlchrmy, and to define all tables:
    class Data(db.Model):
        __tablename__="data"                            # name of the table
        id=db.Column(db.Integer, primary_key=True)      # new column for id, int, primary key
        email_=db.Column(db.String(120), unique=True)   # new column for email, string, unique
        height_=db.Column(db.Integer)                   # new column for height, int

        def __init__(self, email_, height_):            # initialize the variables of the objects, like in every class
            self.email_=email_
            self.height_=height_
Create the instance of the class Data (execute the class to create the table), how?
Not the best in the script, because the Flask will be executed. So the best is in the cmd directly:
    <virtual>...site> python                                    # run python console
    <virtual>...site> from web_data_collector2 import db        # from this script, import db (it is needed for the class)
    <virtual>...site> db.create_all()                           # SQLAlchemy method for creating the tables, fields

We check the pgAdmin, and we see that tables are created with no data inside. :))

FILL UP DATABASE WITH DATA
We have to point to the SQLAlchemy object (db.Model, to use the methods of the SQLAlchemy)
    data = Data(email, height)          # we send grabbed 2 values to the new db.Model obj of Data class
    db.session.add(data)                # ADD DATA; now we can use the SQLAlchemy methods (over db.Model obj)
    db.session.commit()                 # COMMIT CHANGES

We enter a new record on the page and check the database (SELECT * FROM data), we see that we have a new entered record

CHECK IF THE APPLICATION IS RUNNING SMOOTHLY
what if we enter the same record, email is unique, so we get an debug error, so we need to get one of the solutions:

    db.session.query(Data).filter(Data.email_==email)             # creates a SQL query where column email_=email
    db.session.query(Data).filter(Data.email_==email).count()     # how many rows meet the query (1 if we have an email)

    if db.session.query(Data).filter(Data.email_==email).count() == 0:      # we don't have a row with the same email
        data = Data(email, height)          # we send grabbed 2 values to the new db.Model obj of Data class
        db.session.add(data)                # ADD DATA; now we can use the SQLAlchemy methods (over db.Model obj)
        db.session.commit()                 # COMMIT CHANGES
        return render_template("success.html")    # go to the success.html only if it is added
    return render_template("index.html", text="Seems like we've got something from this email already!")  # if the
                            record is not added, then repeat the index page (refresh) and inform with some text
                            (point where in HTML!).

                HTML (point where to inform with text message):         CSS (change the style of the message):
                    <div class="message">                                   .message {
                        {{text | safe}}                                     font-family: Arial, sans-serif;
                    </div>                                                  font-size: 15px;
                                                                            color: #ff9999 }
SEND THE AVERAGE HEIGHTS TO THE EMAIL ADDRESS

For sending the email we make a separate module for that function "send_email.py" and we call it in the mail module.
To calculate average heights (+count), we have to do that inside the query and make a new sub-query, we have to:
    from sqlalchemy.sql import func
                ...
            average_height=db.session.query(func.avg(Data.height_))      # This is a query, SQL statement
            # print(average_height)     # check the result
            average_height=average_height.scalar()      # scalar result of this SQL statement, we have many decimals
            average_height=round(average_height, 1)     # round to 1 decimal place

            send_email(email, height, average_height, count)   # SEND EMAIL FUNCTION FROM DIFFERENT MODULE

HEROKU, UPLOAD, DATABASE

Create an account to heroku.com, download "heroku toolbelt". In the main directory of the app open the Terminal.
Initialize a hit repository in local dir, we need 3 files (Procfile, requirements.txt, runtime.txt), upload to Heroku.
But here we have one more thing! In the script we point to the local database. We have to make a database in Heroku!
Terminal(opened in the main program dir):
    ...site> heroku login            # log-in to heroku (press any key for login, accept)
    ...site> heroku create mirko-heights    # create an app (you can do it manually but this is recommended)
    ...site> heroku addons:create heroku-postgresql:hobby-dev --app mirko-heights    # create an database like
                               # an addon to the app, postgresql with type hobby-dev (free, limited), on the created app
    ...site> heroku config --app mirko-heights     # to get the online URL to heroku database, copy it to:
                    app.config['SQLALCHEMY_DATABASE_URI']='postgres://sjxwqbpowkcxuf:f24..... '
                    ADD TO URL STRING: '?sslmode=require'       - for working with a table over CMD
    ...site> virtual\Scripts\activate           - open virtual env
    <virtual>...site> pip install gunicorn
    <virtual>...site> pip freeze > requirements.txt
Make a Procfile with no extension with text:
    web: gunicorn web_data_collector3:app           # app is where the Flask object is created
Make a runtime.txt with text:
    python-3.9.0        - google the available python runtimes
For database, you need to create a file with no name, on Windows, this can be done in CMD:
    <virtual>...site> notepad .gitignore
There you write the name of directories and files NOT TO UPLOAD in Heroku (now virtual is on the same level, skip):
                        __pycache__
                        virtual
                        psycopg2-2.8.6-cp38-cp38-win32.whl
    <virtual>...site> git init      - initialise git repository (create .git dir)
    <virtual>...site> git add .     - add all
    <virtual>...site> git commit -m "first commit"      - commit changes
    <virtual>...site> heroku info   - check if we are connected to our app (no?-then next step:)
    <virtual>...site> heroku git:remote --app mirko-heights        - connect to the app
    <virtual>...site> git push heroku master        - execute all, push to git
    <virtual>...site> heroku open   - OPENS THE WEB APP OVER HEROKU, we can check if it's working well

We see that 1st page of the program is working but not the rest, we don't have created tables in the created database,
we have to do that manually, for the local database we did manually, too. Firstly, we run python on heroku:
    <virtual>...site> heroku run python
                (on Linux we can use: "heroku run bash" and then using Linux commands)
    >> from web_data_collector3 import db
    >> db.create_all()
    >> exit()
Now we should have created tables, to check if it's true:
    - go to the computer folder "C:\Program Files\PostgreSQL\10\bin", COPY that path (there should be 'psql.exe' inside)
    - go to the "Windows env. variables/Environment Variables", under "System variables", go to "Path", Edit.
    - add ";", and PASTE the previous path... OK
    - open the new Terminal:
            heroku login
            heroku pg:psql --app mirko-heights
    - we should be able to see this line: "mirko-heights::DATABASE=>" where we can enter SQL Queries (; at the end!):
    mirko-heights::DATABASE=> SELECT * FROM data;
             id | email_ | height_
            ----+--------+---------
            (0 rows)
    mirko-heights::DATABASE=> SELECT * FROM data;       - after adding some data, we have more records
             id |        email_        | height_
            ----+----------------------+---------
              1 | mirkommiki@gmail.com |     180
              2 | a@a.com              |      51
              3 | 12@a.com             |     190
    mirko-heights::DATABASE=> DELETE FROM data WHERE email_='mirkommiki@gmail.com' - to delete the record

INTERNAL SERVER ERROR
This is a typical "umbrella" error that occurs for any reason when the Flask app is not working, it is usually problem
with connection on DB, or sending mail parameters or safety or other problems... also, one of the HTML pages of the
Flask app could have this problem. To solve this, look at the Terminal, see the problems from the bottom.
If you use the app in Heroku, there is nothing written, but you can use:
    heroku logs --tail
and you can see the error code (example: H13), and google it.
Google has strong security, sometimes, you have to "Allow to other device to connect" next to "Allow less secure app",
in order to work (google to it)...:
    https://accounts.google.com/DisplayUnlockCaptcha        - next device allow to connect
    https://myaccount.google.com/lesssecureapps             - allow less secure apps
also, you can play with (not here):
    heroku config:set FLASK_ENV=production
    heroku config:set FLASK_ENV=development

"""
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_email import send_email
from sqlalchemy.sql import func

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:741m369@localhost/height_collector'  # old local database
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://fyzeacpjdeiblx:47b5ae4671ef55d4537ef6c7d6ac13fca1bd1ab837324f86bb44835cbe82e8d6@ec2-3-216-89-250.compute-1.amazonaws.com:5432/d8tgqtuj1v27lq?sslmode=require'
db=SQLAlchemy(app)         # creating DB variable to store a SQLAlchemy object from the Flask app called "app"


class Data(db.Model):       # creating a class for tables' Data (inside: open the Model class of the SQLAclchemy object)
    __tablename__="data"                            # name of the table
    id=db.Column(db.Integer, primary_key=True)      # new column for id, int, primary key
    email_=db.Column(db.String(120), unique=True)   # new column for email, string, unique
    height_=db.Column(db.Integer)                   # new column for height, int

    def __init__(self, email_, height_):            # initialize the variables of the objects, like in every class
        self.email_=email_
        self.height_=height_


@app.route("/")             # the decorator for the homepage
def index():
    return render_template("index.html")


@app.route("/success", methods=['POST'])    # the decorator for the success page, you must say that it is a post method
def success():
    if request.method=='POST':              # check if we got to the page by post request, if it is, then
        email=request.form["email_name"]    # we grab the email_name input from html
        height=request.form["height_name"]  # we grab the height_name input from html
        # print(email, height)      # instead of printing we want to send it, calling a function from the other module:
        # send_email(email, height)     # SEND EMAIL FUNCTION FROM DIFFERENT MODULE (we move it down to contain avg_h)
        # print(request.form)           # we can see the results in the cmd
        # print(db.session.query(Data).filter(Data.email_ == email))           # to see the SQL query
        if db.session.query(Data).filter(Data.email_ == email).count() == 0:   # we don't have a row with the same email
            data = Data(email, height)  # we send grabbed 2 values to the new db.Model obj of Data class
            db.session.add(data)        # ADD DATA; now we can use the SQLAlchemy methods (over db.Model obj)
            db.session.commit()         # commit changes

            average_height=db.session.query(func.avg(Data.height_))      # This is a query, SQL statement
            # print(average_height)     # check the result
            average_height=average_height.scalar()      # scalar result of this SQL statement, we have many decimals
            average_height=round(average_height, 1)     # round to 1 decimal place
            count=db.session.query(Data.height_).count()    # count the number of height values (number of users)

            send_email(email, height, average_height, count)   # SEND EMAIL FUNCTION FROM DIFFERENT MODULE

            return render_template("success.html")    # go to the success.html only if it is added
        return render_template("index.html", text="Seems like we've got something from this email already!")  # if the
        # record is not added, then repeat the index page (refresh) and inform with some text (point where in HTML!).

if __name__=="__main__":        # if the script is executed, not imported
    app.debug=True              # debug the errors of the web page (showing the debug explanation on the web), True when program, False when working
    app.run(port=5000)          # open it on the exact port, you can leave it empty (default is 5000)