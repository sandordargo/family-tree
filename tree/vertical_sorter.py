class VerticalSorter(object):

    def __init__(self, edges):
        self.edges = edges
        self.levels_dictionary = self.build_levels_dictionary()

    def get_levels_dictionary(self):
        return self.levels_dictionary

    def build_levels_dictionary(self):
        person_level_dict = dict()
        visited_relationships_list = list()
        reachable_persons_list = list()

        # get first relationship, put high enough for a worst case scenario, where everyone would go under it
        # target to up or same level based on type of relationship
        if len(self.edges) == 0:
            return person_level_dict
        first_relationship = self.edges[0]
        person_level_dict[first_relationship['source']] = len(self.edges) + 1
        if first_relationship['type'] == 'CHILD_OF':
            person_level_dict[first_relationship['target']] = person_level_dict[first_relationship['source']] - 1
        if first_relationship['type'] == 'MARRIED':
            person_level_dict[first_relationship['target']] = person_level_dict[first_relationship['source']]
        visited_relationships_list.append(first_relationship['id'])
        reachable_persons_list.append(first_relationship['source'])
        reachable_persons_list.append(first_relationship['target'])

        # look for adjacent relationship until there is any non-visited
        # TODO if not and there is, get any relationship
        # TODO levels should start from zero
        while len(visited_relationships_list) < len(self.edges):
            for relationship in self.edges:
                if relationship['id'] not in visited_relationships_list and \
                        (relationship['source'] in reachable_persons_list or
                                 relationship['target'] in reachable_persons_list):
                    visited_relationships_list.append(relationship['id'])
                    if relationship['type'] == 'CHILD_OF' and relationship['target'] in reachable_persons_list:
                        person_level_dict[relationship['source']] = person_level_dict[relationship['target']] + 1
                        reachable_persons_list.append(relationship['source'])
                    elif relationship['type'] == 'CHILD_OF' and relationship['source'] in reachable_persons_list:
                        person_level_dict[relationship['target']] = person_level_dict[relationship['source']] - 1
                        reachable_persons_list.append(relationship['target'])
                    elif relationship['type'] == 'MARRIED' and relationship['target'] in reachable_persons_list:
                        person_level_dict[relationship['source']] = person_level_dict[relationship['target']]
                        reachable_persons_list.append(relationship['source'])
                    elif relationship['type'] == 'MARRIED' and relationship['source'] in reachable_persons_list:
                        person_level_dict[relationship['target']] = person_level_dict[relationship['source']]
                        reachable_persons_list.append(relationship['target'])
        return person_level_dict
