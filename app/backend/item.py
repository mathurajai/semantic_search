import numpy as np

class Item:
    def __init__(self, content, embedding):
        self.content = content
        self.embedding = embedding

    def to_tuple(self):
        return (self.content, self.embedding)

    def to_dict_for_redis(self):
        return {
            'content': self.content,
            'content_embedding': np.array(self.embedding, dtype=np.float32).tobytes()
        }