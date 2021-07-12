from database import database

class RateToOwnerModel(database.Model):
    __tablename__ = 'RateToOwner'

    id = database.Column(database.Integer, primary_key=True)
    user_id = database.Column(database.Integer, database.ForeignKey('users.id'))
    owner_id = database.Column(database.Integer, database.ForeignKey('owners.id'))
    rate = database.Column(database.Float(precision=1))

    user = database.relationship('UserModel', viewonly=True)
    owner = database.relationship('OwnerModel', viewonly=True)

    def save_to_database(self):
        database.session.add(self)
        database.session.commit()

    @classmethod
    def already_rated(cls, user_id, owner_id, rate):
        user = cls.get_user_id_for_rate(user_id)
        if user:
            for rate_model in user:
                if rate_model.owner_id == owner_id:
                    return True
        return False

    @classmethod
    def get_user_id_for_rate(cls, id):
        return cls.query.filter_by(user_id=id).all()

    @classmethod
    def find_user_by_id(cls, id):
        return cls.query.filter_by(user_id=id).first()

    @classmethod
    def find_owner_by_id(cls, id):
        return cls.query.filter_by(owner_id=id).first()
