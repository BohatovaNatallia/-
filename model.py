from app import db
from flask_login import UserMixin


class UserCredentials(db.Model):
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        login = db.Column(db.String(64), unique=True)
        password = db.Column(db.String(64))
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

        def __init__(self, login, password, user_id):
            self.login = login
            self.password = password
            self.user_id = user_id


class UserType(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type_name = db.Column(db.String(64))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False)
    surname = db.Column(db.String(64), nullable=False)
    lastname = db.Column(db.String(64), nullable=False)
    type_id = db.Column('type_id', db.Integer, db.ForeignKey(UserType.id))

    def __repr__(self):
        return '<User {}>'.format(self.name)

    def __init__(self):
        self.type_id = 2


class Picture(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    picture = db.Column(db.LargeBinary, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(64))


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    number = db.Column(db.Integer, unique=True)


class m2m_user_group(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))


class UserSubject(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    subject_id = db.Column(db.Integer, db.ForeignKey('Subject.id'))

    def __repr__(self):
        return '<Type {}>'.format(self.type_name)
