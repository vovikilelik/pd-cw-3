from dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, bid):
        return self.session.query(User).get(bid)

    def get_all(self, **fields):
        if len(fields):
            return self.session.query(User).filter_by(**fields).all()
        else:
            return self.session.query(User).all()

    def search_one(self, **fields):
        all_records = self.get_all(**fields)
        return all_records[0] if len(all_records) > 0 else None

    def create(self, user_d):
        ent = User(**user_d)
        self.session.add(ent)
        self.session.commit()
        return ent

    def delete(self, rid):
        user = self.get_one(rid)
        self.session.delete(user)
        self.session.commit()

    def update(self, user_d, **overrides):
        user = self.get_one(user_d.get("id"))

        user.username = overrides['username'] if 'username' in overrides else user_d.get("username")
        user.password = overrides['password'] if 'password' in overrides else user_d.get("password")

        user.name = overrides['name'] if 'name' in overrides else user_d.get("name")
        user.surname = overrides['surname'] if 'surname' in overrides else user_d.get("surname")
        user.favorite_genre = overrides['favorite_genre'] if 'favorite_genre' in overrides else user_d.get("favorite_genre")

        self.session.add(user)
        self.session.commit()
