import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB

from utils.chatgpt_call import generate_trip
from utils.matching import calculate_user_compatibility
from utils.split_dates import split_dates
from utils.generate_plan import generate_plan

load_dotenv()

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = os.getenv("MONGO_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # Disable modification tracking, if desired

db = SQLAlchemy(app)


class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    password = db.Column(db.String)
    username = db.Column(db.String)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Interests(db.Model):
    interest_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    interests = db.relationship("Users", backref=db.backref("interests", uselist=True))
    name = db.Column(db.String)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Trips(db.Model):
    trip_id = db.Column(db.Integer, primary_key=True)
    trip_json = db.Column(JSONB)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    interests = db.relationship("Users", backref=db.backref("trips", uselist=True))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


@app.route('/users')
def get_users():
    users = Users.query.all()
    return [user.as_dict() for user in users]

@app.route('/users/', methods=['POST'])
def create_users():
    data = request.get_json()

    # extract data from JSON request
    email = data.get('email')
    password = data.get('password')
    username = data.get('username')

    # create new User instance with the extracted data
    new_user = Users(email=email, password=password, username=username)

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    # return the newly created user with a 201 status code
    return jsonify({'user_id': new_user.user_id,
                    'email': new_user.email,
                    'password': new_user.password,
                    'username': new_user.username}), 201

@app.route('/interests')
def get_interests():
    interests = Interests.query.all()
    return [interest.as_dict() for interest in interests]

@app.route('/interests', methods=['POST'])
def create_interest():
    data = request.get_json()

    # extract data from JSON request
    name = data.get('name')
    user_id = data.get('user_id')

    # create new Interests instance with the extracted data and the user_id
    new_interest = Interests(name=name, user_id=user_id)

    # add the new interest to the database
    db.session.add(new_interest)
    db.session.commit()

    # return the newly created interest with a 201 status code
    return jsonify({'interest_id': new_interest.interest_id,
                    'user_id': new_interest.user_id,
                    'name': new_interest.name}), 201

@app.route('/interests', methods=['DELETE'])
def delete_all_interests():
    interests = Interests.query.all()
    for i in interests:
        db.session.delete(i)
    db.session.commit()

    return interests, 202

@app.route('/trips')
def get_trips():
    trips = Trips.query.all()
    return [trip.as_dict() for trip in trips]

@app.route('/trips', methods=['POST'])
def create_trip():
    data = request.get_json()

    # extract data from JSON request
    trip_json = data.get('trip_json')
    user_id = data.get('user_id')

    # create new Trips instance with the extracted data and the user_id
    new_trip = Trips(trip_json=trip_json, user_id=user_id)

    # add the new trip to the database
    db.session.add(new_trip)
    db.session.commit()

    # return the newly created trip with a 201 status code
    return jsonify({'trip_id': new_trip.trip_id,
                    'user_id': new_trip.user_id,
                    'trip_json': new_trip.trip_json}), 201

@app.route('/trips/<int:trip_id>', methods=['GET'])
def get_trip(trip_id):
    trip = Trips.query.filter_by(trip_id=trip_id).first_or_404()

    return jsonify({'trip_id': trip.trip_id,
                    'user_id': trip.user_id,
                    'trip_json': trip.trip_json}), 200

@app.route('/trips/user/<int:user_id>', methods=['GET'])
def get_trips_by_user(user_id):
    trips = Trips.query.filter_by(user_id=user_id).all()
    trips_list = []
    for trip in trips:
        trips_list.append(trip.as_dict())
    return jsonify(trips=trips_list)

@app.route('/trips/suggestion', methods=['GET'])
def trip_suggestion():
    data = request.get_json()

    plan = data["plan"]
    user_id = data["user_id"]

    interests = Interests.query.filter_by(user_id=user_id).all()
    list_interests = [interest.name for interest in interests]

    trip = generate_trip(plan, list_interests, os.getenv("CHATGPT_KEY"))

    return trip, 200

@app.route('/trips', methods=['DELETE'])
def delete_all_trips():
    trips = Trips.query.all()
    for i in trips:
        db.session.delete(i)
    db.session.commit()

    return trips, 202

@app.route('/buddies', methods=['GET'])
def get_buddies():
    plan = request.get_json()

    # Get my trip
    my_plan = generate_plan(plan)

    candidates = Trips.query.all()
    buddies = {}
    for candidate_trip in candidates:
        # Get trip for a potential buddy
        candidate_plan = generate_plan(candidate_trip.trip_json)
        # Get the list of dates in which we match
        matches = calculate_user_compatibility(my_plan, candidate_plan)

        # If user has nothing in common skip
        if(len(matches) == 0):
            continue

        # Get users info
        buddy = Users.query.filter_by(user_id=candidate_trip.user_id).first_or_404()

        # If buddy is not in list or list is longer add it to result
        if(buddy.username not in buddies or
           len(buddies[buddy.username]) < len(matches)):
            buddies[buddy.username] = matches

    buddies = sorted(list(buddies.items()), key= lambda x: -len(x[1]))
    
    return {"buddies": buddies}, 200



if __name__ == '__main__':
    app.run(debug=False)
