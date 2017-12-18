class ListOfRequests:
    def __init__(self):
        self.items = {}

    def isEmpty(self):
        return self.items == {}

    def add_request(self, asker, req):
        self.items[asker] = req

    def get_request(self, asker):
        if (asker in self.items):
            return self.items[asker]
        else:
            return False

    def remove_from_requests(self, asker):
        if (asker in self.items):
            self.items.pop(asker)
        else:
            return False

    def contain(self, asker):
        return (asker in self.items)

    def size(self):
        return len(self.items)