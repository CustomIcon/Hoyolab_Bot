import ujson as json


class Database:
    def __init__(self):
        self.db = json.load(open('./database.json'))

    def new_user_id(self, user_id: int, genshin_id=int):
        self.db[user_id] = genshin_id
        self.save()

    def find_by_user_id(self, user_id: int):
        for key, value in self.db.items():
            if key == str(user_id):
                return value
        return False

    def find_by_user_uid(self, uid: int):
        for key, value in self.db.items():
            if value == str(uid):
                return key
        return False

    def remove_user_id(self, user_id: int):
        self.db.pop(str(user_id), None)
        self.save()

    def save(self):
        with open('database.json', 'w') as outfile:
            json.dump(self.db, outfile, indent=4)
            outfile.close()
