import random
from database import database_layer
import person_node


class HorizontalSorter(object):
    def __init__(self, levels_on_tree, edges, nodes):
        self.db = database_layer.DatabaseConnection()
        self.person_level_tree = levels_on_tree
        self.edges = edges
        self.person_dictionary = nodes
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
        self.person_horizontal_position_dict = self.assign_random_x_positions()  # Should be fine
        self.position_person_dict = self.build_position_person_dict()  # Should be fine
        self.put_siblings_next_each_other_bottom_up()  # Should be fine
        self.put_parents_above_their_children()
        self.move_married_people_next_to_each_other()
        # TODO flat repo horizontally
        # TODO make sure, no one is between the siblings, unless a spouse

    def put_siblings_next_each_other_bottom_up(self):
        for level in self.level_person_dict:
            for person in self.level_person_dict[level]:
                siblings_positions = list()
                siblings_positions.append((self.person_dictionary[int(person)].horizontal_position,
                                           self.person_dictionary[int(person)].person_id))
                if self.person_dictionary[int(person)].siblings:
                    for sibling in self.person_dictionary[int(person)].siblings:
                        siblings_positions.append((self.person_dictionary[int(sibling)].horizontal_position,
                                                   self.person_dictionary[int(sibling)].person_id))
                siblings_positions.sort()
                if len(siblings_positions) > 1:
                    for num in range(0, len(siblings_positions)-1):
                        if siblings_positions[num][0] - siblings_positions[num + 1][0] != 2:
                            self.move_person_on_horizontal_axis_to_position(siblings_positions[num + 1][1],
                                                                            siblings_positions[num][0] + 2)

    def move_person_on_horizontal_axis_to_position(self, person_id, new_position):
        """
        Moves a person to the given position.
        If there is already someone at that position, he will be moved with the same number of positions.
        """
        old_position = self.person_dictionary[person_id].horizontal_position
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
        new_position = self.person_horizontal_position_dict[person_id] + change
        if new_position in self.position_person_dict and \
                len(self.position_person_dict[new_position]) > 0:
            for another_person_at_same_position in self.position_person_dict[new_position]:
                if self.get_level_of_person(person_id) == self.get_level_of_person(another_person_at_same_position):
                    self.move_person_on_horizontal_axis(another_person_at_same_position, change)

        old_position = self.person_horizontal_position_dict[person_id]
        self.person_horizontal_position_dict[person_id] = new_position
        self.position_person_dict[old_position].remove(str(person_id))

        if new_position not in self.position_person_dict:
            self.position_person_dict[new_position] = list()
        self.position_person_dict[new_position].append(str(person_id))
        self.person_dictionary[int(person_id)].horizontal_position = new_position

    def move_person_on_horizontal_axis(self, person_id, change):
        """
        Moves a person by the given change in position.
        If there is already someone at that position, he will be moved with the same number of positions.
        """
        self.move(person_id, change)
        # self.move_spouse_if_any(person_id, change)
        # self.move_children_if_any(person_id, change)

    def put_parents_above_their_children(self):
        # TODO average children positions for parents
        # TODO move their siblings with them?
        self.level_person_dict.keys().sort(reverse=True)
        for youngest_level in self.level_person_dict:
            for person in self.level_person_dict[youngest_level]:
                if self.person_dictionary[int(person)].parents:
                    parent_coeff = 0
                    for parent in self.person_dictionary[int(person)].parents:
                        self.move_person_on_horizontal_axis_to_position(parent,
                                                                        self.person_dictionary[int(person)].
                                                                        horizontal_position + parent_coeff)

                        parent_coeff += 1

    def move_married_people_next_to_each_other(self):
        for inner_level in self.level_person_dict:
            for relationship in self.edges:
                if relationship['type'] == 'MARRIED' and relationship['source'] in self.level_person_dict[
                    inner_level] and \
                                relationship['target'] in self.level_person_dict[inner_level]:
                    if abs(self.person_horizontal_position_dict[relationship['source']] -
                           self.person_horizontal_position_dict[relationship['target']]) != 1:
                        new_position = self.person_horizontal_position_dict[relationship['source']] + 1
                        self.move_person_on_horizontal_axis_to_position_spouse(relationship['target'], new_position)

    def put_children_under_parents(self):
        # TODO a child can go into two children of someone else. it should not happen
        # proposal: the new child should move and his parents!
        for level in self.level_person_dict:
            for person in self.level_person_dict[level]:
                if self.db.get_parents_of_person(person):
                    parents = self.db.get_parents_of_person(person)
                    new_position = 0
                    for parent in parents:
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
        old_position = self.person_horizontal_position_dict[str(person_id)]
        change = new_position - old_position
        self.move_person_on_horizontal_axis(str(person_id), change)

    def move_spouse_if_any(self, person_id, change):
        if self.db.is_married(person_id):
            for spouse in self.db.get_spouses_of_person(person_id):
                self.move(spouse, change)

    def move_children_if_any(self, person_id, change):
        if self.db.get_children_of_person(person_id):
            for child in self.db.get_children_of_person(person_id):
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
                random_position = random_positions.pop()
                person_horizontal_position_dict[person] = random_position
                self.person_dictionary[int(person)].horizontal_position = random_position
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

    def get_level_of_person(self, person):
        """
        Returns the level of the given person
        """
        return self.person_level_tree[person]
