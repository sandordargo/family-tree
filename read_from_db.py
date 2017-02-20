from __future__ import print_function
from py2neo import Graph, Node, Relationship

graph_db = Graph()

person = Node("Person", name="JUHASZ Lilla Linda")

for record in graph_db.cypher.execute("Match (n) return n"):
    print(record)

new_person = Node("Person", name="JUHASZ Peter", born=1930)
print("exists: " + str(list(graph_db.find("Person", property_key="name", property_value="JUHASZ Peter"))))

new_person.bind(graph_db.uri)
print("exists: " + str(new_person.exists))

father = graph_db.find_one("Person", property_key='name', property_value="JUHASZ Peter")

child = graph_db.find_one("Person", property_key='name', property_value="JUHASZ Lilla Linda")
child_of_rel = "CHILD_OF"
father_daughter_relationship = Relationship(child, child_of_rel, father)
graph_db.create(father_daughter_relationship)

