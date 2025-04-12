from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Episode(db.model):
    __tablename__ = 'episodes'
    id = db.Colum(db.Integer, primary_key=True)
    date = db.Column(db.String)
    number = db.Column(db.Integer)

    appearances = db.relationship("Appearance", backref="episode", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date,
            "number": self.number 
            }
    
    def to_dict_with_appearances(self):
        return {
            "id": self.id, 
            "date": self.date,
            "number": self.number, 
            "appearances": [appearance.to_dict() for appearance in self.to_dict_with_appearances]
        }
    
class Guest(db.model):
    __tablename__ = 'guests'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    occupation = db.Column(db.String)
    appearances = db.relationship("Appearance", backref="guests", cascade="all, delete-orphan")

    def to_dict(self):
        return{
            "id": self.id, 
            "name": self.name,
            "occupation": self.occupation
        }
    
class Appearance(db.Model):
    __tablename__ = 'appearances'
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)

    episode_id = db.column(db.Integer, db.ForeignKey('episodes.id'))
    guest_id = db.column(db.Integer, db.ForeignKey('guests.id'))

    @validates('rating')
    def validate_rating(self, key, value):
        if not (1<= value <=5):
            raise ValueError("Rating must be between 1 and 5")
        return value
    
    def to_dict(self):
        return {
            "id": self.id,
            "rating": self.rating,
            "episode_id": self.episode_id, 
            "guest_id": self.guest_id,
            "episode": self.episode.to_dict(),
            "guest": self.guest.to_dict()
        }