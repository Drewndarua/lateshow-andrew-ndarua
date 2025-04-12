from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Episode, Guest, Appearance
from sqlalchemy.exc import IntegrityError
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def home():
    return {"message": "TV Guest API" }

@app.route('episodes', methods=['GET'])
def get_episodes():
    episodes = Episode.query.all()
    return jsonify([e.to_dict() for e in episodes]), 200

# 
@app.route('/episodes/<int:id>', methods=['GET'])
def get_episodes(id): 
    episode = Episode.query.get(id)
    if episode:
        return jsonify(episode.to_dict_with_appearances()), 200
    return jsonify({"error": "Episode not found"}), 404   

@app.route('/guests', methods=['GET'])
def get_guests(): 
    guests = Guest.query.all()
    return jsonify([g.to_dict() for g in guests]), 200

@app.route('/appearances', methods=['POST'])
def create_appearance():
    data = request.get_json()
    try: 
        appearance = Appearance(
            rating=data['rating'],
            guest_id=data['guest_id'], 
            episode_id=data['episode_id']
        )
        db.session.add(appearance)
        db.session.commit()
        return jsonify(appearance.to_dict()), 201
    except (KeyError, ValueError) as e:
        return jsonify({"error": str(e)}), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Invalid episode or guest ID"}), 400
    
    if __name__ == '__main__':
        app.run(debug=True)