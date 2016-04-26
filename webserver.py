from flask import Flask, render_template, request, url_for, redirect

from database import database_layer

import json
import random

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
        db.add_relationship(start_id=request.form['start_node'],
                            end_id=request.form['end_node'],
                            relationship_type=request.form['type'])
        return redirect(url_for('show_tree'))
    else:
        return render_template('new_relationship.html', persons=db.get_all_persons())


@app.route("/graph.html", methods=['GET'])
def show_graph():
    db = database_layer.DatabaseConnection()
    relationships = db.get_all_relationships()
    nodes = db.get_all_persons()
    family_tree_json = dict()
    family_tree_json['edges'] = []
    family_tree_json['nodes'] = []
    size = 2
    x = 1
    y = 1
    color = '#666'
    for relationship in relationships:
        relationship_as_dict = dict()
        relationship_as_dict['id'] = relationship.relationship_id
        relationship_as_dict['source'] = str(relationship.start_node.uri).rsplit('/', 1)[-1]
        relationship_as_dict['target'] = str(relationship.end_node.uri).rsplit('/', 1)[-1]
        relationship_as_dict['size'] = size
        family_tree_json['edges'].append(relationship_as_dict)
    for node in nodes:
        node_as_dict = dict()
        node_as_dict['id'] = node.id
        node_as_dict['label'] = node.name
        node_as_dict['size'] = size
        node_as_dict['color'] = color
        random_coefficient = random.random()
        node_as_dict['x'] = x * random_coefficient - random_coefficient * 10
        x += 1
        node_as_dict['y'] = y * random_coefficient + random_coefficient * 10
        y += 1
        family_tree_json['nodes'].append(node_as_dict)
    print family_tree_json
    family_tree_json_dump = json.dumps(family_tree_json)
    return render_template('graph.html', json_to_display=family_tree_json_dump)


if __name__ == "__main__":
    app.run()


