@app.route("/meditation_search")
def meditation_search():
    a = render_template("meditation_search.html",)
    return a


@app.route("/meditation/search/<searchkey>")
def search_meditation(searchkey):
    meditations_searched = search_meditation_on_key(searchkey, allmeditations)
    a = render_template("meditation_search.html", meditations = meditations_searched)
    return a