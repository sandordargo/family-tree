from flask import Flask, render_template, request, url_for, redirect

from database import database_layer

app = Flask(__name__)

APPLICATION_NAME = "Family Tree Application"


@app.route("/")
@app.route("/index.html")
def show_tree():
    db = database_layer.DatabaseConnection()
    return render_template('index.html', persons=db.get_all_persons(), relations=db.get_all_relationships())


@app.route("/new_person.html", methods=['GET', 'POST'])
def add_new_person():
    if request.method == 'POST':
        db = database_layer.DatabaseConnection()
        db.add_person(person_name=request.form['name'],
                      year_of_birth=request.form['born'])
        return redirect(url_for('show_tree'))
    else:
        return render_template('new_person.html')


@app.route("/new_relationship.html")
def add_new_relationship():
    pass


if __name__ == "__main__":
    app.run()
