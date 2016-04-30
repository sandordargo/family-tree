from database import database_layer
import random


class FamilyTree(object):

    def __init__(self):
        self.db = database_layer.DatabaseConnection()
        self.nodes = self.read_persons()
        self.edges = self.read_relationships()
        self.levels_on_tree = self.build_levels_dictionary()
        self.horizontal_sort = self.sort_horizontal()
        self.size = 2
        self.color = '#666'

    def read_persons(self):
        persons = self.db.get_all_persons()
        persons_json = []
        for node in persons:
            node_as_dict = node.get_as_json()
            node_as_dict['id'] = node.id
            node_as_dict['label'] = node.name
            node_as_dict['child_generations'] = self.db.get_child_generations_for_person(node.id)
            node_as_dict['parent_generations'] = self.db.get_parent_generations_for_person(node.id)
            persons_json.append(node_as_dict)
        return persons_json

    def read_relationships(self):
        relationships = self.db.get_all_relationships()
        edges = []
        for relationship in relationships:
            edges.append(relationship.get_as_json())
        return edges

    def get_tree_as_json(self):
        family_tree_json = dict()
        family_tree_json['edges'] = self.edges
        family_tree_json['nodes'] = self.nodes
        for node in family_tree_json['nodes']:
            node['y'] = self.levels_on_tree[node['id']]
            node['x'] = self.horizontal_sort[node['id']]
            node['size'] = self.size
            node['color'] = self.color
        for edge in self.edges:
            edge['size'] = self.size
        return family_tree_json

    def build_levels_dictionary(self):
        person_level_dict = dict()
        visited_relationships_list = list()
        reachable_persons_list = list()

        # get first relationship, put high enough for a worst case scenario, where everyone would go under it
        # target to up or same level based on type of relationship
        first_relationship = self.edges[0]
        person_level_dict[first_relationship['source']] = len(self.edges) + 1
        if first_relationship['type'] == 'CHILD_OF':
            person_level_dict[first_relationship['target']] = person_level_dict[first_relationship['source']] - 1
        if first_relationship['type'] == 'MARRIED':
            person_level_dict[first_relationship['target']] = person_level_dict[first_relationship['source']]
        visited_relationships_list.append(first_relationship['id'])
        reachable_persons_list.append(first_relationship['source'])
        reachable_persons_list.append(first_relationship['target'])

        # look for adjacent relationship until there is any non-visited
        # TODO if not and there is, get any relationship
        while len(visited_relationships_list) < len(self.edges):
            for relationship in self.edges:
                if relationship['id'] not in visited_relationships_list and \
                    (relationship['source'] in reachable_persons_list or
                        relationship['target'] in reachable_persons_list):
                    visited_relationships_list.append(relationship['id'])
                    if relationship['type'] == 'CHILD_OF' and relationship['target'] in reachable_persons_list:
                        person_level_dict[relationship['source']] = person_level_dict[relationship['target']] + 1
                        reachable_persons_list.append(relationship['source'])
                    elif relationship['type'] == 'CHILD_OF' and relationship['source'] in reachable_persons_list:
                        person_level_dict[relationship['target']] = person_level_dict[relationship['source']] - 1
                        reachable_persons_list.append(relationship['target'])
                    elif relationship['type'] == 'MARRIED' and relationship['target'] in reachable_persons_list:
                        person_level_dict[relationship['source']] = person_level_dict[relationship['target']]
                        reachable_persons_list.append(relationship['source'])
                    elif relationship['type'] == 'MARRIED' and relationship['source'] in reachable_persons_list:
                        person_level_dict[relationship['target']] = person_level_dict[relationship['source']]
                        reachable_persons_list.append(relationship['target'])
        return person_level_dict

    def sort_horizontal(self):
        person_horizonal_position_dict = dict()
        x = 1
        for person in self.nodes:
            random_coefficient = random.random()
            person_horizonal_position_dict[person['id']] = x * random_coefficient - random_coefficient * 10
            x += 1
        return person_horizonal_position_dict
        # idea 1 top down
        # oldest generation to middle
        # next generation...

        # idea 2 bottom up
        # start with last generation, supposed to be the largest

        # married people always next to each other
