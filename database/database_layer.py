from __future__ import print_function

from py2neo import Graph, Node, Relationship

from database import node, relationship


#
# uid should be an id which identifies uniquely a node or a relationship
# uid for nodes: <NAME><FIRST NAME><YEAR OF BIRTH>: DARGODALMA2016
# uid for relationships: <TYPE><START NAME FIRST TWO LETTERS><START FIRST NAME FIRST TWO LETTERS><YEAR OF BIRTH>
# <END NAME FIRST TWO LETTERS><END FIRST NAME FIRST TWO LETTERS><YEAR OF BIRTH>: CODADA2016JULI1986
# CO = CHILD OF
#

class DatabaseConnection(object):

    def __init__(self):
        self.connection = Graph()
        self.uri = self.connection.uri

    def add_person(self, person_name, year_of_birth):
        print('person_name: {}, year of birth {}'.format(person_name, year_of_birth))
        self.connection.create(Node("Person", name=person_name, born=year_of_birth))

    def add_relationship(self, start_id, end_id, relationship_type):
        start_node = self.connection.node(start_id)
        end_node = self.connection.node(end_id)
        self.connection.create(Relationship(start_node, 'CHILD_OF', end_node))

    def remove_relationship(self, relationship_id):
        self.connection.cypher.stream("MATCH n - [r] - () WHERE ID(r) = {} DELETE r".format(relationship_id))

    def remove_person(self, person_id):
        self.connection.cypher.stream("MATCH(p:Person) where ID(p) = {} OPTIONAL MATCH(p) - [r] - () DELETE r, p".format(person_id))

    def add_person_property(self):
        pass

    def get_all_persons(self):
        nodes = list()
        for n in self.connection.cypher.stream("START z=node(*) RETURN z"):
            new_node = node.Node(str(n[0].uri).rsplit('/', 1)[-1], n[0].properties["name"], n[0].properties["born"])
            nodes.append(new_node)
        return nodes

    def get_all_relationships(self):
        relations = list()
        for relation in self.connection.cypher.stream("Match (a)-[r]->(b) return r"):
            new_relationship = relationship.Relationship(relationship_id=str(relation[0].uri).rsplit('/', 1)[-1],
                                                         start_node=relation[0].start_node,
                                                         end_node=relation[0].end_node,
                                                         relationship_type=relation[0].type,
                                                         properties=relation[0].properties)
            relations.append(new_relationship)
        return relations


# # ...
# dc = DatabaseConnection()
# dc.add_person("CHMARA OdOn", 1907)
# dc.add_relationship("CHMARAMARIA1939", "CHMARAODON1907", "CHILD_OF")
