class Person(object):
    def __init__(self, id, name, birth, properties):
        self.id = id
        self.name = name
        self.birth = birth
        self.properties = properties
        self.x = 0
        self.y = 0
        self.level = 0

    def get_as_json(self):
        node_as_dict = dict()
        node_as_dict['id'] = self.id
        node_as_dict['label'] = self.name
        return node_as_dict
