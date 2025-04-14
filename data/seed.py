import json 
from app import app 

def load_json(): 
    with open() as f:
        return json.load()
    
    with app.app_context():
        db.drop_all()
        db.create_all()