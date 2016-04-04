from __future__ import print_function
from py2neo import Graph, Node, Relationship

import sys

graph_db = Graph()

person = Node("Person", name="JUHASZ Lilla Linda")

for record in graph_db.cypher.execute("Match (n) return n"):
    print(record)

# add new perons
new_person = Node("Person", name="JUHASZ Peter", born=1930)
#graph_db.create(new_person)

print("exists: " + str(list(graph_db.find("Person", property_key="name", property_value="JUHASZ Peter"))))

new_person.bind(graph_db.uri)
print("exists: " + str(new_person.exists))


#father = Node("Person", name="JUHASZ Peter", born=1930)
father = graph_db.find_one("Person", property_key='name', property_value="JUHASZ Peter")
#father.bind(graph_db.uri)

#child = Node("Person", name="JUHASZ Lilla Linda")
child = graph_db.find_one("Person", property_key='name', property_value="JUHASZ Lilla Linda")
#child.bind(graph_db.uri)

# if not(father.exists and child.exists):
#     print('father or child does not exist')
#     sys.exit(2)


#child_of_rel = rel("CHILD_OF")
child_of_rel = "CHILD_OF"
father_daughter_relationship = Relationship(child, child_of_rel, father)
#father_daughter_relationship.bind(graph_db.uri)
graph_db.create(father_daughter_relationship)

