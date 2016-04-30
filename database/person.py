class Person(object):
    def __init__(self, id, name, birth, properties):
        self.id = id
        self.name = name
        self.birth = birth
        self.properties = properties

    def get_as_json(self):
        size = 2
        color = '#666'
        node_as_dict = dict()
        node_as_dict['id'] = self.id
        node_as_dict['label'] = self.name
        node_as_dict['size'] = size
        node_as_dict['color'] = color
        return node_as_dict
