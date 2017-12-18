class ListOfAnswerers:

    def __init__(self):
        self.items = {}

    def isEmpty(self):
        return self.items == {}

    def add_to_answerer(self, answerer_id, who_ask):
        if (answerer_id not in self.items):
            self.items[answerer_id] = [who_ask]
        else:
            self.items[answerer_id].append(who_ask)

    def get_first_asker(self, answerer_id):
        if (answerer_id in self.items):
            return self.items[answerer_id][0]
        else:
            return False

    def remove_from_answerer(self, answerer_id, who_ask):
        if (answerer_id in self.items):
            if (who_ask in self.items[answerer_id]):
                self.items[answerer_id].remove(who_ask)
                if (len(self.items[answerer_id]) == 0):
                    self.items.pop(answerer_id)
                return True
            else:
                return False
        else:
            return False

    def contain(self, answerer_id):
        return (answerer_id in self.items)

    def size(self):
        return len(self.items)