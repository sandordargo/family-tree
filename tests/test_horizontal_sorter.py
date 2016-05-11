import unittest
from tree import horizontal_sorter


class TestHorizontalSorter(unittest.TestCase):
    def setUp(self):
        pass

    @staticmethod
    def only_even_numbers_in_dict(dict_to_check):
        for key in dict_to_check:
            if dict_to_check[key] % 2 != 0:
                return False
        return True

    def test_are_there_persons_at_the_same_positions_false(self):
        position_person_dict = {1: ['5', '3'], 2: ['1', '2'], 3: ['4']}
        person_level_dict = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 4}
        edges = {}

        sorter = horizontal_sorter.HorizontalSorter(person_level_dict, edges)
        self.assertFalse(sorter.are_there_persons_at_the_same_positions(position_person_dict))

    def test_are_there_persons_at_the_same_positions_true(self):
        position_person_dict = {1: ['5', '3'], 2: ['1', '2'], 3: ['4']}
        person_level_dict = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 3}
        edges = {}

        sorter = horizontal_sorter.HorizontalSorter(person_level_dict, edges)
        self.assertTrue(sorter.are_there_persons_at_the_same_positions(position_person_dict))

    def test_get_level_of_person(self):
        person_level_dict = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 4}
        edges = {}
        sorter = horizontal_sorter.HorizontalSorter(person_level_dict, edges)
        expected_level = 4
        retrieved_level = sorter.get_level_of_person('5')

        self.assertEqual(retrieved_level, expected_level)

    def test_get_position_with_multiple_persons_raise(self):
        position_person_dict = {1: ['5', '3'], 2: ['1', '2'], 3: ['4']}
        person_level_dict = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 4}
        edges = {}

        sorter = horizontal_sorter.HorizontalSorter(person_level_dict, edges)
        retrieved_persons = sorter.get_position_with_multiple_persons(position_person_dict)

        self.assertIsNone(retrieved_persons)

    def test_get_position_with_multiple_persons_true(self):
        position_person_dict = {1: ['5', '3'], 2: ['1', '2'], 3: ['4']}
        person_level_dict = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 3}
        edges = {}
        sorter = horizontal_sorter.HorizontalSorter(person_level_dict, edges)
        expected_persons = ['5', '3']

        retrieved_persons = sorter.get_position_with_multiple_persons(position_person_dict)

        self.assertEqual(retrieved_persons, expected_persons)

    def test_build_person_dict(self):
        person_level_dict = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 3}
        edges = {}

        sorter = horizontal_sorter.HorizontalSorter(person_level_dict, edges)

        expected_output = {1: ['1'], 2: ['2'], 3: ['3', '5'], 4: ['4']}

        retrieved_output = sorter.build_level_person_dict()

        self.assertEqual(retrieved_output, expected_output)

    def test_assign_random_x_positions(self):
        person_level_dict = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 3}
        edges = {}
        expected_number_of_persons = len(person_level_dict)

        sorter = horizontal_sorter.HorizontalSorter(person_level_dict, edges)
        person_horizontal_position_dict = sorter.assign_random_x_positions()

        retrieved_number_of_persons = len(person_horizontal_position_dict)
        only_even_values_in_dict = self.only_even_numbers_in_dict(person_horizontal_position_dict)

        self.assertEqual(retrieved_number_of_persons, expected_number_of_persons)
        self.assertTrue(only_even_values_in_dict)

    def test_build_position_person_dict(self):
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

    def test_move_persons_from_same_level_and_position(self):
        pass

    def test_move_person_on_horizontal_axis_single_move(self):
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

    def test_move_person_on_horizontal_axis_double_move(self):
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

    def test_move_person_on_horizontal_axis_to_position(self):
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
