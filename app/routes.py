from app import app,db,loginmanager
from flask import render_template,redirect,request,flash,url_for
from app.models import User,Lesson,Course,Booking,Event,Feedback,Reply
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import current_user,login_user,logout_user,login_required
from datetime import date
import os
import string
import secrets


loginmanager.login_view='login'


@app.route('/')
@app.route('/index')
def index():
    lessons=Lesson.query.all()
    courses=Course.query.all()
    bookings=Booking.query.all()
    return render_template('index.html',lessons=lessons,courses=courses,bookings=bookings)

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        user=User.query.filter_by(username=request.form['username'])
        # if user:
        #     flash("username already taken")
        user=User(username=request.form['username'],email=request.form['email'],password_hash=generate_password_hash(request.form['password']),is_admin=False,phone=request.form['phone'])
        db.session.add(user)
        db.session.commit()
        flash('registration successful')
        return redirect(url_for('login'))

    return render_template('register.html')

#login route
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        user=User.query.filter_by(username=request.form['username']).first()
        if user:
            if check_password_hash(user.password_hash,request.form['password']):
                login_user(user,remember=True)
                flash('login successful')
                return redirect(url_for('index'))
        flash('incorrect username or password')
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/admin')
@login_required
def admin():
    users=User.query.all()
    lessons=Lesson.query.all()
    courses=Course.query.all()
    bookings = Booking.query.all()
    #number of pending bookings
    pending=Booking.query.filter_by(status='waiting approval').count()
    #number of confirmed bookings
    confirmed=Booking.query.filter_by(status='confirmed').count()
    #number of attended
    attended=Booking.query.filter_by(status='attended').count()
    return  render_template('admin.html',users=users,lessons=lessons,
                            courses=courses,bookings=bookings,pending=pending,confirmed=confirmed,attended=attended)

#lessons routes

#add a lesson
@app.route('/add_lesson',methods=['GET','POST'])
def add_lesson():
    if request.method=='POST':
        course=request.form['course']
        lesson=Lesson(title=request.form['title'],topic=request.form['topic'],body=request.form['body'],course_id=course,video=request.form['video'], user_id=current_user.id)
        db.session.add(lesson)
        db.session.commit()
        flash('lesson added successfully')
        return redirect(url_for('index'))
    return render_template('add_lesson.html')

#view a single lesson
@app.route('/lesson/<int:id>',methods=['GET','POST'])
def lesson(id):

        lesson=Lesson.query.get(id)
        return render_template('lesson.html',lesson=lesson)

#edit a lesson
@app.route('/edit/<int:id>',methods=['GET','POST'])
@login_required
def edi(id):
    if request.method=='POST':
        lesson = Lesson.query.get(id)
        lesson.title=request.form['title']
        lesson.topic=request.form['topic']
        lesson.body=request.form['body']
        db.session.commit()
    return render_template(url_for('edit.html'))

#delete lesson
@app.route('/delete_lesson/<int:id>',methods=['GET','POST'])
@login_required
def delete(id):
    lesson=Lesson.query.get(id)
    db.session.delete(lesson)
    db.session.commit()
    flash('lesson deleted ')
    return redirect(url_for('index'))

#add course
@app.route('/add_course',methods=['GET','POST'])
@login_required
def add_course():
    if request.method=='POST':
        name=request.form['name']
        duration=request.form['duration']
        objective=request.form['objective']
        course=Course(name=name,duration=duration,objective=objective)
        db.session.add(course)
        db.session.commit()
        flash('course added successfully')
        return redirect(url_for('admin'))

#delete course
@app.route('/delete_course/<int:id>',methods=['GET','POST'])
@login_required
def delete_course(id):
    course=Course.query.get(id)
    db.session.delete(course)
    db.session.commit()
    flash('lesson deleted ')
    return redirect(url_for('index'))

#course
@app.route('/course/<int:id>',methods=['GET','POST'])
def course(id):
    course=Course.query.get(id)
    lessons=Lesson.query.all()
    return render_template('course.html',course=course)


#bookings
@app.route('/book',methods=['GET','POST'])
@login_required
def book():
    if request.method=='POST':
        user_id=current_user.id
        event_id=1
        name=request.form['name']
        location=request.form['event_location']
        date=request.form['event_date']
        time=request.form['start_time']
        price=request.form['price']
        alphabet = string.ascii_letters + string.digits
        secret_id = ''.join(secrets.choice(alphabet) for i in range(32))
        booking=Booking(user_id=user_id,event_id=event_id,event_name=name,event_location=location,event_date=date,start_time=time,price=price,secret_id= secret_id)
        db.session.add(booking)
        db.session.commit()
        flash('booking request recieved,I will reach you in a few')
    return render_template('index.html')

#

#events
@app.route('/add_event',methods=['GET','POST'])
def add_event():
    if request.method=='POST':

        name=request.form['name']
        price=request.form['price']
        location=request.form['location']
        event=Event(name=name,price=price,location=location)
        db.session.add(event)
        db.session.commit()
        flash('event added successfully')
    return redirect(url_for('admin'))





#book a date
@app.route('/book_session')
@login_required
def book_session():
    return render_template('book.html')


#view individual booking
@app.route('/booking/<id>',methods=['GET','POST'])
@login_required
def booking(id):
    booking=Booking.query.filter_by(secret_id=id).first()
    feedback=Feedback.query.filter_by(booking_id=booking.id)
    reply=Reply.query.filter_by(user_id=current_user.id)
    
    return render_template('view_booking.html',booking=booking,feedback=feedback)



#admin accept booking
@app.route('/admin_accept/<int:id>',methods=['GET','POST'])
def admin_accept(id):

        booking = Booking.query.get(id)
        booking.status='confirmed'
        db.session.commit()
        return redirect(url_for('admin'))

#admin_reject
@app.route('/admin_reject/<int:id>',methods=['GET','POST'])
def admin_reject(id):
    booking = Booking.query.get(id)
    booking.status = 'sorry,date taken'
    db.session.commit()
    return redirect(url_for('admin'))


@app.route('/attend/<int:id>')
def attend(id):
    booking=Booking.query.get(id)
    booking.status='attended'
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/feedback/<id>',methods=['GET','POST'])
@login_required
def feedback(id):
    booking=Booking.query.get(id)
    if request.method=='POST':
        message=request.form['message']

        feedback=Feedback(message=message,user_id=current_user.id,booking_id=id)
        db.session.add(feedback)
        db.session.commit()
        flash('comment added successfully')
        return redirect(url_for('index'))

@app.route('/admin_reply/<int:id>',methods=['GET','POST'])
@login_required
def admin_reply(id):
    replies=Reply.query.filter_by(feedback_id=id)
    if request.method=='POST':
        message=request.form['reply']
        reply=Reply(message=message,feedback_id=id,user_id=current_user.id)
        db.session.add(reply)
        db.session.commit()
        return redirect(url_for('booking',id=id))

#admin delete booking
@app.route('/delete_booking/<int:id>')
def delete_booking(id):
    booking=Booking.query.get(id)
    db.session.delete(booking)
    db.session.commit()
    return redirect(url_for('admin'))



#admin update user
@app.route('/delete_user/<int:id>',methods=['GET','POST'])
def delete_user(id):
    user=User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin'))



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))




