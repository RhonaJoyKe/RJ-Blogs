from flask import render_template,request, redirect, url_for, abort, flash
from . import main
from flask_login import login_required, current_user
from ..models import  User
from .. import db, photos
from .forms import UpdateProfile
@main.route('/')
def index():
    pitches = Pitches.query.order_by(Pitches.date_created).all()
    
    return render_template('index.html',pitches=pitches)
@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)
@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    form = UpdateProfile()
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)
    if form.validate_on_submit():
        user.bio = form.bio.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('.profile',uname=user.username))
    return render_template('profile/update.html',form =form)