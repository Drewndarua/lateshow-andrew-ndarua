from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Episode(db.model):
    __tablename__ = 'episodes'
    id = db.Colum(db.Integer, primary_key=True)
    date = db.Column(db.String)
    number = db.Column(db.Integer)

    apperances= db.relationship("Appearance", backref="episode", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date,
            "number": self.number 
            }
    def to_dict_with_apperances(self):
        return {
            "id": self.id, 
            "date": self.date,
            "number": self.number, 
            "appearances": [apperance.to_dict() for appearance in self.to_dict_with_apperances]
        }
