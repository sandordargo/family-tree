from flask import Flask, render_template, request, url_for, redirect

from database import database_layer
from database import node

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


@app.route("/persons/<int:person_id>/delete/", methods=['GET', 'POST'])
def delete_person(person_id):
    if request.method == 'POST':
        db = database_layer.DatabaseConnection()
        db.remove_person(person_id)
        return redirect(url_for('show_tree'))
    else:
        return render_template('delete_person.html', person_id=person_id)


@app.route('/persons/<int:person_id>/edit/', methods=['GET', 'POST'])
def edit_person(person_id):
    db = database_layer.DatabaseConnection()
    if request.method == 'POST':
        db.update_person(person_id=person_id,
                         person_name=request.form['name'],
                         year_of_birth=request.form['year_of_birth'])
        return redirect(url_for('show_tree'))
    else:
        return render_template('edit_person.html', person=db.get_person(person_id))


@app.route("/relationships/<int:relationship_id>/delete/", methods=['GET', 'POST'])
def delete_relationship(relationship_id):
    if request.method == 'POST':
        db = database_layer.DatabaseConnection()
        db.remove_relationship(relationship_id)
        return redirect(url_for('show_tree'))
    else:
        return render_template('delete_relationship.html', relationship_id=relationship_id)


@app.route('/relationships/<int:relationship_id>/edit/', methods=['GET', 'POST'])
def edit_relationship(relationship_id):
    db = database_layer.DatabaseConnection()
    if request.method == 'POST':
        return redirect(url_for('show_tree'))
    else:
        print(str(db.get_relationship(relationship_id).start_node.uri).rsplit('/', 1)[-1])
        return render_template('edit_relationship.html',
                               persons=db.get_all_persons(),
                               relationship=db.get_relationship(relationship_id),
                               start_node_id=str(db.get_relationship(relationship_id).start_node.uri).rsplit('/', 1)[-1],
                               end_node_id=str(db.get_relationship(relationship_id).end_node.uri).rsplit('/', 1)[-1])


@app.route("/new_relationship.html", methods=['GET', 'POST'])
def add_new_relationship():
    db = database_layer.DatabaseConnection()
    if request.method == 'POST':
        # print(request.form['start_node'])
        # print(type(request.form['start_node']))
        # print(type(request.form['start_node'].id))
        # print(node.Node(request.form['start_node']).id)
        # print(request.form['end_node'].id)
        # print(request.form['type'])
        db.add_relationship(start_id=request.form['start_node'],
                            end_id=request.form['end_node'],
                            relationship_type=request.form['type'])
        return redirect(url_for('show_tree'))
    else:
        return render_template('new_relationship.html', persons=db.get_all_persons())


if __name__ == "__main__":
    app.run()
