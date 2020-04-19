
class UserNote(object):
    
    def __init__(self, id, username, note):
        self.id = id
        self.username = username
        self.note = note

    def to_dict(self):
        return {"id": self.id, "username": self.username, "note": self.note}
