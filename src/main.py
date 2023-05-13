from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = '<URL>'
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


@app.route('/trips')
def get_trips():
    trips = Trips.query.all()
    return [trip.as_dict() for trip in trips]


if __name__ == '__main__':
    app.run(debug=False)
