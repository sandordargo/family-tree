class PersonNode(object):

    def __init__(self):
        self.person_id = None
        self.label = None
        self.vertical_position = None
        self.horizontal_position = None
        self.parents = list()
        self.children = list()
        self.siblings = list()
        self.size = None
        self.color = None

    def get_as_json(self):
        node_as_dict = dict()
        node_as_dict['id'] = self.person_id
        node_as_dict['label'] = self.label
        node_as_dict['x'] = self.horizontal_position
        node_as_dict['y'] = self.vertical_position
        return node_as_dict
