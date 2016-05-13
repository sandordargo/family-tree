import random
from database import database_layer


class HorizontalSorter(object):
    def __init__(self, levels_on_tree, edges):
        self.db = database_layer.DatabaseConnection()
        self.person_level_tree = levels_on_tree
        self.edges = edges
        self.person_horizontal_position_dict = dict()
        self.position_person_dict = dict()
        self.level_person_dict = self.build_level_person_dict()

    def get_person_horizontal_position_dict(self):
        return self.person_horizontal_position_dict

    def sort_horizontal(self):
        # TODO add tests
        # TODO every children should be under his parents or spouse's parents
        # TODO siblings next to each other (even)
        # TODO make sure that between siblings there are nobody else only spouses
        self.person_horizontal_position_dict = self.assign_random_x_positions()
        self.position_person_dict = self.build_position_person_dict()
        self.put_children_under_parents()
        self.move_married_people_next_to_each_other()
        self.put_children_under_parents()

        print(self.person_horizontal_position_dict)

    def move_married_people_next_to_each_other(self):
        for inner_level in self.level_person_dict:
            for relationship in self.edges:
                if relationship['type'] == 'MARRIED' and relationship['source'] in self.level_person_dict[
                    inner_level] and \
                                relationship['target'] in self.level_person_dict[inner_level]:
                    new_position = self.person_horizontal_position_dict[relationship['source']] + 1
                    self.move_person_on_horizontal_axis_to_position_spouse(relationship['target'], new_position)

    def put_children_under_parents(self):
        # TODO a child can go into two children of someone else. it should not happen
        # proposal: the new child should move and his parents!
        for level in self.level_person_dict:
            print('level: {}.'.format(level))
            for person in self.level_person_dict[level]:
                # if not self.db.is_married(person):
                print(person)
                if self.db.get_parents_of_person(person):
                    print('{} has parent '.format(person))
                    parents = self.db.get_parents_of_person(person)
                    new_position = 0
                    for parent in parents:
                        print('{} is parent of {}'.format(parent, person))
                        new_position = self.person_horizontal_position_dict[parent]
                    self.move_person_on_horizontal_axis_to_position(person, new_position)

    def move_person_on_horizontal_axis_to_position_spouse(self, person_id, new_position):
        """
        Moves a person to the given position.
        If there is already someone at that position, he will be moved with the same number of positions.
        """
        old_position = self.person_horizontal_position_dict[person_id]
        change = new_position - old_position
        self.move(person_id, change)

    def move_person_on_horizontal_axis_to_position(self, person_id, new_position):
        """
        Moves a person to the given position.
        If there is already someone at that position, he will be moved with the same number of positions.
        """
        old_position = self.person_horizontal_position_dict[person_id]
        change = new_position - old_position
        self.move_person_on_horizontal_axis(person_id, change)

    def move(self, person_id, change):
        if change == 0:
            return
        if change < 0:
            print('=============')
            print('negative move')
            print(person_id)
            print(change)
            print('=============')
        if self.person_horizontal_position_dict[person_id] + change in self.position_person_dict and \
                        len(self.position_person_dict[self.person_horizontal_position_dict[person_id] + change]) > 0:
            for person in self.position_person_dict[self.person_horizontal_position_dict[person_id] + change]:
                if self.get_level_of_person(person_id) == self.get_level_of_person(person):
                    self.move_person_on_horizontal_axis(person, change)

        old_position = self.person_horizontal_position_dict[person_id]
        new_position = self.person_horizontal_position_dict[person_id] + change
        self.person_horizontal_position_dict[person_id] = new_position
        self.position_person_dict[old_position].remove(person_id)
        if new_position not in self.position_person_dict:
            self.position_person_dict[new_position] = list()
        self.position_person_dict[new_position].append(person_id)

    def move_person_on_horizontal_axis(self, person_id, change):
        """
        Moves a person by the given change in position.
        If there is already someone at that position, he will be moved with the same number of positions.
        """
        self.move(person_id, change)
        self.move_spouse_if_any(person_id, change)
        self.move_children_if_any(person_id, change)

    def move_spouse_if_any(self, person_id, change):
        if self.db.is_married(person_id):
            print('married')
            for spouse in self.db.get_spouses_of_person(person_id):
                self.move(spouse, change)
                #self.move_children_if_any(spouse, change)

    def move_children_if_any(self, person_id, change):
        if self.db.get_children_of_person(person_id):
            for child in self.db.get_children_of_person(person_id):
                print(child)
                self.move_person_on_horizontal_axis(child, change)

    def build_position_person_dict(self):
        """
        Returns a dictionary of horizontal positions (key) and lists of perons (value) in the given position
        """
        position_person_dict = dict()
        for level in self.level_person_dict:
            for person in self.level_person_dict[level]:
                if self.person_horizontal_position_dict[person] not in position_person_dict:
                    position_person_dict[self.person_horizontal_position_dict[person]] = list()
                position_person_dict[self.person_horizontal_position_dict[person]].append(person)
        return position_person_dict

    def assign_random_x_positions(self):
        """
        Returns a dictionary of persons (key) and randomly assigned horizontal positions (values)
        Although the values are randomly assigned, they range from 0 to twice the number of the persons on a given level
         and each value most be even and cannot appear more than once
        """
        person_horizontal_position_dict = dict()
        for level in self.level_person_dict:
            number_of_persons = len(self.level_person_dict[level])
            random_positions = random.sample(range(0, 2 * number_of_persons + 1, 2), number_of_persons)
            for person in self.level_person_dict[level]:
                person_horizontal_position_dict[person] = random_positions.pop()
        return person_horizontal_position_dict

    def build_level_person_dict(self):
        """
        Based on levels_on_tree dictionary (key: person, value: its level on tree) builds another dict
         where the keys are the levels and values are the person sitting on a given level
        """
        level_person_dict = dict()
        for person in self.person_level_tree:
            if self.person_level_tree[person] not in level_person_dict:
                level_person_dict[self.person_level_tree[person]] = list()
            level_person_dict[self.person_level_tree[person]].append(person)
        return level_person_dict

    def are_there_persons_at_the_same_positions(self, position_persons_dict):
        """
        Checks whether there are persons at the same position on the same level
        Returns True if there are, otherwise False
        """
        return self.get_position_with_multiple_persons(position_persons_dict) is not None

    def get_level_of_person(self, person):
        """
        Returns the level of the given person
        """
        return self.person_level_tree[person]

    def get_position_with_multiple_persons(self, position_persons_dict):
        """
        Returns persons who are on the same level and at the same position
        Returns the first such persons
        """
        for position in position_persons_dict:
            if len(position_persons_dict[position]) > 1:
                level_person_dict = dict()
                for person in position_persons_dict[position]:
                    level = self.get_level_of_person(person)
                    if level not in level_person_dict:
                        level_person_dict[level] = list()
                    level_person_dict[level].append(person)
                for level in level_person_dict:
                    if len(level_person_dict[level]) > 1:
                        return level_person_dict[level]
        return None
