from flask import Flask, abort, redirect, render_template, request, url_for 
from datetime import date
import database

app = Flask(__name__)
database.database_setup()

def days_left(closing):
    if not closing:
        return None
    try:
        closing_date = date.fromisoformat(closing)
    except ValueError:
        return None
    return (closing_date - date.today())

@app.route("/")
def index():
    applications = database.get_all_applications() 
    return render_template("index.html", applications=applications)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        database.add_application(
            request.form["company"],
            request.form["role"],
            request.form["location"],
            request.form["dateopened"],
            request.form["dateclosing"],
            request.form["link"],
            request.form["stages"],
            request.form["notes"],
        )
        return redirect(url_for("index"))
    return render_template(
        "form.html", application=None, stages=database.STAGES, title="Add a new application:")

@app.route("/edit/<int:application_id>", methods=["GET", "POST"])
def edit(application_id):
    application = database.get_application_by_id(application_id)
    if application is None:
        abort(404)
    if request.method == "POST":
        database.edit_application(
            application_id,
            request.form["company"],
            request.form["role"],
            request.form["location"],
            request.form["dateopened"],
            request.form["dateclosing"],
            request.form["link"],
            request.form["stages"],
            request.form["notes"],
        )
        return redirect(url_for("index"))
    return render_template("form.html", application=application, stages=database.STAGES, title="Edit application:") 

@app.route("/delete/<int:application_id>", methods=["POST"]) 
def delete(application_id):
    database.delete_application(application_id) 
    return redirect(url_for("index")) 


if __name__ == '__main__':
    app.run(debug=True, port=5001)   

