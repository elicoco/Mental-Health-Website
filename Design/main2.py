@app.route("/daily_tracker")
def daily_tracker():
    a = render_template("daily_tracker.html",)
    return a

@app.route("/meditation_search")
def meditation_search():
    a = render_template("meditation_search.html",)
    return a

@app.route("/journal")
def journal():
    journals = get_journals_by_userid(cursor=cursor,userid=current_user_id)
    a = render_template("journal_search.html",journals=journals)
    return a

@app.route("/journal/<id>")
def journal_date(id):
    current_journal = get_journal_by_journalid(cursor=cursor,journalid=id)
    a = render_template("journal.html",journal=current_journal)
    return a



@app.route("/meditation/search/<searchkey>")
def search_meditation(searchkey):
    meditations_searched = search_meditation_on_key(searchkey, allmeditations)
    a = render_template("meditation_search.html", meditations = meditations_searched)
    return a