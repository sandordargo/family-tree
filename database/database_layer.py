from __future__ import print_function

from py2neo import Graph, Node, Relationship

from database import node


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
        self.connection.create(Node("Person", name=person_name, birth=year_of_birth))

    def add_relationship(self, start_id, end_id, relationship_type):
        start_node = self.connection.find_one("Person", property_key='uid', property_value=start_id)
        end_node = self.connection.find_one("Person", property_key='uid', property_value=end_id)
        self.connection.create = Relationship(start_node, relationship_type, end_node)

    def remove_relationship(self):
        pass

    def remove_person(self):
        pass

    def add_person_property(self):
        pass

    def get_all_persons(self):
        nodes = list()
        for n in self.connection.cypher.stream("START z=node(*) RETURN z"):
            new_node = node.Node(n[0].properties["name"], n[0].properties["born"])
            nodes.append(new_node)
        return nodes

    def get_all_relationships(self):
        relations = list()
        for relation in self.connection.cypher.stream("Match (a)-[r]->(b) return r"):
            relations.append(relation[0])
        return relations


# # ...
# dc = DatabaseConnection()
# dc.add_person("CHMARA OdOn", 1907)
# dc.add_relationship("CHMARAMARIA1939", "CHMARAODON1907", "CHILD_OF")
