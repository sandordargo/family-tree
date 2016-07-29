import unittest
from database import relationship

class TestRelationship(unittest.TestCase):

    def setUp(self):
        self.relationship = relationship.Relationship(relationship_id=1,
                                                      start_node='(n0:Person {born:"2016",name:"Dargo Dalma Lea"})',
                                                      end_node='(n1:Person {born:1985,name:"DARGO Sandor"})',
                                                      relationship_type="CHILD_OF",
                                                      properties=list())

    def test_should_return_formatted_start_node(self):
        expected_start_node = "Dargo Dalma Lea (2016 - )"

        retrieved_start_node = self.relationship.get_formatted_start()

        self.assertEqual(expected_start_node, retrieved_start_node)

    def test_should_return_formatted_end_node(self):
        expected_end_node = "DARGO Sandor (1985 - )"

        retrieved_end_node = self.relationship.get_formatted_end()

        self.assertEqual(expected_end_node, retrieved_end_node)


if __name__ == '__main__':
    unittest.main()
