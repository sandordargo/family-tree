from flask import Flask, render_template

from database import database_layer

app = Flask(__name__)

APPLICATION_NAME = "Family Tree Application"


@app.route("/")
@app.route("/index.html")
def show_tree():
    db = database_layer.DatabaseConnection()
    return render_template('index.html', persons=db.get_all_persons(), relations=db.get_all_relationships())


@app.route("/new_person.html")
def add_new_person():
    pass


@app.route("/new_relationship.html")
def add_new_relationship():
    pass


if __name__ == "__main__":
    app.run()
