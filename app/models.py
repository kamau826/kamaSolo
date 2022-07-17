from app import db,loginmanager
from datetime import date,time
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@loginmanager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_admin=db.Column(db.Boolean)
    phone=db.Column(db.Integer)
    posts = db.relationship('Lesson', backref='author', lazy='dynamic')
    bookings=db.relationship('Booking',backref='user',lazy='dynamic')
    comments=db.relationship('Feedback',backref='user',lazy='dynamic')
    reply= db.relationship('Reply', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Lesson(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(50))
    topic= db.Column(db.String(50))
    body=db.Column(db.String)
    pic=db.Column(db.String(255),nullable=True)
    video=db.Column(db.String(255),nullable=True)
    created_on=db.Column(db.DateTime,default=date.today())
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    course_id=db.Column(db.Integer,db.ForeignKey('course.id'))

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100))
    duration=db.Column(db.String(100))
    objective=db.Column(db.String(255))
    lessons=db.relationship('Lesson',backref='course',lazy='dynamic')

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_name=db.Column(db.String(255))
    event_location=db.Column(db.String(100))
    secret_id=db.Column(db.String(255))
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    event_date= db.Column(db.String(255))
    start_time=db.Column(db.String(255))
    status=db.Column(db.String(255),default='waiting approval')
    event_id=db.Column(db.Integer,db.ForeignKey('event.id'))
    price=db.Column(db.Integer)
    comments=db.relationship('Feedback',backref='booking',lazy='dynamic')

class Feedback(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    message=db.Column(db.String(255))
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'))
    created_on=db.Column(db.DateTime,default=date.today())
    reply=db.relationship('Reply',backref='feedback',lazy='dynamic')

class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255))
    feedback_id=db.Column(db.Integer,db.ForeignKey('feedback.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name =db.Column(db.String(55))
    date =db.Column(db.DateTime,default=date.today())
    price=db.Column(db.String(255))
    location=db.Column(db.String(100))
    bookings = db.relationship('Booking', backref='event', lazy='dynamic')