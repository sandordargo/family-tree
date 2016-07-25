import unittest
from tree import horizontal_sorter
from tree import person_node


class TestHorizontalSorter(unittest.TestCase):
    def setUp(self):
        self.edges = {}

    @staticmethod
    def only_even_numbers_in_dict(dict_to_check):
        for key in dict_to_check:
            if dict_to_check[key] % 2 != 0:
                return False
        return True

    @staticmethod
    def build_person_nodes_dict(person_horizontal_position_dict):
        person_nodes = dict()

        for person_id, position in person_horizontal_position_dict.iteritems():
            new_person = person_node.PersonNode()
            new_person.person_id = int(person_id)
            new_person.horizontal_position = position
            person_nodes[int(person_id)] = new_person

        return person_nodes

    @staticmethod
    def assert_list_differences(list_to_check, difference_between_adjacent_elements):
        """
        True if the difference between each adjacent element in the given one
        There should be len(list)-1 of occurences of the given difference if we check all the possible combinationss
        between the passed positions
        This is not efficient for long lists, but we don't expect to have so many siblings
        :param list_to_check: List of horizontal positions
        :param difference_between_adjacent_elements:
        :return: True if assertion is valid, False otherwise
        """
        differences = dict()
        for n in range(0, len(list_to_check), 1):
            for m in range(1, len(list_to_check[n:]), 1):
                diff = abs(list_to_check[n] - list_to_check[n+m])
                if diff in differences:
                    differences[diff] += 1
                else:
                    differences[diff] = 1

        print(differences)
        difference_existance = 1
        for n in range(len(list_to_check) - 1, 0, -1):
            if differences[n * difference_between_adjacent_elements] != difference_existance:
                return False
            difference_existance += 1
        return True

    def test_move(self):
        position_person_dict = {1: ['5', '3'], 2: ['1', '2'], 3: ['4']}
        person_level_dict = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 3}

        person_horizontal_position_dict = {'1': 2, '3': 1, '2': 2, '5': 1, '4': 3}
        person_nodes = self.build_person_nodes_dict(person_horizontal_position_dict)

        sorter = horizontal_sorter.HorizontalSorter(person_level_dict, self.edges, person_nodes)
        sorter.person_horizontal_position_dict = person_horizontal_position_dict
        sorter.position_person_dict = position_person_dict

        sorter.move('4', 2)

        expected_position_person_dict = {1: ['5', '3'], 2: ['1', '2'], 3: [], 5: ['4']}
        expected_person_horizontal_position_dict = {'1': 2, '3': 1, '2': 2, '5': 1, '4': 5}
        self.assertEqual(expected_position_person_dict, sorter.position_person_dict)
        self.assertEqual(expected_person_horizontal_position_dict, sorter.person_horizontal_position_dict)

    def test_move_to_occupied(self):
        position_person_dict = {1: ['5'], 2: ['1', '2'], 3: ['4', '3']}
        person_level_dict = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 3}

        person_horizontal_position_dict = {'1': 2, '3': 3, '2': 2, '5': 1, '4': 3}
        person_nodes = self.build_person_nodes_dict(person_horizontal_position_dict)

        sorter = horizontal_sorter.HorizontalSorter(person_level_dict, self.edges, person_nodes)
        sorter.person_horizontal_position_dict = person_horizontal_position_dict
        sorter.position_person_dict = position_person_dict

        sorter.move('5', 2)

        expected_position_person_dict = {1: [], 2: ['1', '2'], 3: ['4', '5'], 5: ['3']}
        expected_person_horizontal_position_dict = {'1': 2, '3': 5, '2': 2, '5': 3, '4': 3}
        self.assertEqual(expected_position_person_dict, sorter.position_person_dict)
        self.assertEqual(expected_person_horizontal_position_dict, sorter.person_horizontal_position_dict)

    def test_put_siblings_next_each_other_bottom_up(self):

        position_person_dict = {1: ['5'], 2: ['1', '2'], 3: ['4'], 5: ['3']}
        person_level_dict = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 3}

        person_horizontal_position_dict = {'1': 2, '3': 5, '2': 2, '5': 1, '4': 3}
        person_nodes = self.build_person_nodes_dict(person_horizontal_position_dict)

        person_nodes[3].siblings = ['5']
        person_nodes[5].siblings = ['3']

        sorter = horizontal_sorter.HorizontalSorter(person_level_dict, self.edges, person_nodes)
        sorter.person_horizontal_position_dict = person_horizontal_position_dict
        sorter.position_person_dict = position_person_dict

        sorter.put_siblings_next_each_other_bottom_up()

        expected_difference = 2
        positions_to_check = list()
        positions_to_check.append(sorter.person_horizontal_position_dict['5'])
        positions_to_check.append(sorter.person_horizontal_position_dict['3'])
        self.assertTrue(self.assert_list_differences(positions_to_check, expected_difference))

        #retrieved_difference = abs(sorter.person_horizontal_position_dict['5'] - sorter.person_horizontal_position_dict['3'])

        #self.assertEqual(expected_difference, retrieved_difference)

    def test_put_siblings_next_each_other_bottom_up_three_bros(self):

        position_person_dict = {1: ['5'], 2: ['1', '2'], 3: ['4', '6'], 5: ['3']}
        person_level_dict = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 3, '6': 3}

        person_horizontal_position_dict = {'1': 2, '3': 5, '2': 2, '5': 1, '4': 3, '6': 3}
        person_nodes = self.build_person_nodes_dict(person_horizontal_position_dict)

        person_nodes[3].siblings = ['5', '6']
        person_nodes[5].siblings = ['3', '6']
        person_nodes[6].siblings = ['3', '5']

        sorter = horizontal_sorter.HorizontalSorter(person_level_dict, self.edges, person_nodes)
        sorter.person_horizontal_position_dict = person_horizontal_position_dict
        sorter.position_person_dict = position_person_dict

        sorter.put_siblings_next_each_other_bottom_up()

        # expected_differences = [2, 2, 4]
        # retrieved_differences = list()
        # retrieved_differences.append(abs(
        #     sorter.person_horizontal_position_dict['5'] - sorter.person_horizontal_position_dict['3']))
        # retrieved_differences.append(abs(
        #     sorter.person_horizontal_position_dict['6'] - sorter.person_horizontal_position_dict['3']))
        # retrieved_differences.append(abs(
        #     sorter.person_horizontal_position_dict['6'] - sorter.person_horizontal_position_dict['5']))
        # retrieved_differences.sort()

        expected_difference = 2
        positions_to_check = list()
        positions_to_check.append(sorter.person_horizontal_position_dict['5'])
        positions_to_check.append(sorter.person_horizontal_position_dict['3'])
        positions_to_check.append(sorter.person_horizontal_position_dict['6'])
        self.assertTrue(self.assert_list_differences(positions_to_check, expected_difference))

        #self.assertEqual(expected_differences, retrieved_differences)

    def not_test_are_there_persons_at_the_same_positions_false(self):
        position_person_dict = {1: ['5', '3'], 2: ['1', '2'], 3: ['4']}
        person_level_dict = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 4}
        edges = {}

        sorter = horizontal_sorter.HorizontalSorter(person_level_dict, edges)
        self.assertFalse(sorter.are_there_persons_at_the_same_positions(position_person_dict))

    def not_test_are_there_persons_at_the_same_positions_true(self):
        position_person_dict = {1: ['5', '3'], 2: ['1', '2'], 3: ['4']}
        person_level_dict = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 3}
        edges = {}

        sorter = horizontal_sorter.HorizontalSorter(person_level_dict, edges)
        self.assertTrue(sorter.are_there_persons_at_the_same_positions(position_person_dict))

    def not_test_get_level_of_person(self):
        person_level_dict = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 4}
        edges = {}
        sorter = horizontal_sorter.HorizontalSorter(person_level_dict, edges)
        expected_level = 4
        retrieved_level = sorter.get_level_of_person('5')

        self.assertEqual(retrieved_level, expected_level)

    def not_test_get_position_with_multiple_persons_raise(self):
        position_person_dict = {1: ['5', '3'], 2: ['1', '2'], 3: ['4']}
        person_level_dict = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 4}
        edges = {}

        sorter = horizontal_sorter.HorizontalSorter(person_level_dict, edges)
        retrieved_persons = sorter.get_position_with_multiple_persons(position_person_dict)

        self.assertIsNone(retrieved_persons)

    def not_test_get_position_with_multiple_persons_true(self):
        position_person_dict = {1: ['5', '3'], 2: ['1', '2'], 3: ['4']}
        person_level_dict = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 3}
        edges = {}
        sorter = horizontal_sorter.HorizontalSorter(person_level_dict, edges)
        expected_persons = ['5', '3']

        retrieved_persons = sorter.get_position_with_multiple_persons(position_person_dict)

        self.assertEqual(retrieved_persons, expected_persons)

    def not_test_build_person_dict(self):
        person_level_dict = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 3}
        edges = {}

        sorter = horizontal_sorter.HorizontalSorter(person_level_dict, edges)

        expected_output = {1: ['1'], 2: ['2'], 3: ['3', '5'], 4: ['4']}

        retrieved_output = sorter.build_level_person_dict()

        self.assertEqual(retrieved_output, expected_output)

    def not_test_assign_random_x_positions(self):
        person_level_dict = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 3}
        edges = {}
        expected_number_of_persons = len(person_level_dict)

        sorter = horizontal_sorter.HorizontalSorter(person_level_dict, edges)
        person_horizontal_position_dict = sorter.assign_random_x_positions()

        retrieved_number_of_persons = len(person_horizontal_position_dict)
        only_even_values_in_dict = self.only_even_numbers_in_dict(person_horizontal_position_dict)

        self.assertEqual(retrieved_number_of_persons, expected_number_of_persons)
        self.assertTrue(only_even_values_in_dict)

    def not_test_build_position_person_dict(self):
        person_level_dict = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 3}
        edges = {}
        sorter = horizontal_sorter.HorizontalSorter(person_level_dict, edges)
        sorter.person_horizontal_position_dict = {'1': 0, '3': 0, '2': 2, '5': 4, '4': 0}

        expected_position_person_dict = {0: ['1', '3', '4'], 2: ['2'], 4: ['5']}

        retrieved_position_person_dict = sorter.build_position_person_dict()

        self.assertEqual(retrieved_position_person_dict, expected_position_person_dict)

#
# def move_persons_from_same_level_and_position(self):
#     while self.are_there_persons_at_the_same_positions(self.position_person_dict):
#         position_with_multiple_persons = self.get_position_with_multiple_persons(self.position_person_dict)
#         i = 0
#         for person in position_with_multiple_persons:
#             print('persons with same position: {}'.format(position_with_multiple_persons))
#             self.move_person_on_horizontal_axis(person, -1 * i * 2)
#             i += 1

    def not_test_move_persons_from_same_level_and_position(self):
        pass

    def not_test_move_person_on_horizontal_axis_single_move(self):
        person_level_dict = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 3}
        edges = {}
        sorter = horizontal_sorter.HorizontalSorter(person_level_dict, edges)
        sorter.person_horizontal_position_dict = {'1': 0, '3': 0, '2': 2, '5': 4, '4': 0}
        sorter.position_person_dict = {0: ['1', '3', '4'], 2: ['2'], 4: ['5']}

        expected_position_person_dict = {0: ['1', '3'], 2: ['2', '4'], 4: ['5']}
        expected_person_horizontal_position_dict = {'1': 0, '3': 0, '2': 2, '5': 4, '4': 2}

        sorter.move_person_on_horizontal_axis('4', 2)

        retrieved_position_person_dict = sorter.position_person_dict
        retrieved_person_horizontal_position_dict = sorter.person_horizontal_position_dict

        self.assertEqual(retrieved_position_person_dict, expected_position_person_dict)
        self.assertEqual(retrieved_person_horizontal_position_dict, expected_person_horizontal_position_dict)

    def not_test_move_person_on_horizontal_axis_double_move(self):
        person_level_dict = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 3}
        edges = {}
        sorter = horizontal_sorter.HorizontalSorter(person_level_dict, edges)
        sorter.person_horizontal_position_dict = {'1': 0, '3': 2, '2': 2, '5': 4, '4': 0}
        sorter.position_person_dict = {0: ['1', '4'], 2: ['2', '3'], 4: ['5']}

        expected_position_person_dict = {0: ['1', '4'], 2: ['2'], 4: ['3'], 6: ['5']}
        expected_person_horizontal_position_dict = {'1': 0, '3': 4, '2': 2, '5': 6, '4': 0}

        sorter.move_person_on_horizontal_axis('3', 2)

        retrieved_position_person_dict = sorter.position_person_dict
        retrieved_person_horizontal_position_dict = sorter.person_horizontal_position_dict

        self.assertEqual(retrieved_position_person_dict, expected_position_person_dict)
        self.assertEqual(retrieved_person_horizontal_position_dict, expected_person_horizontal_position_dict)

    def not_test_move_person_on_horizontal_axis_to_position(self):
        person_level_dict = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 3}
        edges = {}
        sorter = horizontal_sorter.HorizontalSorter(person_level_dict, edges)
        sorter.person_horizontal_position_dict = {'1': 0, '3': 2, '2': 2, '5': 4, '4': 0}
        sorter.position_person_dict = {0: ['1', '4'], 2: ['2', '3'], 4: ['5']}

        expected_position_person_dict = {0: ['1', '4'], 2: ['2'], 4: ['3'], 6: ['5']}
        expected_person_horizontal_position_dict = {'1': 0, '3': 4, '2': 2, '5': 6, '4': 0}

        sorter.move_person_on_horizontal_axis_to_position('3', 4)

        retrieved_position_person_dict = sorter.position_person_dict
        retrieved_person_horizontal_position_dict = sorter.person_horizontal_position_dict

        self.assertEqual(retrieved_position_person_dict, expected_position_person_dict)
        self.assertEqual(retrieved_person_horizontal_position_dict, expected_person_horizontal_position_dict)


if __name__ == '__main__':
    unittest.main()
