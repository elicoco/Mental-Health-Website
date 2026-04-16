from datetime import datetime, timedelta
import json
import os
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, session, url_for
from flask_session import Session
from flask_compress import Compress
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect
from Backend.daily_tracker.dailytrackercalculator import calculate_mood_exercise_on_username, calculate_mood_meditation_on_username, calculate_mood_productive_on_username, calculate_mood_sleep_on_username, check_data_exists
from Backend.database.daily_tracker import check_daily_tracker_access_by_username, create_daily_tracker_for_date, create_new_daily_tracker_by_username, delete_daily_tracker_by_id, get_daily_tracker_by_id, get_daily_trackers_by_username, get_daily_trackers_by_username_date, update_daily_tracker_by_id
from Backend.database.journal import check_journal_access_by_username, create_new_journal_by_username, delete_journal_by_id, get_journal_by_journal_id, get_journals_by_username, update_journal_by_id
from Backend.database.habits import add_habit, delete_habit_permanently, end_habit, get_all_habits_for_user, get_habits_with_completion, get_total_habit_checkins, resume_habit, toggle_habit_log
from Backend.database.login import authenticate_user
from Backend.custom.customclasses import Snackbar, InputLogin, SignupInformation
from Backend.database.signup import create_new_user, verify_user_by_email_verification_key
from Backend.meditations.search_meditations import get_all_meditations, get_meditation_by_id, search_meditation_on_key

load_dotenv()
app = Flask(__name__, static_folder='Static')
app.secret_key = os.getenv('APPSECRETKEY')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './flask_session/'
app.config['SESSION_PERMANENT'] = False
app.config['WTF_CSRF_TIME_LIMIT'] = None
Session(app)
csrf = CSRFProtect(app)
limiter = Limiter(get_remote_address, app=app, default_limits=[], storage_uri="memory://")
Compress(app)
green = "#4CAF50"
red = "#F44336"
blue = "#2196F3"
orange = "#FBC02D"

# function to check if user is in a session
def require_login():
    if 'username' in session: # if in a session
        return None
    else:
        return( redirect(url_for("login", 
        snackbar_message="Need to login", snackbar_colour=orange)))
        # redirect to login page

# main home page
@app.route("/")
def main():
    # check if user is logged in
    login_redirect = require_login()
    if login_redirect is not None:
        return login_redirect
    else:
        if request.args.get('snackbar_message','') != "":
            # checks if there is snackbar and sends snackbar accordingly
            snackbar = Snackbar(message=request.args.get('snackbar_message', ''),need_snackbar=True,colour=green)
        else:
            snackbar = (Snackbar(need_snackbar=False, colour="", message=""))
        today_dt = datetime.now()
        today = today_dt.strftime("%Y-%m-%d")
        hour = today_dt.hour
        greeting = "Good morning" if hour < 12 else "Good afternoon" if hour < 18 else "Good evening"

        all_trackers = get_daily_trackers_by_username(session['username'])
        tracked_today = bool(get_daily_trackers_by_username_date(session['username'], today))
        trackers_by_date = {t.date: t for t in all_trackers}

        last_7_days = []
        for i in range(6, -1, -1):
            d = today_dt.date() - timedelta(days=i)
            d_str = d.strftime("%Y-%m-%d")
            tracker = trackers_by_date.get(d_str)
            last_7_days.append({
                'date': d_str,
                'day': d.strftime('%a'),
                'mood': tracker.mood_score if tracker else None,
                'tracker_id': tracker.id if tracker else None,
                'is_today': i == 0
            })

        all_habits = get_all_habits_for_user(session['username'])
        active_habits = [h for h in all_habits if h['is_active']]
        total_tracked = len(all_trackers)
        total_habit_checkins = get_total_habit_checkins(session['username'])

        # Aggregate stats from tracker entries
        total_meditation_mins = sum(t.meditation_mins or 0 for t in all_trackers)
        total_exercise_mins = sum(t.exercise_mins or 0 for t in all_trackers)
        sleep_hours_list = [
            (24 - t.bed_time + t.wakeup_time) if t.bed_time > t.wakeup_time else (t.wakeup_time - t.bed_time)
            for t in all_trackers if t.bed_time is not None and t.wakeup_time is not None
        ]
        avg_sleep = round(sum(sleep_hours_list) / len(sleep_hours_list), 1) if sleep_hours_list else 0

        def fmt_mins(m):
            if m >= 60:
                h, rem = divmod(m, 60)
                return f"{h}h {rem}m" if rem else f"{h}h"
            return f"{m}m"

        total_meditation = fmt_mins(total_meditation_mins)
        total_exercise = fmt_mins(total_exercise_mins)

        # Consecutive days-tracked streak (today not tracked yet doesn't break it)
        tracked_dates = {t.date for t in all_trackers}
        current_streak = 0
        check = today_dt.date()
        if today not in tracked_dates:
            check -= timedelta(days=1)
        while check.strftime("%Y-%m-%d") in tracked_dates:
            current_streak += 1
            check -= timedelta(days=1)
        best_streak = current_streak

        return render_template("home.html", snackbar=snackbar, username=session['username'],
                               tracked_today=tracked_today, today=today, greeting=greeting,
                               last_7_days=last_7_days, active_habits=active_habits,
                               total_tracked=total_tracked, best_streak=best_streak,
                               total_habit_checkins=total_habit_checkins,
                               avg_sleep=avg_sleep, total_meditation=total_meditation,
                               total_exercise=total_exercise)

# login page
@app.route("/login",methods=["GET","POST"])
@limiter.limit("10 per minute")
def login():
    if request.method == "POST":
        # gets form if it is a POST request
        username = request.form['username']
        password = request.form['password']
        if username is not None and password is not None:
            # checks data is not empty
            information = InputLogin(username=username, password=password)
            # calls a function to check if the login information is correct
            snackbar = authenticate_user(information)
            if snackbar.colour == green:
                session.clear()
                session['username'] = username
                return redirect(url_for("main", snackbar_message=snackbar.message)) 
                # redirect to homepage if login works
            else:
                # send error message if login doesn't work
                return render_template("login.html",loggedin=False, snackbar = snackbar, username = username)
    else:
        if require_login() is not None:
            snackbar_message = request.args.get('snackbar_message', '')
            if snackbar_message != '':
                # checks for snackbar message and displays snackbar accordingly
                snackbar = (Snackbar(message=snackbar_message,
                need_snackbar=True,colour=request.args.get('snackbar_colour','')))
                username = request.args.get('username', '')
            else:
                snackbar = (Snackbar(need_snackbar=False, colour="", message=""))
                username = ""
            return render_template("login.html",loggedin=False, snackbar = snackbar, username = username)
        else:
            # if already logged in redirect to home page
            return redirect(url_for("main",snackbar_message="Already Logged In"))

#signup page
@app.route("/signup",methods=["GET","POST"])
@limiter.limit("5 per minute")
def signup():
    if request.method == "POST": 
        # user sending a request to the server
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        # gets all information from form
        info_signup = SignupInformation(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        # calls function to create new user
        snackbar = create_new_user(info_signup)
        if snackbar.colour == green: 
            # if signup successful goes to login page
            return redirect(url_for("login", snackbar_message=snackbar.message,username=info_signup.username,snackbar_colour=green))
        else:
            # if signup unsuccessful stays on signup page
            return render_template("signup.html", loggedin=False, snackbar = snackbar, info = info_signup)
    else:
        if 'username' in session:
            # if already logged in redirect user to home page
            return redirect(url_for("main",snackbar_message="Already Logged In"))
        else:
            info_signup = SignupInformation(username="", password="", email="", first_name="", last_name="")
            return render_template("signup.html", loggedin=False, info = info_signup)

# email verification page
@app.route("/emailverification/<key>")
def email_verification(key):
    # calls function to check if key works
    check_if_verified = verify_user_by_email_verification_key(key)
    if check_if_verified:
        # if works takes to email verified page
        return render_template("email_verified.html",loggedin=False)
    else:
        # if it does not work takes to email not verified page
        return render_template("email_not_verified.html",loggedin=False)

@app.route("/journal")
def journal():
    login_redirect = require_login()
    if login_redirect is not None:
        return login_redirect
    else:
        journals = get_journals_by_username(username=session['username'])
        for current_journal in journals:
            current_journal.date_created = datetime.strptime(current_journal.date_created, "%Y-%m-%d").strftime("%B %d, %Y")
        snackbar_message = request.args.get('snackbar_message', '')
        if snackbar_message != '':
            snackbar = (Snackbar(message=snackbar_message,
            need_snackbar=True,colour=request.args.get('snackbar_colour','')))
        else:
            snackbar = (Snackbar(need_snackbar=False, colour="", message=""))
        return render_template("journal_search.html",journals=journals, snackbar=snackbar)

@app.route("/journal/<id>", methods=["GET","POST"])
def journal_id(id):
    if request.method == "GET":
        login_redirect = require_login()
        if login_redirect is not None:
            return login_redirect
        else:
            if check_journal_access_by_username(username=session['username'],journal_id=id):
                # checks if user is allowed to access this journal
                current_journal = get_journal_by_journal_id(journalid=id)
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

# new journal route
@app.route('/new_journal')
def new_journal():
    # check if logged in
    login_redirect = require_login()
    if login_redirect is not None:
        return login_redirect
    else:
        # create a new journal for the user
        current_journal = create_new_journal_by_username(session['username'])

        # redirect to journals page for new journal created
        return redirect(url_for('journal_id', id=current_journal.id))

# deleting journal route
@app.route('/delete_journal/<id>')
def delete_journal(id):
    login_redirect = require_login()
    if login_redirect is not None:
        return login_redirect
    else:
        if check_journal_access_by_username(username=session['username'],journal_id=id):
            # checks if it has access to delete this journal
            delete_journal_by_id(id)
            snackbar_message = "Journal Deleted Successfully" 
            snackbar_colour = green  
        else: # if it does not have access to delete this journal
            snackbar_message = "You do not have access to this journal"
            snackbar_colour = red
    # goes to the main journal page and displays a snackbar which says whether the user
    # has successfully deleted the journal
        return redirect(url_for('journal', snackbar_message=snackbar_message, snackbar_colour=snackbar_colour))

# main daily tracker page route
@app.route("/daily_tracker")
def daily_tracker():
    login_redirect = require_login()
    if login_redirect is not None:
        return login_redirect
    else:
        daily_trackers = get_daily_trackers_by_username(username=session['username'])
        for current_daily_tracker in daily_trackers:
            # converts date into readable format
            current_daily_tracker.date = datetime.strptime(current_daily_tracker.date, "%Y-%m-%d").strftime("%B %d, %Y")
        snackbar_message = request.args.get('snackbar_message', '')
        if snackbar_message != '':
            snackbar = (Snackbar(message=snackbar_message,
            need_snackbar=True,colour=request.args.get('snackbar_colour','')))
        else:
            snackbar = (Snackbar(need_snackbar=False, colour="", message=""))
        return render_template("daily_tracker_search.html",daily_trackers=daily_trackers, snackbar=snackbar)

@app.route("/daily_tracker/<id>", methods=["GET","POST"])
def daily_tracker_id(id):
    if request.method == "GET":
        login_redirect = require_login()
        if login_redirect is not None:
            return login_redirect
        else:
            if check_daily_tracker_access_by_username(username=session['username'],daily_tracker_id=id):
                # checks if user is allowed to access this daily_tracker
                current_daily_tracker = get_daily_tracker_by_id(daily_tracker_id=id)
                raw_date = current_daily_tracker.date
                habits = get_habits_with_completion(session['username'], raw_date)
                current_daily_tracker.date = datetime.strptime(raw_date, "%Y-%m-%d").strftime("%B %d, %Y")
                return render_template("daily_tracker.html", daily_tracker=current_daily_tracker,
                                       habits=habits, raw_date=raw_date)
            else:
                return redirect(url_for('daily_tracker', snackbar_message="You do not have access to this Daily Tracker", snackbar_colour=red))
    elif request.method == "POST":
        if check_daily_tracker_access_by_username(username=session['username'],daily_tracker_id=id):
            # Get JSON data sent from the frontend
            data = request.get_json()
            # Validate incoming data
            if ("comment" not in data or "mood_score" not in data or "bed_time" not in data or 
                "wakeup_time" not in data  or "meditation_mins" not in data  or "productive_mins" not in data
                 or "exercise_mins" not in data):
                return {"error": "Invalid data format"}, 400     
            updated_comment = data["comment"]
            updated_mood_score = data["mood_score"]
            updated_bed_time = data["bed_time"]
            updated_wakeup_time = data["wakeup_time"]
            updated_meditation_mins = data["meditation_mins"]
            updated_productive_mins = data["productive_mins"]
            updated_exercise_mins = data["exercise_mins"]
            # Update daily_tracker in the database
            update_daily_tracker_by_id(id=id, comment=updated_comment, mood_score=updated_mood_score,
            bed_time=updated_bed_time,wakeup_time=updated_wakeup_time,meditation_mins=updated_meditation_mins,
            productive_mins=updated_productive_mins, exercise_mins=updated_exercise_mins)
            return {"message": "Daily Tracker updated successfully"}, 200
        else: # if user is not allowed access to this daily tracker
            return redirect(url_for('daily_tracker', snackbar_message="You do not have access to this Daily Tracker", snackbar_colour=red))

@app.route('/habits')
def habits_page():
    login_redirect = require_login()
    if login_redirect is not None:
        return login_redirect
    habits = get_all_habits_for_user(session['username'])
    today = datetime.now().strftime('%Y-%m-%d')
    snackbar_message = request.args.get('snackbar_message', '')
    snackbar_colour = request.args.get('snackbar_colour', green)
    snackbar = Snackbar(need_snackbar=bool(snackbar_message), colour=snackbar_colour, message=snackbar_message)
    return render_template('habits.html', habits=habits, today=today, snackbar=snackbar)

@app.route('/habits/add', methods=['POST'])
def add_habit_route():
    login_redirect = require_login()
    if login_redirect is not None:
        return login_redirect
    name = request.form.get('name', '').strip()
    start_date = request.form.get('start_date', datetime.now().strftime('%Y-%m-%d'))
    if name:
        add_habit(session['username'], name, start_date)
    return redirect(url_for('habits_page'))

@app.route('/habits/<int:habit_id>/end', methods=['POST'])
def end_habit_route(habit_id):
    login_redirect = require_login()
    if login_redirect is not None:
        return login_redirect
    end_date = request.form.get('end_date', datetime.now().strftime('%Y-%m-%d'))
    end_habit(habit_id, end_date, session['username'])
    return redirect(url_for('habits_page'))

@app.route('/habits/<int:habit_id>/resume', methods=['POST'])
def resume_habit_route(habit_id):
    login_redirect = require_login()
    if login_redirect is not None:
        return login_redirect
    start_date = request.form.get('start_date', datetime.now().strftime('%Y-%m-%d'))
    resume_habit(habit_id, start_date, session['username'])
    return redirect(url_for('habits_page'))

@app.route('/habits/<int:habit_id>/delete', methods=['POST'])
def delete_habit_route(habit_id):
    login_redirect = require_login()
    if login_redirect is not None:
        return login_redirect
    delete_habit_permanently(habit_id, session['username'])
    return redirect(url_for('habits_page'))

@app.route('/toggle_habit', methods=['POST'])
def toggle_habit_route():
    login_redirect = require_login()
    if login_redirect is not None:
        return login_redirect, 401
    data = request.get_json()
    if 'habit_id' not in data or 'date' not in data:
        return {"error": "Invalid data"}, 400
    completed = toggle_habit_log(data['habit_id'], data['date'], session['username'])
    return {"completed": completed}, 200

@app.route('/new_daily_tracker')
def new_daily_tracker():
    login_redirect = require_login()
    if login_redirect is not None:
        return login_redirect
    else:
        current_daily_tracker = create_new_daily_tracker_by_username(session['username'])
        return redirect(url_for('daily_tracker_id', id=current_daily_tracker.id))
    # redirect to daily_trackers page for new daily_tracker

@app.route('/delete_daily_tracker/<id>')
def delete_daily_tracker(id):
    login_redirect = require_login()
    if login_redirect is not None:
        return login_redirect
    else:
        if check_daily_tracker_access_by_username(username=session['username'],daily_tracker_id=id):
            # checks if it has access to delete this daily_tracker
            delete_daily_tracker_by_id(id)
            snackbar_message = "Daily Tracker Deleted Successfully" 
            snackbar_colour = green  
        else: # if it does not have access to delete this daily_tracker
            snackbar_message = "You do not have access to this Daily Tracker"
            snackbar_colour = red
        return redirect(url_for('daily_tracker', snackbar_message=snackbar_message, snackbar_colour=snackbar_colour))

# for all graphs
@app.route('/graph/<group_type>')
def display_scatter_graph(group_type):
    login_redirect = require_login()
    if login_redirect is not None:
        return login_redirect
    else:
        if not check_data_exists(session['username']):
            # if there is no data then it will redirect to the daily tracker page so there is no error
            snackbar_message = "No data to be analysed"
            return redirect(url_for('daily_tracker', snackbar_message=snackbar_message, snackbar_colour=orange))
        # checks the group_type and if it doesn't exist then it redirects to 
        # the main daily tracker page
        if group_type == 'exercise': # for exercise type
            data = calculate_mood_exercise_on_username(session['username'])
        elif group_type == 'meditation': # for meditation type
            data = calculate_mood_meditation_on_username(session['username'])
        elif group_type == 'productivity': # for productive type
            data = calculate_mood_productive_on_username(session['username'])
        elif group_type == 'sleep': # for sleep type
            data = calculate_mood_sleep_on_username(session['username'])
        else: # if not for any group type
            snackbar_message = "This graph does not exist"
            snackbar_colour = orange
            return redirect(url_for('daily_tracker', snackbar_message=snackbar_message, snackbar_colour=snackbar_colour))
        # collects the data from the backend
        stats_json = json.dumps(data.to_dict())
        group_type = group_type.capitalize()
        return render_template("scatter-graph-display.html", stats=stats_json, name = group_type)

@app.route('/calendar')
def calendar():
    login_redirect = require_login()
    if login_redirect is not None:
        return login_redirect
    else:
        data = get_daily_trackers_by_username(session['username'])
        # converts it to json for transfer to JS
        trackers_dict_list = [tracker.to_dict() for tracker in data]
        daily_trackers_json = json.dumps(trackers_dict_list, indent=4)
        snackbar_message = request.args.get('snackbar_message', '')
        snackbar_colour = request.args.get('snackbar_colour', orange)
        snackbar = Snackbar(need_snackbar=bool(snackbar_message), colour=snackbar_colour, message=snackbar_message)
        return render_template("calendar.html", dailytrackers=daily_trackers_json, snackbar=snackbar)


@app.route('/day/<date>')
def display_day(date):
    login_redirect = require_login()
    if login_redirect is not None:
        return login_redirect
    if date > datetime.now().strftime("%Y-%m-%d"):
        snackbar = Snackbar(message="You can't log a future date", need_snackbar=True, colour=orange)
        return redirect(url_for('calendar', snackbar_message=snackbar.message, snackbar_colour=snackbar.colour))
    current_daily_tracker = get_daily_trackers_by_username_date(session['username'], date)
    if not current_daily_tracker:
        current_daily_tracker = create_daily_tracker_for_date(session['username'], date)
    return redirect(url_for('daily_tracker_id', id=current_daily_tracker.id))

# code for a single meditation page
@app.route("/meditation/<id>")
def meditation(id):
    if 'username' in session:
        logged_in = True
    else:
        logged_in = False
    # get meditation from current id
    current_meditation = get_meditation_by_id(id)
    # if there aren't any meditations with this id
    if not current_meditation:
        return render_template("meditation_search.html", searchvalue="",
            meditations = get_all_meditations(), snackbar = Snackbar(need_snackbar=True,
                colour = orange, message= "Meditation Does Not Exist"))
    filename = url_for('static', filename=f"audio/{current_meditation.filename}")
    # adds filename for meditation audio file
    return render_template("meditation.html", meditation=current_meditation,
    audio_file = filename, loggedin=logged_in)

# page which shows all meditations
@app.route("/meditation_search/")
@app.route("/meditation_search")
def all_meditations():
    if 'username' in session:
        logged_in = True
    else:
        logged_in = False
    meditations = get_all_meditations()
    # this will be an array of meditationClassifiers
    return render_template("meditation_search.html",loggedin=logged_in, searchvalue="", meditations = meditations)

# page which shows meditations when searched for
@app.route("/meditation_search/<search_key>")
def meditation_search(search_key):
    if 'username' in session:
        logged_in = True
    else:
        logged_in = False
    meditations = search_meditation_on_key(search_key)
    # this will be an array of meditationClassifiers
    return render_template("meditation_search.html",loggedin=logged_in, searchvalue=search_key, meditations = meditations)

@app.route('/health')
def health():
    return {"status": "ok"}, 200

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", loggedin='username' in session), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html", loggedin='username' in session), 500

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))
# allows user to log out

if __name__=='__main__':
   app.run(port=5000)