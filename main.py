from datetime import datetime
import json
import os
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, session, url_for
from flask_session import Session
from Backend.daily_tracker.dailytrackercalculator import calculate_mood_exercise_on_username, calculate_mood_meditation_on_username, calculate_mood_productive_on_username, calculate_mood_sleep_on_username, check_data_exists
from Backend.database.daily_tracker import check_daily_tracker_access_by_username, create_new_daily_tracker_by_username, delete_daily_tracker_by_id, get_daily_tracker_by_id, get_daily_trackers_by_username, update_daily_tracker_by_id
from Backend.database.journal import check_journal_access_by_username, create_new_journal_by_username, delete_journal_by_id, get_journal_by_journalid, get_journals_by_username, update_journal_by_id
from Backend.database.login import check_login
from Backend.custom.customclasses import Journal, Snackbar, input_login, signup_information
from Backend.database.signup import create_new_user, verify_user_by_email_verification_key
# Replace with your Gmail email address
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('APPSECRETKEY')
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
        if 'username' in session:
            return redirect(url_for("main",snackbar_message="Already Logged In"))
        else:
            info_signup = signup_information(username="", password="", email="",first_name="",last_name="")
            return render_template("signup.html", loggedin=False, info = info_signup)

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

@app.route("/daily_tracker")
def daily_tracker():
    in_session = check_if_session()
    if in_session != None:
        return in_session
    else:
        daily_trackers = get_daily_trackers_by_username(username=session['username'])
        for daily_tracker in daily_trackers:
            daily_tracker.date = datetime.strptime(daily_tracker.date, "%Y-%m-%d").strftime("%B %d, %Y")
        if request.args.get('snackbar_message','') != None:
            snackbar = (Snackbar(message=request.args.get('snackbar_message', ''),
            need_snackbar=True,colour=request.args.get('snackbar_colour','')))
        else:
            snackbar = (Snackbar(need_snackbar=False, colour="", message=""))
        return render_template("daily_tracker_search.html",daily_trackers=daily_trackers, snackbar=snackbar)

@app.route("/daily_tracker/<id>", methods=["GET","POST"])
def daily_tracker_id(id):
    if request.method == "GET":
        in_session = check_if_session()
        if in_session != None:
            return in_session
        else:
            if check_daily_tracker_access_by_username(username=session['username'],daily_tracker_id=id):
                # checks if user is allowed to access this daily_tracker
                current_daily_tracker = get_daily_tracker_by_id(daily_tracker_id=id)
                current_daily_tracker.date = datetime.strptime(current_daily_tracker.date, "%Y-%m-%d").strftime("%B %d, %Y")
                print(current_daily_tracker)
                return render_template("daily_tracker.html",daily_tracker=current_daily_tracker)
            else:
                return redirect(url_for('daily_tracker', snackbar_message="You do not have access to this Daily Tracker", snackbar_colour=red))
    elif request.method == "POST":
        if check_daily_tracker_access_by_username(username=session['username'],daily_tracker_id=id):
            # Get JSON data sent from the frontend
            data = request.get_json()
            # Validate incoming data
            print(data)
            if ("comment" not in data or "mood_score" not in data or "bed_time" not in data or 
                "wakeup_time" not in data  or "meditation_mins" not in data  or "prodcutive_mins" not in data
                 or "exercise_mins" not in data):
                return {"error": "Invalid data format"}, 400     
            updated_comment = data["comment"]
            updated_mood_score = data["mood_score"]
            updated_bed_time = data["bed_time"]
            updated_wakeup_time = data["wakeup_time"]
            updated_meditation_mins = data["meditation_mins"]
            updated_prodcutive_mins = data["prodcutive_mins"]
            updated_exercise_mins = data["exercise_mins"]
            # Update daily_tracker in the database
            update_daily_tracker_by_id(id=id, comment=updated_comment, mood_score=updated_mood_score,
            bed_time=updated_bed_time,wakeup_time=updated_wakeup_time,meditation_mins=updated_meditation_mins,
            productive_mins=updated_prodcutive_mins, exercise_mins=updated_exercise_mins)
            return {"message": "Daily Tracker updated successfully"}, 200
        else: # if user is not allowed access to this daily tracker
            return redirect(url_for('daily_tracker', snackbar_message="You do not have access to this Daily Tracker", snackbar_colour=red))

@app.route('/new_daily_tracker')
def new_daily_tracker():
    in_session = check_if_session()
    if in_session is not None:
        return in_session
    else:
        current_daily_tracker = create_new_daily_tracker_by_username(session['username'])
        return redirect(url_for('daily_tracker_id', id=current_daily_tracker.id))
    # redirect to daily_trackers page for new daily_tracker

@app.route('/delete_daily_tracker/<id>')
def delete_daily_tracker(id):
    in_session = check_if_session()
    if in_session is not None:
        return in_session
    else:
        if check_daily_tracker_access_by_username(username=session['username'],daily_tracker_id=id):
            # checks if has access to delete this daily_tracker
            delete_daily_tracker_by_id(id)
            snackbar_message = "Daily Tracker Deleted Successfully" 
            snackbar_colour = green  
        else: # if does not have access to delete this daily_tracker
            snackbar_message = "You do not have access to this Daily Tracker"
            snackbar_colour = red
        return redirect(url_for('daily_tracker', snackbar_message=snackbar_message, snackbar_colour=snackbar_colour))

# for all graphs
@app.route('/graph/<grouptype>')
def display_scatter_graph(grouptype):
    in_session = check_if_session()
    if in_session is not None:
        return in_session
    else:
        if check_data_exists(session['username']) == False:
            # if there is no data then it will redirect to the daily tracker page so there is no error
            snackbar_message = "No data to be analysed"
            return redirect(url_for('daily_tracker', snackbar_message=snackbar_message, snackbar_colour=orange))
        # checks the grouptype and if it doesn't exist then it redirects to 
        # the main daily tracker page
        if grouptype == 'exercise': # for exercise type
            data = calculate_mood_exercise_on_username(session['username'])
        elif grouptype == 'meditation': # for meditation type
            data = calculate_mood_meditation_on_username(session['username'])
        elif grouptype == 'productive': # for productive type
            data = calculate_mood_productive_on_username(session['username'])
        elif grouptype == 'sleep': # for sleep type
            data = calculate_mood_sleep_on_username(session['username'])
        else: # if not for any group type
            snackbar_message = "This graph does not exist"
            snackbar_colour = orange
            return redirect(url_for('daily_tracker', snackbar_message=snackbar_message, snackbar_colour=snackbar_colour))
        # collects the data from the backend
        stats_json = json.dumps(data.to_dict())
        grouptype = grouptype.capitalize()
        return render_template("scatter-graph-display.html", stats=stats_json, name = grouptype)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))
# allows user to log out

if __name__=='__main__':
   app.run(port=5000)