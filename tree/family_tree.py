from database import database_layer
from tree import vertical_sorter, horizontal_sorter
from tree import person_node


class FamilyTree(object):

    def __init__(self):
        self.db = database_layer.DatabaseConnection()
        self.nodes = self.read_persons()
        self.edges = self.read_relationships()
        my_vertical_sorter = vertical_sorter.VerticalSorter(self.edges)
        self.levels_on_tree = my_vertical_sorter.get_levels_dictionary()
        my_horizontal_sorter = horizontal_sorter.HorizontalSorter(self.levels_on_tree, self.edges, self.nodes)
        my_horizontal_sorter.sort_horizontal()
        self.person_horizontal_position_dict = my_horizontal_sorter.get_person_horizontal_position_dict()
        self.size = 2
        self.color = '#666'

    def read_persons(self):
        persons = self.db.get_all_persons()
        person_nodes = dict()
        for node in persons:
            new_person_node = person_node.PersonNode()
            new_person_node.person_id = node.id
            new_person_node.label = node.name
            new_person_node.children = self.db.get_child_generations_for_person(node.id) # TODO check function call? get_children_of_person
            new_person_node.parents = self.db.get_parents_of_person(node.id)
            if new_person_node.parents:
                if self.db.get_children_of_person(new_person_node.parents[0]):
                    new_person_node.siblings = self.db.get_children_of_person(new_person_node.parents[0])
            person_nodes[int(node.id)] = new_person_node
        return person_nodes

    def read_relationships(self):
        relationships = self.db.get_all_relationships()
        edges = []
        for relationship in relationships:
            edges.append(relationship.get_as_json())
        return edges

    #TODO rewrite
    def get_tree_as_json(self):
        family_tree_json = dict()
        family_tree_json['edges'] = self.edges
        family_tree_json['nodes'] = list()
        for node in self.nodes:
            node_as_json =  self.nodes[node].get_as_json()
            node_as_json['size'] = self.size
            node_as_json['color'] = self.color
            if str(node) in self.levels_on_tree:
                node_as_json['y'] = self.levels_on_tree[str(node)]
            elif self.levels_on_tree: 
                node_as_json['y'] = max(self.levels_on_tree)
            
            family_tree_json['nodes'].append(node_as_json)
            #TODO what to do with edge?
            #edge['size'] = self.size
        return family_tree_json

