class Relationship(object):
    def __init__(self, relationship_id, start_node, end_node, relationship_type, properties):
        self.relationship_id = relationship_id
        self.start_node = start_node
        self.end_node = end_node
        self.relationship_type = relationship_type
        self.properties = properties

    def get_as_json(self):
        size = 2
        relationship_as_dict = dict()
        relationship_as_dict['id'] = self.relationship_id
        relationship_as_dict['source'] = str(self.start_node.uri).rsplit('/', 1)[-1]
        relationship_as_dict['target'] = str(self.end_node.uri).rsplit('/', 1)[-1]
        relationship_as_dict['type'] = self.relationship_type
        relationship_as_dict['size'] = size
        return relationship_as_dict
