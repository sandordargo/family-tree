from database import database_layer
import random


class FamilyTree(object):

    def __init__(self):
        self.db = database_layer.DatabaseConnection()
        self.nodes = self.read_persons()
        self.edges = self.read_relationships()
        self.levels_on_tree = self.build_levels_dictionary()
        self.person_horizontal_position_dict = dict()
        self.position_person_dict = dict()
        self.level_person_dict = self.build_level_person_dict()
        self.sort_horizontal()
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
            node['y'] = self.levels_on_tree[node['id']] * 2
            node['x'] = self.person_horizontal_position_dict[node['id']]
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
        # TODO levels should start from zero
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
        self.assign_random_x_positions()
        print(self.person_horizontal_position_dict)
        self.put_children_under_parents()
        print(self.person_horizontal_position_dict)
        self.build_position_person_dict()
        self.move_persons_from_same_level_and_position()
        print('before married move')
        print(self.person_horizontal_position_dict)
        self.move_married_people_next_to_each_other()

        # TODO add tests
        # TODO every children should be under his parents or spouse's parents
        # TODO siblings next to each other (even)
        # TODO maintain position_person_dict
        print('before return')
        print(self.person_horizontal_position_dict)

        self.move_persons_from_same_level_and_position()

    # self.person_horizontal_position_dict = dict()
    # self.position_person_dict = dict()
    # self.level_person_dict = self.build_level_person_dict()

    def move_person_on_horizontal_axis_to_position(self, person_id, new_position):
        old_position = self.person_horizontal_position_dict[person_id]
        change = new_position - old_position
        self.move_person_on_horizontal_axis(person_id, change)

    def move_person_on_horizontal_axis(self, person_id, change):
        if str(self.person_horizontal_position_dict[person_id] + change) in self.position_person_dict:
            for person in self.position_person_dict[self.person_horizontal_position_dict[person_id]]:
                self.move_person_on_horizontal_axis(person, change)
            old_position = self.person_horizontal_position_dict[person_id]
            new_position = self.person_horizontal_position_dict[person_id] + change
            self.person_horizontal_position_dict[person_id] = new_position
            self.position_person_dict[old_position].remove(person_id)
            if new_position not in self.position_person_dict:
                self.position_person_dict[new_position] = list()
            self.position_person_dict[new_position].append(person_id)
        else:
            old_position = self.person_horizontal_position_dict[person_id]
            new_position = self.person_horizontal_position_dict[person_id] + change
            self.person_horizontal_position_dict[person_id] = new_position
            self.position_person_dict[old_position].remove(person_id)
            if new_position not in self.position_person_dict:
                self.position_person_dict[new_position] = list()
            self.position_person_dict[new_position].append(person_id)

    # before
    # married
    # move
    # {'11': 4, '10': 3, '1': 3, '0': -2, '3': 4, '2': 0, '5': 3, '4': 3, '7': 2, '9': 3}
    # brefore
    # last
    # mixture
    # {'11': 4, '10': 3, '1': 3, '0': -2, '3': 4, '2': 4, '5': 3, '4': 5, '7': 5, '9': 3}
    # before
    # return
    # {'11': 4, '10': 3, '1': 3, '0': -6, '3': 4, '2': 2, '5': 3, '4': 5, '7': -1, '9': 3}
    # Lilla +4, Mama +3, anyu +2
    def move_married_people_next_to_each_other(self):
        for inner_level in self.level_person_dict:
            for relationship in self.edges:
                if relationship['type'] == 'MARRIED' and relationship['source'] in self.level_person_dict[
                    inner_level] and \
                                relationship['target'] in self.level_person_dict[inner_level]:
                    old_position = self.person_horizontal_position_dict[relationship['target']]
                    new_position = self.person_horizontal_position_dict[relationship['source']] + 1
                    self.move_person_on_horizontal_axis_to_position(relationship['target'], new_position)
                    # self.person_horizontal_position_dict[relationship['target']] = new_position
                    # self.position_person_dict[old_position].remove(relationship['target'])
                    # if new_position in self.position_person_dict:
                    #     self.position_person_dict[new_position].append(relationship['target'])
                    # else:
                    #     self.position_person_dict[new_position] = list()
                    #     self.position_person_dict[new_position].append(relationship['target'])


    # TODO make it recursive, if there is someone there, shift her
    # TODO move based on level
    def move_persons_from_same_level_and_position(self):
        while self.is_there_key_with_multiple_values(self.position_person_dict):
            position_with_multiple_persons = self.get_position_with_multiple_persons(self.position_person_dict)
            i = 0
            for person in position_with_multiple_persons:
                print('persons with same position: {}'.format(position_with_multiple_persons))
                self.move_person_on_horizontal_axis(person, -1*i*2)
                #self.person_horizontal_position_dict[person] -= i*2
                i += 1
        #self.build_position_person_dict()

    @staticmethod
    def get_position_with_multiple_persons(dict_to_check):
        for key in dict_to_check:
            if len(dict_to_check[key]) > 1:
                return dict_to_check[key]
        raise

    def build_position_person_dict(self):
        for level in self.level_person_dict:
            for person in self.level_person_dict[level]:
                if self.person_horizontal_position_dict[person] in self.position_person_dict:
                    self.position_person_dict[self.person_horizontal_position_dict[person]].append(person)
                else:
                    self.position_person_dict[self.person_horizontal_position_dict[person]] = list()
                    self.position_person_dict[self.person_horizontal_position_dict[person]].append(person)

    def put_children_under_parents(self):
        for level in self.level_person_dict:
            for person in self.level_person_dict[level]:
                # if not self.db.is_married(person):
                if self.db.get_parents_of_person(person):
                    parents = self.db.get_parents_of_person(person)
                    new_position = 0
                    for parent in parents:
                        #new_position += self.person_horizontal_position_dict[parent]
                        new_position = self.person_horizontal_position_dict[parent]
                    #new_position /= len(parents)
                    self.person_horizontal_position_dict[person] = new_position
                    #self.move_person_on_horizontal_axis_to_position(person, new_position)

    def assign_random_x_positions(self):
        for level in self.level_person_dict:
            for person in self.level_person_dict[level]:
                # TODO make sure uniqueness
                random_coefficient = random.randrange(0, 2 * len(self.level_person_dict[level]) + 1, 2)
                self.person_horizontal_position_dict[person] = random_coefficient

    def build_level_person_dict(self):
        level_person_dict = dict()
        for person in self.levels_on_tree:
            if self.levels_on_tree[person] not in level_person_dict:
                level_person_dict[self.levels_on_tree[person]] = list()
                level_person_dict[self.levels_on_tree[person]].append(person)
            else:
                level_person_dict[self.levels_on_tree[person]].append(person)
        return level_person_dict

    @staticmethod
    def is_there_key_with_multiple_values(dict_to_check):
        for key in dict_to_check:
            if len(dict_to_check[key]) > 1:
                return True
        return False
