from flask import Flask, render_template, request, redirect, session, flash
# the "re" module will let us perform some regular expression operations
import re
# create a regular expression object that we can use run operations on
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# import the function connectToMySQL from the file mysqlconnection.py
from mysqlconnection import connectToMySQL
app = Flask(__name__)
app.secret_key = "KeepItSecrectKeepItSafe!"
# invoke the connectToMySQL function and pass it the name of the database we're using
# connectToMySQL returns an instance of MySQLConnection, which we will store in the variable 'mysql'
mysql = connectToMySQL('email_db')
# now, we may invoke the query_db method

# print("all the users", mysql.query_db("SELECT * FROM emails;"))

@app.route('/')
def index():

    return render_template('index.html')

@app.route('/process', methods=['POST'])
def validate():
    if len(request.form['email']) < 1:
        flash("Email cannot be blank!")
        return redirect('/')
    # else if email doesn't match regular expression display an "invalid email address" message
    # elif not
    elif not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid Email Address!")
        return redirect('/')
    else:
        query = "INSERT INTO emails(email, created_at) VALUES (%(email)s, NOW());"
        data = {
                 'email': request.form['email'],
                 'created_at': request.form['created_at']
               }
        mysql.query_db(query, data)
        return redirect('/success')

@app.route('/success')
def create():
    flash("Success! Email address was added to list!")

    all_emails = mysql.query_db("SELECT * FROM emails")
    print('All Emails: ', all_emails)

    return render_template('success.html', emails=all_emails)


@app.route('/success')
def success():
    all_emails = mysql.query_db("SELECT * FROM emails")
    return render_template('success.html' , emails=all_emails)


if __name__=="__main__":
    app.run(debug=True)
