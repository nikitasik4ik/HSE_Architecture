from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from backend.app import db


class User(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    role_id = db.Column(db.Integer, db.ForeignKey('Roles.id'))

    def to_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


class Role(db.Model):
    __tablename__ = 'Roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)


class MissingAnimal(db.Model):
    __tablename__ = 'MissingAnimals'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    category_id = db.Column(db.Integer, db.ForeignKey('CategoryAnimals.id'))
    description = db.Column(db.Text)
    date_last_seen = db.Column(db.DateTime)
    location_last_seen = db.Column(db.Text)
    image = db.Column(db.LargeBinary)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    status_id = db.Column(db.Integer, db.ForeignKey('Status.id'))

    def to_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


class Status(db.Model):
    __tablename__ = 'Status'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))


class CategoryAnimal(db.Model):
    __tablename__ = 'CategoryAnimals'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    type_id = db.Column(db.Integer, db.ForeignKey('BreedAnimals.id'))


class BreedAnimal(db.Model):
    __tablename__ = 'BreedAnimals'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class FoundAnimal(db.Model):
    __tablename__ = 'FoundAnimals'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    category_id = db.Column(db.Integer, db.ForeignKey('CategoryAnimals.id'))
    description = db.Column(db.Text)
    date_found = db.Column(db.DateTime)
    location_found = db.Column(db.Text)
    image = db.Column(db.LargeBinary)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))

    def to_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
