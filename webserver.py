import json

from flask import Flask, render_template, request, url_for, redirect, flash, make_response

from database import database_layer
from tree import family_tree

app = Flask(__name__)
app.secret_key = 'some_secret'
APPLICATION_NAME = "Family Tree Application"


@app.route("/")
@app.route("/index.html")
def show_tree():
    db = database_layer.DatabaseConnection()
    persons_relationship_map = dict()
    for person in db.get_all_persons():
        persons_relationship_map[person] = db.get_relationships_of_a_node(person.id)

    my_family_tree = family_tree.FamilyTree()
    print(my_family_tree.get_tree_as_json())
    family_tree_json_dump = json.dumps(my_family_tree.get_tree_as_json())

    return render_template('index.html', persons_with_relationships=persons_relationship_map, json_to_display=family_tree_json_dump)


@app.route("/new_person.html", methods=['GET', 'POST'])
def add_new_person():
    if request.method == 'POST':
        db = database_layer.DatabaseConnection()
        db.add_person(person_name=request.form['name'],
                      year_of_birth=request.form['born'])
        flash('{} has been added to the family tree'.format(request.form['name']))
        return redirect(url_for('show_tree'))
    else:
        return render_template('new_person.html')


@app.route("/persons/<int:person_id>/delete/", methods=['GET', 'POST'])
def delete_person(person_id):
    db = database_layer.DatabaseConnection()
    person = db.get_person(person_id)
    if request.method == 'POST':
        db.remove_person(person_id)
        flash('Person with {} has been deleted from the family tree'.format(person.name))
        return redirect(url_for('show_tree'))
    else:
        return render_template('delete_person.html', person=person)


@app.route('/persons/<int:person_id>/edit/', methods=['GET', 'POST'])
def edit_person(person_id):
    db = database_layer.DatabaseConnection()
    if request.method == 'POST':
        import re
        properties = {}
        for element in request.form:
            new_property = re.search('propertyname(\d+)', element)
            if new_property:
                properties[request.form[element]] = request.form['propertyvalue{}'.format(new_property.group(1))]
            elif element.startswith('propertyvalue'):
                pass
            else:
                properties[element] = request.form[element]
        db.update_person(person_id=person_id,
                         person_properties=properties)
        flash('{} has been edited'.format(request.form['name']))
        return redirect(url_for('show_tree'))
    else:
        return render_template('edit_person.html', person=db.get_person(person_id))


@app.route("/relationships/<int:relationship_id>/delete/", methods=['GET', 'POST'])
def delete_relationship(relationship_id):
    db = database_layer.DatabaseConnection()
    if request.method == 'POST':
        start_name, end_name = get_start_name_end_name(relationship_id)
        db.remove_relationship(relationship_id)
        flash('Relationship between {} and {} has been deleted'.format(start_name, end_name))
        return redirect(url_for('show_tree'))
    else:
        relationship = db.get_relationship(relationship_id)
        return render_template('delete_relationship.html', relationship=relationship)


@app.route('/relationships/<int:relationship_id>/edit/', methods=['GET', 'POST'])
def edit_relationship(relationship_id):
    db = database_layer.DatabaseConnection()
    if request.method == 'POST':
        import re
        properties = {}
        for element in request.form:
            new_property = re.search('propertyname(\d+)', element)
            if new_property:
                properties[request.form[element]] = request.form['propertyvalue{}'.format(new_property.group(1))]
            elif element.startswith('propertyvalue'):
                pass
            else:
                properties[element] = request.form[element]
        db.update_relationship(relationship_id=relationship_id,
                               relationship_properties=properties)
        start_name, end_name = get_start_name_end_name(relationship_id)
        flash('Relationship between {} and {} has been edited'.format(start_name, end_name))
        return redirect(url_for('show_tree'))
    else:
        return render_template('edit_relationship.html',
                               persons=db.get_all_persons(),
                               relationship=db.get_relationship(relationship_id),
                               start_node_id=str(db.get_relationship(relationship_id).start_node.uri).rsplit('/', 1)[-1],
                               end_node_id=str(db.get_relationship(relationship_id).end_node.uri).rsplit('/', 1)[-1])


@app.route("/new_relationship.html", methods=['GET', 'POST'])
def add_new_relationship():
    db = database_layer.DatabaseConnection()
    if request.method == 'POST':
        db.add_relationship(start_id=request.form['start_node'],
                            end_id=request.form['end_node'],
                            relationship_type=request.form['type'])
        start_name = db.get_person(request.form['start_node']).name
        end_name = db.get_person(request.form['end_node']).name
        flash('Relationship between {} and {} has been added'.format(start_name, end_name))
        return redirect(url_for('show_tree'))
    else:
        return render_template('new_relationship.html', persons=db.get_all_persons())


@app.route("/graph.html", methods=['GET'])
def show_graph():
    my_family_tree = family_tree.FamilyTree()
    print(my_family_tree.get_tree_as_json())
    family_tree_json_dump = json.dumps(my_family_tree.get_tree_as_json())
    return render_template('graph.html', json_to_display=family_tree_json_dump)


def get_start_name_end_name(relationship_id):
    db = database_layer.DatabaseConnection()
    relationship = db.get_relationship(relationship_id)
    start_name = db.get_person(relationship.get_start_id()).name
    end_name = db.get_person(relationship.get_start_id()).name
    return start_name, end_name

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5000)


