class Item:
    def __init__(self, content, embedding):
        self.content = content
        self.embedding = embedding

    def to_tuple(self):
        return (self.content, self.embedding)
