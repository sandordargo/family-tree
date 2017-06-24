class RelationshipTypeMapper(object):
    @staticmethod
    def get_mapper():
        return {"CHILD_OF": "IS CHILD OF",
                "MARRIED": "GOT MARRIED TO",
                "IS CHILD OF": "IS CHILD OF",
                "GOT MARRIED TO": "GOT MARRIED TO"}



class Relationship(object):
    def __init__(self, relationship_id, start_node, end_node, relationship_type, properties):
        self.relationship_id = relationship_id
        self.start_node = start_node
        self.end_node = end_node
        self.relationship_type = relationship_type
        self.properties = properties

    def get_as_json(self):
        relationship_as_dict = dict()
        relationship_as_dict['id'] = self.relationship_id
        relationship_as_dict['source'] = self.get_start_id()
        relationship_as_dict['target'] = self.get_end_id()
        relationship_as_dict['type'] = self.relationship_type
        return relationship_as_dict

    def get_formatted_person(self, person_json_string):
        start_node_as_str = person_json_string
        name_tag = 'name:"'
        name = start_node_as_str[start_node_as_str.find(name_tag) + len(name_tag):-3]

        birth_tag = 'born:'
        birth_tag_start = start_node_as_str.find(birth_tag) + len(birth_tag)
        birth_tag_end = start_node_as_str.find(',', birth_tag_start)
        birth = start_node_as_str[birth_tag_start:birth_tag_end]
        birth = birth.replace('"',"")

        death_tag = 'died:'
        death_tag_start = start_node_as_str.find(death_tag) + len(death_tag)
        death = ""
        if death_tag_start != -1 + len(death_tag):
            death_tag_end = start_node_as_str.find(',', death_tag_start)
            death = start_node_as_str[death_tag_start:death_tag_end]
        death = death.replace('"', "")

        return '{name} ({birth} - {death})'.format(name=name, birth=birth, death=death)

    def get_start_id(self):
        return str(self.start_node.uri).rsplit('/', 1)[-1]

    def get_end_id(self):
        return str(self.end_node.uri).rsplit('/', 1)[-1]

    def get_formatted_start(self):
        return self.get_formatted_person(str(self.start_node))

    def get_formatted_end(self):
        return self.get_formatted_person(str(self.end_node))

    def get_formatted_relationship_type(self):
        return Relationship.get_mapper()[self.relationship_type]

    @staticmethod
    def get_mapper():
        return RelationshipTypeMapper().get_mapper()
