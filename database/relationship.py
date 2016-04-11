class Relationship(object):
    def __init__(self, relationship_id, start_node, end_node, relationship_type, properties):
        self.relationship_id = relationship_id
        self.start_node = start_node
        self.end_node = end_node
        self.relationship_type = relationship_type
        self.properties = properties
