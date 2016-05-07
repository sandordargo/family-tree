import unittest
from tree import horizontal_sorter


class TestHorizontalSorter(unittest.TestCase):
    def setUp(self):
        pass

    def test_are_there_persons_at_the_same_positions_false(self):
        position_person_dict = {1: ['5', '3'], 2: ['1', '2'], 3: ['4']}
        levels_on_tree = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 4}
        edges = {}

        sorter = horizontal_sorter.HorizontalSorter(levels_on_tree, edges)
        self.assertFalse(sorter.are_there_persons_at_the_same_positions(position_person_dict))

    def test_are_there_persons_at_the_same_positions_true(self):
        position_person_dict = {1: ['5', '3'], 2: ['1', '2'], 3: ['4']}
        levels_on_tree = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 3}
        edges = {}

        sorter = horizontal_sorter.HorizontalSorter(levels_on_tree, edges)
        self.assertTrue(sorter.are_there_persons_at_the_same_positions(position_person_dict))

    def test_get_level_of_person(self):
        levels_on_tree = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 4}
        edges = {}
        sorter = horizontal_sorter.HorizontalSorter(levels_on_tree, edges)
        expected_level = 4
        retrieved_level = sorter.get_level_of_person('5')

        self.assertEqual(retrieved_level, expected_level)

    def test_get_position_with_multiple_persons_raise(self):
        position_person_dict = {1: ['5', '3'], 2: ['1', '2'], 3: ['4']}
        levels_on_tree = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 4}
        edges = {}

        sorter = horizontal_sorter.HorizontalSorter(levels_on_tree, edges)
        retrieved_persons = sorter.get_position_with_multiple_persons(position_person_dict)

        self.assertIsNone(retrieved_persons)

    def test_get_position_with_multiple_persons_true(self):
        position_person_dict = {1: ['5', '3'], 2: ['1', '2'], 3: ['4']}
        levels_on_tree = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 3}
        edges = {}
        sorter = horizontal_sorter.HorizontalSorter(levels_on_tree, edges)
        expected_persons = ['5', '3']

        retrieved_persons = sorter.get_position_with_multiple_persons(position_person_dict)

        self.assertEqual(retrieved_persons, expected_persons)


if __name__ == '__main__':
    unittest.main()
