from datetime import datetime
import time
from flask import Flask, flash, redirect, render_template, request, session, url_for
import requests
from flask_session import Session
from Backend.database.creating_tables import createalltables
from Backend.database.journal import check_journal_access_by_username, create_new_journal_by_username, delete_journal_by_id, get_journal_by_journalid, get_journals_by_username, update_journal_by_id
from Backend.database.login import check_login
from Backend.custom.customclasses import Journal, Snackbar, input_login, signup_information
from Backend.database.signup import create_new_user, verify_user_by_email_verification_key

app = Flask(__name__)
app.secret_key = 'iuoiuhiugy3e892r8076&*^$F^fs8^%&*(&gd))(*&y()09h&td6RNJJ)'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './flask_session/'
app.config['SESSION_PERMANENT'] = False
Session(app)
green = "#4CAF50"
red = "#F44336"
blue = "#2196F3"
orange = "#FBC02D"

def check_if_session():
    if 'username' in session: # if in a session
        return None
    else:
        return( redirect(url_for("login", 
        snackbar_message="Need to login", snackbar_colour=orange)))
        # redirect to login

@app.route("/")
def main():
    in_session = check_if_session()
    if in_session != None:
        return in_session
    else:
        if request.args.get('snackbar_message','') != "":
            snackbar = Snackbar(message=request.args.get('snackbar_message', ''),need_snackbar=True,colour=green)
        else:
            snackbar = (Snackbar(need_snackbar=False, colour="", message=""))
        return render_template("home.html", snackbar=snackbar, username = session['username'])

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if username != None and password != None:
            information = input_login(username=username,password=password)
            print(information)
            snackbar = check_login(information)
            if snackbar.colour == green:
                session['username'] = username
                return redirect(url_for("main", snackbar_message=snackbar.message)) # redirect to home
            else:
                return render_template("login.html",loggedin=False, snackbar = snackbar, username = username)
    else:
        if check_if_session() != None:
            if request.args.get('snackbar_message','') != None:
                snackbar = (Snackbar(message=request.args.get('snackbar_message', ''),
                need_snackbar=True,colour=request.args.get('snackbar_colour','')))
                username = request.args.get('username', '')
            else:
                snackbar = (Snackbar(need_snackbar=False, colour="", message=""))
                username = ""
            return render_template("login.html",loggedin=False, snackbar = snackbar, username = username)
        else:
            return redirect(url_for("main",snackbar_message="Already Logged In"))

@app.route("/signup",methods=["GET","POST"])
def signup():
    if request.method == "POST": # user sending a request to the server
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        info_signup = signup_information(username=username, password=password, email=email,first_name=first_name,last_name=last_name)
        snackbar = create_new_user(info_signup)
        if snackbar.colour == green: # if signup successful goes to login page
            return redirect(url_for("login", snackbar_message=snackbar.message,username=info_signup.username,snackbar_colour=green))
        else:
            return render_template("signup.html", loggedin=False, snackbar = snackbar, info = info_signup)
    else:
        snackbar = (Snackbar(need_snackbar=False, colour="", message=""))
        info_signup = signup_information(username="", password="", email="",first_name="",last_name="")
        return render_template("signup.html", loggedin=False,snackbar = snackbar, info = info_signup)

@app.route("/emailverification/<key>")
def email_verification(key):
    check_if_verified = verify_user_by_email_verification_key(key)
    if check_if_verified == True:
        return render_template("email_verified.html",loggedin=False)
    else:
        return render_template("email_not_verified.html",loggedin=False)

@app.route("/journal")
def journal():
    in_session = check_if_session()
    if in_session != None:
        return in_session
    else:
        journals = get_journals_by_username(username=session['username'])
        for journal in journals:
            journal.date_created = datetime.strptime(journal.date_created, "%Y-%m-%d").strftime("%B %d, %Y")
        if request.args.get('snackbar_message','') != None:
            snackbar = (Snackbar(message=request.args.get('snackbar_message', ''),
            need_snackbar=True,colour=request.args.get('snackbar_colour','')))
        else:
            snackbar = (Snackbar(need_snackbar=False, colour="", message=""))
        return render_template("journal_search.html",journals=journals, snackbar=snackbar)

@app.route("/journal/<id>", methods=["GET","POST"])
def journal_id(id):
    if request.method == "GET":
        in_session = check_if_session()
        if in_session != None:
            return in_session
        else:
            if check_journal_access_by_username(username=session['username'],journal_id=id):
                # checks if user is allowed to access this journal
                current_journal = get_journal_by_journalid(journalid=id)
                current_journal.date_created = datetime.strptime(current_journal.date_created, "%Y-%m-%d").strftime("%B %d, %Y")
                return render_template("journal.html",journal=current_journal)
            else:
                return redirect(url_for('journal', snackbar_message="You do not have access to this journal", snackbar_colour=red))
    elif request.method == "POST":
        if check_journal_access_by_username(username=session['username'],journal_id=id):
            # Get JSON data sent from the frontend
            data = request.get_json()
            # Validate incoming data
            if "title" not in data or "content" not in data:
                return {"error": "Invalid data format"}, 400     
            updated_title = data["title"]
            updated_content = data["content"]
            # Update journal in the database
            update_journal_by_id(id=id, title=updated_title, content=updated_content)
            return {"message": "Journal updated successfully"}, 200
        else:
            return redirect(url_for('journal', snackbar_message="You do not have access to this journal", snackbar_colour=red))

@app.route('/new_journal')
def new_journal():
    in_session = check_if_session()
    if in_session is not None:
        return in_session
    else:
        current_journal = create_new_journal_by_username(session['username'])
        return redirect(url_for('journal_id', id=current_journal.id))
    # redirect to journals page for new journal

@app.route('/delete_journal/<id>')
def delete_journal(id):
    in_session = check_if_session()
    if in_session is not None:
        return in_session
    else:
        if check_journal_access_by_username(username=session['username'],journal_id=id):
            # checks if has access to delete this journal
            delete_journal_by_id(id)
            snackbar_message = "Journal Deleted Successfully" 
            snackbar_colour = green  
        else: # if does not have access to delete this journal
            snackbar_message = "You do not have access to this journal"
            snackbar_colour = red
        return redirect(url_for('journal', snackbar_message=snackbar_message, snackbar_colour=snackbar_colour))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))
# allows user to log out

if __name__=='__main__':
   app.run(port=5000)