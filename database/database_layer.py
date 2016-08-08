from __future__ import print_function

from py2neo import Graph, Node, Relationship

from database import person, relationship


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

    def add_person(self, person_name, year_of_birth):
        print('person_name: {}, year of birth {}'.format(person_name, year_of_birth))
        self.connection.create(Node("Person", name=person_name, born=year_of_birth))

    def add_relationship(self, start_id, end_id, relationship_type):
        start_node = self.connection.node(start_id)
        end_node = self.connection.node(end_id)
        self.connection.create(Relationship(start_node, relationship_type, end_node))

    def remove_relationship(self, relationship_id):
        self.connection.cypher.stream("MATCH n - [r] - () WHERE ID(r) = {} DELETE r".format(relationship_id))

    def remove_person(self, person_id):
        self.connection.cypher.stream("MATCH(p:Person) where ID(p) = {} OPTIONAL MATCH(p) - [r] - () DELETE r, p".format(person_id))

    def add_person_property(self):
        pass

    def update_person(self, person_id, person_properties):
        node_to_update = self.get_neo4j_person(person_id)
        keys = node_to_update.properties.keys()
        for key in keys:
            del node_to_update.properties[key]
        if person_properties:
            for key in person_properties:
                node_to_update.properties[key] = person_properties[key]
        node_to_update.push()

    def update_relationship(self, relationship_id, relationship_properties):
        relationship_to_update = self.get_neo4j_relationship(relationship_id)
        keys = relationship_to_update.properties.keys()
        for key in keys:
            del relationship_to_update.properties[key]
        if relationship_properties:
            for key in relationship_properties:
                relationship_to_update.properties[key] = relationship_properties[key]
        relationship_to_update.push()

    def get_neo4j_person(self, person_id):
        single_node_list = self.connection.cypher.stream("MATCH(p:Person) where ID(p) = {} RETURN p".format(person_id))
        for a_node in single_node_list:
            return a_node[0]

    def get_person(self, person_id):
        neo_node = self.get_neo4j_person(person_id)
        return person.Person(str(neo_node.uri).rsplit('/', 1)[-1],
                             neo_node.properties["name"],
                             neo_node.properties["born"],
                             neo_node.properties)

    def get_all_persons(self):
        nodes = list()
        for n in self.connection.cypher.stream("START z=node(*) RETURN z"):
            new_node = person.Person(str(n[0].uri).rsplit('/', 1)[-1], n[0].properties["name"], n[0].properties["born"], n[0].properties)
            nodes.append(new_node)
        return nodes

    def get_relationship(self, relationship_id):
        neo_relationship = self.get_neo4j_relationship(relationship_id)
        relationship_to_return = relationship.Relationship(relationship_id=str(neo_relationship.uri).rsplit('/', 1)[-1],
                                         start_node=neo_relationship.start_node,
                                         end_node=neo_relationship.end_node,
                                         relationship_type=neo_relationship.type,
                                         properties=neo_relationship.properties)
        return relationship_to_return

    def get_neo4j_relationship(self, relationship_id):
        single_relationship_list = self.connection.cypher.stream("MATCH n - [r] - () WHERE ID(r) = {} RETURN r"
                                                                 .format(relationship_id))
        for a_relation in single_relationship_list:
            return a_relation[0]

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

    def get_child_generations_for_person(self, person_id):
        return_value = next(self.connection.cypher.
                    stream("MATCH p=(r:Person)<-[:CHILD_OF*1..20]-(x) WHERE ID(r) = {} RETURN max(length(p))".
                           format(person_id)))[0]
        return_value = return_value if return_value else 0
        return return_value

    def get_parent_generations_for_person(self, person_id):
        return_value = next(self.connection.cypher.
                    stream("MATCH p=(r:Person)-[:CHILD_OF*1..20]->(x) WHERE ID(r) = {} RETURN max(length(p))".
                           format(person_id)))[0]

        return_value = return_value if return_value else 0
        return return_value

    def is_descendant_of(self, descendant_person_id, ancestor_person_id):
        path_length = next(self.connection.cypher.
                            stream("MATCH p=(r:Person)-[:CHILD_OF*1..20]->(q:Person) WHERE ID(r) = {} and ID(q) = {}"
                                   "RETURN max(length(p))".
                                   format(descendant_person_id, ancestor_person_id)))[0]
        return True if path_length else False

    def is_married(self, person_id):
        path_length = next(self.connection.cypher.
                           stream("MATCH p=(r:Person)-[:MARRIED]-(x) WHERE ID(r) = {} RETURN max(length(p))".
                                  format(person_id)))[0]
        return True if path_length else False

    def get_spouses_of_person(self, person_id):
        spouse_list = list()
        for spouse in self.connection.cypher.stream("MATCH p=(r:Person)-[:MARRIED]-(q:Person) WHERE ID(r) = {} "
                                                    "RETURN q".format(person_id)):
            spouse_list.append(str(spouse[0].uri).rsplit('/', 1)[-1])
        return spouse_list

    def get_parents_of_person(self, person_id):
        parents_list = list()
        for parent in self.connection.cypher.stream("MATCH p=(r:Person)-[:CHILD_OF]->(q:Person) WHERE ID(r) = {} RETURN q".
                                  format(person_id)):
            parents_list.append(str(parent[0].uri).rsplit('/', 1)[-1])
        return parents_list if parents_list else False

    def get_children_of_person(self, person_id):
        children_list = list()
        for parent in self.connection.cypher.stream(
                "MATCH p=(r:Person)<-[:CHILD_OF]-(q:Person) WHERE ID(r) = {} RETURN q".
                        format(person_id)):
            children_list.append(str(parent[0].uri).rsplit('/', 1)[-1])
        return children_list if children_list else False

    def get_relationships_of_a_node(self, person_id):
        relationship_list = list()
        return_value = next(self.connection.cypher.stream("MATCH p=(person:Person)-[r]-() WHERE ID(person) = {} WITH collect(r) AS rs RETURN rs".format(person_id)))
        print("relationship for person: " + person_id)
        print(return_value)
        start_place = 0
        while True:
            start_place = str(return_value).find("relationship/", start_place) + len("relationship/")
            if start_place == -1 + len("relationship/"):
                print(str(return_value))
                print('not found')
                break
            end_place = str(return_value).find("'", start_place)
            relationship_list.append(self.get_relationship(str(return_value)[start_place:end_place]))
            print('next')
            print(str(return_value)[start_place:end_place])
            start_place = end_place
        print(relationship_list)
        return relationship_list


# dc = DatabaseConnection()
# dc.add_person("CHMARA OdOn", 1907)
# dc.add_relationship("CHMARAMARIA1939", "CHMARAODON1907", "CHILD_OF")
