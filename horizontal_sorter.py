import random
from database import database_layer


class HorizontalSorter(object):

    def __init__(self, levels_on_tree, edges):
        self.db = database_layer.DatabaseConnection()
        self.levels_on_tree = levels_on_tree
        self.edges = edges
        self.person_horizontal_position_dict = dict()
        self.position_person_dict = dict()
        self.level_person_dict = self.build_level_person_dict()
        self.sort_horizontal()

    def get_person_horizontal_position_dict(self):
        return self.person_horizontal_position_dict

    def sort_horizontal(self):
        # TODO add tests
        # TODO every children should be under his parents or spouse's parents
        # TODO siblings next to each other (even)
        # TODO maintain position_person_dict
        self.assign_random_x_positions()
        self.put_children_under_parents()
        self.build_position_person_dict()
        self.move_persons_from_same_level_and_position()
        self.move_married_people_next_to_each_other()

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

    def move_married_people_next_to_each_other(self):
        for inner_level in self.level_person_dict:
            for relationship in self.edges:
                if relationship['type'] == 'MARRIED' and relationship['source'] in self.level_person_dict[
                    inner_level] and \
                                relationship['target'] in self.level_person_dict[inner_level]:
                    new_position = self.person_horizontal_position_dict[relationship['source']] + 1
                    self.move_person_on_horizontal_axis_to_position(relationship['target'], new_position)

    # TODO make it recursive, if there is someone there, shift her
    # TODO move based on level
    def move_persons_from_same_level_and_position(self):
        while self.is_there_key_with_multiple_values(self.position_person_dict):
            position_with_multiple_persons = self.get_position_with_multiple_persons(self.position_person_dict)
            i = 0
            for person in position_with_multiple_persons:
                print('persons with same position: {}'.format(position_with_multiple_persons))
                self.move_person_on_horizontal_axis(person, -1 * i * 2)
                i += 1

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
                        new_position = self.person_horizontal_position_dict[parent]
                    self.person_horizontal_position_dict[person] = new_position

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

